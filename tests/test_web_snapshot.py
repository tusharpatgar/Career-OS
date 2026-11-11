from __future__ import annotations

import json
from pathlib import Path

from careeros.sources.parser import PLATFORM_SPEC
from careeros.sources.registry import (
    STATUS_DISABLED,
    STATUS_PENDING,
    STATUS_SUPPORTED,
    Adapter,
    AdapterRegistry,
)
from careeros.web.server import build_snapshot

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "config"


def test_snapshot_of_repository_config_is_complete_and_serializable() -> None:
    snapshot = build_snapshot(CONFIG_DIR)
    json.dumps(snapshot)  # must be JSON serializable for the API

    assert snapshot["total"] > 0
    assert snapshot["issues"] == []
    assert set(snapshot["kinds"]) == {"platform", "company_portal", "recruitment"}
    for kind in snapshot["kinds"].values():
        assert kind["record_count"] == len(kind["records"])
        assert kind["format"]
        assert kind["filename"].endswith(".txt")

    assert snapshot["summary"][STATUS_SUPPORTED] == 0, "no adapter is tested yet"
    assert snapshot["summary"][STATUS_PENDING] > 0
    assert snapshot["summary"][STATUS_DISABLED] > 0
    assert sum(snapshot["summary"].values()) == snapshot["total"]


def test_snapshot_reports_record_details_and_adapters() -> None:
    snapshot = build_snapshot(CONFIG_DIR)
    platform = snapshot["kinds"]["platform"]
    naukri = next(record for record in platform["records"] if record["name"] == "Naukri")

    assert naukri["enabled"] is True
    assert naukri["adapter"] == "jobspy"
    assert naukri["raw_status"] == STATUS_PENDING
    assert naukri["reasons"] == ["adapter_pending"]
    assert naukri["url"].startswith("https://")
    assert naukri["filename"] == PLATFORM_SPEC.filename
    assert naukri["line"] > 0

    portal = next(record for record in snapshot["kinds"]["company_portal"]["records"] if record["name"] == "Google")
    assert portal["details"]["market"] == "India+Global"
    assert portal["details"]["category"] == "MANGOS"
    assert portal["reasons"] == ["adapter_not_assigned"]

    consultancy = snapshot["kinds"]["recruitment"]["records"][0]
    assert consultancy["details"]["specialization"]
    assert consultancy["details"]["geography"]

    assert snapshot["adapters"] == [
        {
            "adapter_id": "jobspy",
            "display_name": "JobSpy",
            "kinds": ["platform"],
            "health": STATUS_PENDING,
            "health_label": "Pending",
            "notes": "Adapter not implemented yet; see the JobSpy audit (COS-001).",
        }
    ]


def test_snapshot_surfaces_invalid_rows_instead_of_dropping_them(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "platforms.txt").write_text(
        "Naukri | https://www.naukri.com/ | jobspy | true\n"
        "Broken row without pipes\n"
        "Evil | javascript:alert(1) | jobspy | true\n",
        encoding="utf-8",
    )
    (config_dir / "companyportals.txt").write_text("# no portals in this fixture\n", encoding="utf-8")
    (config_dir / "recruitment_sources.txt").write_text("# no consultancies in this fixture\n", encoding="utf-8")

    snapshot = build_snapshot(config_dir)

    assert snapshot["total"] == 1
    assert [issue["code"] for issue in snapshot["issues"]] == ["wrong_field_count", "invalid_url"]
    assert snapshot["issues"][0]["line"] == 2
    assert snapshot["issues"][0]["raw"] == "Broken row without pipes"


def test_snapshot_marks_healthy_adapters_as_supported(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "platforms.txt").write_text(
        "Naukri | https://www.naukri.com/ | jobspy | true\n"
        "Hirist | https://www.hirist.com/ | pending | true\n",
        encoding="utf-8",
    )

    registry = AdapterRegistry()
    registry.register(
        Adapter("jobspy", "JobSpy", frozenset({"platform"}), health=STATUS_SUPPORTED, notes="tested")
    )

    snapshot = build_snapshot(config_dir, registry=registry)

    statuses = {record["name"]: record["raw_status"] for record in snapshot["kinds"]["platform"]["records"]}
    assert statuses == {"Naukri": STATUS_SUPPORTED, "Hirist": STATUS_PENDING}
    assert snapshot["summary"][STATUS_SUPPORTED] == 1


def test_snapshot_honours_override_layer(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    override_dir = tmp_path / "overrides"
    config_dir.mkdir()
    override_dir.mkdir()
    (config_dir / "platforms.txt").write_text(
        "Naukri | https://www.naukri.com/ | jobspy | true\n", encoding="utf-8"
    )
    (override_dir / "platforms.txt").write_text(
        "Naukri | https://www.naukri.com/ | jobspy | false\n", encoding="utf-8"
    )

    snapshot = build_snapshot(config_dir, override_dir=override_dir)

    record = snapshot["kinds"]["platform"]["records"][0]
    assert snapshot["override_dir"] == str(override_dir)
    assert record["origin"] == "override"
    assert record["enabled"] is False
    assert record["raw_status"] == STATUS_DISABLED
