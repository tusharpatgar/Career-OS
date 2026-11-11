"""Parse and validate the editable Career OS source configuration files.

Formats are documented in config/README.md. Parsing never silently drops a
configured source: every rejected row produces a :class:`SourceIssue` that the
caller must surface to the user.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping
from urllib.parse import urlsplit, urlunsplit

ALLOWED_SCHEMES = frozenset({"http", "https"})
_ENABLED_TRUE = frozenset({"true"})
_ENABLED_FALSE = frozenset({"false"})

ORIGIN_REPOSITORY = "repository"
ORIGIN_OVERRIDE = "override"


@dataclass(frozen=True)
class SourceIssue:
    """A rejected row or file problem that must be shown, never swallowed."""

    code: str
    message: str
    filename: str
    line: int = 0
    raw: str = ""

    def __str__(self) -> str:
        where = f"{self.filename}:{self.line}" if self.line else self.filename
        return f"{where}: {self.code}: {self.message}"


@dataclass(frozen=True)
class FieldSpec:
    key: str
    label: str
    kind: str = "text"  # "text" | "url" | "bool" | "adapter"


@dataclass(frozen=True)
class SourceSpec:
    kind: str
    filename: str
    fields: tuple[FieldSpec, ...]
    summary: str

    @property
    def field_count(self) -> int:
        return len(self.fields)

    @property
    def field_keys(self) -> tuple[str, ...]:
        return tuple(field.key for field in self.fields)


PLATFORM_SPEC = SourceSpec(
    kind="platform",
    filename="platforms.txt",
    fields=(
        FieldSpec("name", "Platform Name"),
        FieldSpec("url", "Base URL", "url"),
        FieldSpec("adapter", "Adapter ID", "adapter"),
        FieldSpec("enabled", "Enabled", "bool"),
    ),
    summary="Platform Name | Base URL | Adapter ID | Enabled",
)

COMPANY_PORTAL_SPEC = SourceSpec(
    kind="company_portal",
    filename="companyportals.txt",
    fields=(
        FieldSpec("name", "Company Name"),
        FieldSpec("url", "Official Careers URL", "url"),
        FieldSpec("market", "Market"),
        FieldSpec("category", "Category"),
        FieldSpec("enabled", "Enabled", "bool"),
    ),
    summary="Company Name | Official Careers URL | Market | Category | Enabled",
)

RECRUITMENT_SPEC = SourceSpec(
    kind="recruitment",
    filename="recruitment_sources.txt",
    fields=(
        FieldSpec("name", "Consultancy Name"),
        FieldSpec("url", "Official Website URL", "url"),
        FieldSpec("geography", "Geography"),
        FieldSpec("specialization", "Specialization"),
        FieldSpec("enabled", "Enabled", "bool"),
    ),
    summary="Consultancy Name | Official Website URL | Geography | Specialization | Enabled",
)

SPECS: tuple[SourceSpec, ...] = (PLATFORM_SPEC, COMPANY_PORTAL_SPEC, RECRUITMENT_SPEC)
SPEC_BY_KIND: dict[str, SourceSpec] = {spec.kind: spec for spec in SPECS}
SPEC_BY_FILENAME: dict[str, SourceSpec] = {spec.filename: spec for spec in SPECS}


@dataclass(frozen=True)
class SourceRecord:
    """One validated, enabled or disabled source entry."""

    kind: str
    filename: str
    line: int
    origin: str
    name: str
    url: str
    enabled: bool
    fields: Mapping[str, str]

    @property
    def adapter_id(self) -> str | None:
        return self.fields.get("adapter")

    @property
    def market(self) -> str | None:
        return self.fields.get("market")

    @property
    def category(self) -> str | None:
        return self.fields.get("category")

    @property
    def geography(self) -> str | None:
        return self.fields.get("geography")

    @property
    def specialization(self) -> str | None:
        return self.fields.get("specialization")

    @property
    def is_override(self) -> bool:
        return self.origin == ORIGIN_OVERRIDE


@dataclass(frozen=True)
class ParseResult:
    kind: str
    records: tuple[SourceRecord, ...] = ()
    issues: tuple[SourceIssue, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.issues

    def extend(self, other: "ParseResult") -> "ParseResult":
        if other.kind != self.kind:
            raise ValueError(f"cannot merge {other.kind!r} into {self.kind!r}")
        return ParseResult(
            kind=self.kind,
            records=self.records + other.records,
            issues=self.issues + other.issues,
        )


def normalize_name(value: str) -> str:
    """Case- and whitespace-insensitive key for source names."""
    return " ".join(value.split()).casefold()


def normalize_url(value: str) -> str:
    """Comparable form of a URL: lower-case scheme/host, no fragment, no trailing slash."""
    parts = urlsplit(value.strip())
    path = parts.path.rstrip("/")
    netloc = parts.netloc.lower()
    return urlunsplit((parts.scheme.lower(), netloc, path, parts.query, ""))


def parse_source_text(
    text: str,
    spec: SourceSpec,
    *,
    origin: str = ORIGIN_REPOSITORY,
    filename: str | None = None,
) -> ParseResult:
    """Parse one source file's text according to ``spec``.

    Comments (lines starting with ``#``) and blank lines are ignored. Every
    other line must contain exactly the spec's field count and valid values.
    """
    name = filename or spec.filename
    records: list[SourceRecord] = []
    issues: list[SourceIssue] = []
    seen_names: dict[str, int] = {}
    seen_urls: dict[str, int] = {}

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        record, row_issues = _parse_row(line, spec, name, line_number, origin)
        if record is None:
            issues.extend(row_issues)
            continue

        name_key = normalize_name(record.name)
        url_key = normalize_url(record.url)
        if name_key in seen_names:
            issues.append(
                SourceIssue(
                    "duplicate_name",
                    f"{record.name!r} is already configured on line {seen_names[name_key]}",
                    name,
                    line_number,
                    line,
                )
            )
            continue
        if url_key in seen_urls:
            issues.append(
                SourceIssue(
                    "duplicate_url",
                    f"{record.url!r} is already configured on line {seen_urls[url_key]}",
                    name,
                    line_number,
                    line,
                )
            )
            continue

        seen_names[name_key] = line_number
        seen_urls[url_key] = line_number
        records.append(record)

    return ParseResult(kind=spec.kind, records=tuple(records), issues=tuple(issues))


def _parse_row(
    line: str,
    spec: SourceSpec,
    filename: str,
    line_number: int,
    origin: str,
) -> tuple[SourceRecord | None, list[SourceIssue]]:
    parts = [part.strip() for part in line.split("|")]
    if len(parts) != spec.field_count:
        return None, [
            SourceIssue(
                "wrong_field_count",
                f"expected {spec.field_count} fields ({spec.summary}), found {len(parts)}",
                filename,
                line_number,
                line,
            )
        ]

    fields = {field.key: value for field, value in zip(spec.fields, parts)}
    issues: list[SourceIssue] = []

    name = fields["name"]
    if not name:
        issues.append(SourceIssue("empty_name", "name must not be empty", filename, line_number, line))

    url = fields["url"]
    url_problem = url_error(url)
    if url_problem is not None:
        code, message = url_problem
        issues.append(SourceIssue(code, message, filename, line_number, line))

    enabled_raw = fields["enabled"]
    if enabled_raw.lower() not in _ENABLED_TRUE | _ENABLED_FALSE:
        issues.append(
            SourceIssue(
                "invalid_enabled",
                f"enabled must be 'true' or 'false', found {enabled_raw!r}",
                filename,
                line_number,
                line,
            )
        )

    if "adapter" in fields and not fields["adapter"]:
        issues.append(
            SourceIssue(
                "empty_adapter",
                "adapter ID must not be empty; use 'pending' when no adapter exists",
                filename,
                line_number,
                line,
            )
        )

    if issues:
        return None, issues

    return (
        SourceRecord(
            kind=spec.kind,
            filename=filename,
            line=line_number,
            origin=origin,
            name=name,
            url=url,
            enabled=enabled_raw.lower() in _ENABLED_TRUE,
            fields=fields,
        ),
        [],
    )


def url_error(url: str) -> tuple[str, str] | None:
    """Return ``(code, message)`` when ``url`` is not a safe http(s) URL."""
    if not url:
        return ("invalid_url", "URL must not be empty")
    if any(character.isspace() for character in url) or any(ord(character) < 32 for character in url):
        return ("invalid_url", f"URL must not contain whitespace or control characters: {url!r}")

    try:
        parts = urlsplit(url)
        hostname = parts.hostname
        port = parts.port
    except ValueError:
        return ("invalid_url", f"URL could not be parsed: {url!r}")

    if parts.scheme.lower() not in ALLOWED_SCHEMES:
        return ("invalid_url", f"URL scheme must be http or https: {url!r}")
    if not hostname:
        return ("invalid_url", f"URL must include a host: {url!r}")
    if parts.username or parts.password:
        return ("invalid_url", f"URL must not embed credentials: {url!r}")
    if port is not None and not 0 < port < 65536:
        return ("invalid_url", f"URL port is out of range: {url!r}")
    return None
