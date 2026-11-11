from __future__ import annotations

from pathlib import Path

import pytest

from careeros.sources.loader import load_all, load_kind
from careeros.sources.parser import (
    COMPANY_PORTAL_SPEC,
    ORIGIN_OVERRIDE,
    PLATFORM_SPEC,
    RECRUITMENT_SPEC,
    normalize_name,
    normalize_url,
    parse_source_text,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "config"

HEADER = "# CAREER OS\n# Format: Name | URL | Adapter | Enabled\n\n"
VALID_TEXT = HEADER + """
Naukri | https://www.naukri.com/ | jobspy | true
LinkedIn Jobs | https://www.linkedin.com/jobs/ | pending | false
"""


def codes(result) -> list[str]:
    return [issue.code for issue in result.issues]


def test_comments_and_blank_lines_are_ignored() -> None:
    result = parse_source_text(VALID_TEXT, PLATFORM_SPEC)
    assert result.ok
    assert [record.name for record in result.records] == ["Naukri", "LinkedIn Jobs"]
    assert result.records[0].line == 5
    assert result.records[0].adapter_id == "jobspy"
    assert result.records[0].enabled is True
    assert result.records[1].enabled is False


def test_fields_are_trimmed_and_booleans_are_case_insensitive() -> None:
    result = parse_source_text("  Naukri  |  https://www.naukri.com/  |  jobspy  |  TRUE ", PLATFORM_SPEC)
    assert result.ok
    record = result.records[0]
    assert record.name == "Naukri"
    assert record.url == "https://www.naukri.com/"
    assert record.enabled is True


def test_company_portal_and_recruitment_formats_parse() -> None:
    portal = parse_source_text(
        "Microsoft | https://careers.microsoft.com/ | India+Global | MANGOS | true", COMPANY_PORTAL_SPEC
    )
    assert portal.ok
    assert portal.records[0].market == "India+Global"
    assert portal.records[0].category == "MANGOS"
    assert portal.records[0].adapter_id is None

    consultancy = parse_source_text(
        "Quess Corp | https://www.quesscorp.com/ | India | Staffing-IT-General | true", RECRUITMENT_SPEC
    )
    assert consultancy.ok
    assert consultancy.records[0].geography == "India"
    assert consultancy.records[0].specialization == "Staffing-IT-General"


@pytest.mark.parametrize(
    ("line", "expected_code"),
    [
        ("Naukri | https://www.naukri.com/ | jobspy", "wrong_field_count"),
        ("Naukri | https://www.naukri.com/ | jobspy | true | extra", "wrong_field_count"),
        (" | https://www.naukri.com/ | jobspy | true", "empty_name"),
        ("Naukri | https://www.naukri.com/ |  | true", "empty_adapter"),
        ("Naukri | https://www.naukri.com/ | jobspy | yes", "invalid_enabled"),
        ("Naukri | javascript:alert(1) | jobspy | true", "invalid_url"),
        ("Naukri | file:///etc/passwd | jobspy | true", "invalid_url"),
        ("Naukri | ftp://www.naukri.com/ | jobspy | true", "invalid_url"),
        ("Naukri | https://user:secret@www.naukri.com/ | jobspy | true", "invalid_url"),
        ("Naukri | https:// | jobspy | true", "invalid_url"),
        ("Naukri | https://www.naukri.com/a b | jobspy | true", "invalid_url"),
    ],
)
def test_invalid_rows_are_rejected_with_visible_issues(line: str, expected_code: str) -> None:
    result = parse_source_text(line, PLATFORM_SPEC)
    assert result.records == ()
    assert codes(result) == [expected_code]
    assert result.issues[0].line == 1
    assert result.issues[0].filename == PLATFORM_SPEC.filename


def test_duplicate_names_are_rejected_case_insensitively() -> None:
    result = parse_source_text(
        "Naukri | https://www.naukri.com/ | jobspy | true\n"
        "  naukri   | https://www.naukri.com/other | jobspy | true\n",
        PLATFORM_SPEC,
    )
    assert [record.name for record in result.records] == ["Naukri"]
    assert codes(result) == ["duplicate_name"]
    assert "line 1" in result.issues[0].message


def test_duplicate_urls_are_rejected_after_normalization() -> None:
    result = parse_source_text(
        "Naukri | https://www.naukri.com/ | jobspy | true\n"
        "Naukri Mirror | HTTPS://WWW.NAUKRI.COM | jobspy | true\n",
        PLATFORM_SPEC,
    )
    assert [record.name for record in result.records] == ["Naukri"]
    assert codes(result) == ["duplicate_url"]


def test_normalizers() -> None:
    assert normalize_name("  Amazon   /  AWS ") == "amazon / aws"
    assert normalize_url("HTTPS://Example.COM/Path/?b=2#frag") == "https://example.com/Path?b=2"


def test_disabled_sources_are_preserved_not_dropped() -> None:
    result = parse_source_text(
        "LinkedIn Jobs | https://www.linkedin.com/jobs/ | pending | false", PLATFORM_SPEC
    )
    assert result.ok
    assert result.records[0].enabled is False


@pytest.mark.parametrize(
    "spec", [PLATFORM_SPEC, COMPANY_PORTAL_SPEC, RECRUITMENT_SPEC], ids=lambda spec: spec.filename
)
def test_repository_seed_files_parse_without_issues(spec) -> None:
    result = load_kind(CONFIG_DIR, spec)
    assert result.issues == ()
    assert result.records, f"{spec.filename} should contain at least one source"
    assert all(record.origin == "repository" for record in result.records)


def test_repository_seed_files_have_expected_minimum_coverage() -> None:
    results = load_all(CONFIG_DIR)
    assert len(results["platform"].records) >= 20
    assert len(results["company_portal"].records) >= 50
    assert len(results["recruitment"].records) >= 20
    assert all(result.ok for result in results.values())


def test_missing_file_is_reported_not_silently_skipped(tmp_path: Path) -> None:
    result = load_kind(tmp_path, PLATFORM_SPEC)
    assert result.records == ()
    assert codes(result) == ["missing_file"]


def test_override_layer_replaces_by_name_and_appends_new_entries(tmp_path: Path) -> None:
    repo_dir = tmp_path / "config"
    override_dir = tmp_path / "overrides"
    repo_dir.mkdir()
    override_dir.mkdir()

    (repo_dir / "platforms.txt").write_text(
        "Naukri | https://www.naukri.com/ | jobspy | true\n"
        "Indeed India | https://in.indeed.com/ | jobspy | true\n",
        encoding="utf-8",
    )
    (override_dir / "platforms.txt").write_text(
        "Naukri | https://www.naukri.com/ | jobspy | false\n"
        "Hirist | https://www.hirist.com/ | pending | true\n",
        encoding="utf-8",
    )

    result = load_kind(repo_dir, PLATFORM_SPEC, override_dir=override_dir)

    by_name = {record.name: record for record in result.records}
    assert [record.name for record in result.records] == ["Naukri", "Indeed India", "Hirist"]
    assert by_name["Naukri"].enabled is False
    assert by_name["Naukri"].origin == ORIGIN_OVERRIDE
    assert by_name["Indeed India"].origin == "repository"
    assert by_name["Hirist"].is_override is True
    assert result.ok


def test_override_layer_duplicate_url_is_reported(tmp_path: Path) -> None:
    repo_dir = tmp_path / "config"
    override_dir = tmp_path / "overrides"
    repo_dir.mkdir()
    override_dir.mkdir()

    (repo_dir / "platforms.txt").write_text("Naukri | https://www.naukri.com/ | jobspy | true\n", encoding="utf-8")
    (override_dir / "platforms.txt").write_text(
        "Naukri Mirror | https://www.naukri.com | jobspy | true\n", encoding="utf-8"
    )

    result = load_kind(repo_dir, PLATFORM_SPEC, override_dir=override_dir)
    assert [record.name for record in result.records] == ["Naukri"]
    assert codes(result) == ["duplicate_url"]


def test_missing_override_file_is_not_an_error(tmp_path: Path) -> None:
    repo_dir = tmp_path / "config"
    repo_dir.mkdir()
    (repo_dir / "platforms.txt").write_text("Naukri | https://www.naukri.com/ | jobspy | true\n", encoding="utf-8")

    result = load_kind(repo_dir, PLATFORM_SPEC, override_dir=tmp_path / "does-not-exist")
    assert result.ok
    assert len(result.records) == 1
