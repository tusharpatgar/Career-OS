"""Load source configuration from the repository defaults and user overrides."""

from __future__ import annotations

from pathlib import Path

from .parser import (
    ORIGIN_OVERRIDE,
    ORIGIN_REPOSITORY,
    SPECS,
    ParseResult,
    SourceIssue,
    SourceRecord,
    SourceSpec,
    normalize_name,
    normalize_url,
    parse_source_text,
)


def load_file(path: str | Path, spec: SourceSpec, *, origin: str = ORIGIN_REPOSITORY) -> ParseResult:
    """Read and parse one source file; missing or unreadable files are reported."""
    path = Path(path)
    filename = path.name
    if not path.exists():
        return ParseResult(
            spec.kind,
            (),
            (SourceIssue("missing_file", f"configured source file was not found at {path}", filename),),
        )
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return ParseResult(
            spec.kind,
            (),
            (SourceIssue("invalid_encoding", f"file is not valid UTF-8: {exc}", filename),),
        )
    except OSError as exc:
        return ParseResult(
            spec.kind,
            (),
            (SourceIssue("unreadable_file", f"file could not be read: {exc}", filename),),
        )
    return parse_source_text(text, spec, origin=origin, filename=filename)


def load_kind(
    config_dir: str | Path,
    spec: SourceSpec,
    *,
    override_dir: str | Path | None = None,
) -> ParseResult:
    """Load one source kind, layering an optional user override file over the defaults.

    Overrides are matched by normalized source name: an override entry replaces
    the default entry of the same name and new names are appended. Replaced
    defaults are returned by the caller's report as overridden, never dropped
    silently, because the override file itself remains on disk.
    """
    config_dir = Path(config_dir)
    defaults = load_file(config_dir / spec.filename, spec, origin=ORIGIN_REPOSITORY)

    if override_dir is None:
        return defaults

    override_path = Path(override_dir) / spec.filename
    if not override_path.exists():
        return defaults

    overrides = load_file(override_path, spec, origin=ORIGIN_OVERRIDE)
    return merge_results(defaults, overrides)


def load_all(
    config_dir: str | Path,
    *,
    override_dir: str | Path | None = None,
    specs: tuple[SourceSpec, ...] = SPECS,
) -> dict[str, ParseResult]:
    """Load every source kind, keyed by source kind."""
    return {spec.kind: load_kind(config_dir, spec, override_dir=override_dir) for spec in specs}


def merge_results(defaults: ParseResult, overrides: ParseResult) -> ParseResult:
    """Merge an override layer over repository defaults."""
    merged: dict[str, SourceRecord] = {}
    order: list[str] = []

    for record in defaults.records:
        key = normalize_name(record.name)
        merged[key] = record
        order.append(key)

    for record in overrides.records:
        key = normalize_name(record.name)
        if key not in merged:
            order.append(key)
        merged[key] = record

    issues: list[SourceIssue] = list(defaults.issues) + list(overrides.issues)
    seen_urls: dict[str, str] = {}
    records: list[SourceRecord] = []
    for record in (merged[key] for key in order):
        url_key = normalize_url(record.url)
        if url_key in seen_urls:
            issues.append(
                SourceIssue(
                    "duplicate_url",
                    f"{record.name!r} reuses a URL already configured in {seen_urls[url_key]}",
                    record.filename,
                    record.line,
                    record.url,
                )
            )
            continue
        seen_urls[url_key] = f"{record.filename}:{record.line}"
        records.append(record)

    return ParseResult(kind=defaults.kind, records=tuple(records), issues=tuple(issues))
