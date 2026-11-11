from __future__ import annotations

import pytest

from careeros.sources.parser import PLATFORM_SPEC, COMPANY_PORTAL_SPEC, parse_source_text
from careeros.sources.registry import (
    STATUS_BLOCKED_OR_RESTRICTED,
    STATUS_DISABLED,
    STATUS_PENDING,
    STATUS_SUPPORTED,
    STATUS_TEMPORARILY_UNAVAILABLE,
    Adapter,
    AdapterRegistry,
    default_registry,
)


def record(line: str = "Naukri | https://www.naukri.com/ | jobspy | true", spec=PLATFORM_SPEC):
    result = parse_source_text(line, spec)
    assert result.ok, result.issues
    return result.records[0]


def healthy_jobspy() -> Adapter:
    return Adapter(
        adapter_id="jobspy",
        display_name="JobSpy",
        kinds=frozenset({"platform"}),
        health=STATUS_SUPPORTED,
    )


def test_register_and_lookup() -> None:
    registry = AdapterRegistry()
    registry.register(healthy_jobspy())
    assert registry.adapter_ids() == ("jobspy",)
    assert registry.get("jobspy").display_name == "JobSpy"
    assert registry.get("missing") is None
    assert registry.get(None) is None


@pytest.mark.parametrize(
    "adapter",
    [
        Adapter("JobSpy", "JobSpy", frozenset({"platform"})),
        Adapter("job-spy", "JobSpy", frozenset({"platform"})),
        Adapter("jobspy", "JobSpy", frozenset()),
        Adapter("jobspy", "JobSpy", frozenset({"platform"}), health="online"),
        Adapter("jobspy", "JobSpy", frozenset({"platform"}), health=STATUS_DISABLED),
    ],
)
def test_invalid_adapters_are_rejected(adapter: Adapter) -> None:
    registry = AdapterRegistry()
    with pytest.raises(ValueError):
        registry.register(adapter)


def test_duplicate_adapter_id_is_rejected() -> None:
    registry = AdapterRegistry()
    registry.register(healthy_jobspy())
    with pytest.raises(ValueError):
        registry.register(healthy_jobspy())


def test_healthy_registered_adapter_makes_source_supported() -> None:
    registry = AdapterRegistry()
    registry.register(healthy_jobspy())
    status = registry.resolve(record())
    assert status.status == STATUS_SUPPORTED
    assert status.scrapeable is True
    assert status.adapter.adapter_id == "jobspy"


def test_unknown_adapter_is_pending_and_not_scrapeable() -> None:
    registry = AdapterRegistry()
    status = registry.resolve(record("Hirist | https://www.hirist.com/ | pending | true"))
    assert status.status == STATUS_PENDING
    assert status.reasons == ("unknown_adapter",)
    assert status.scrapeable is False


def test_disabled_source_is_never_scrapeable() -> None:
    registry = AdapterRegistry()
    registry.register(healthy_jobspy())
    status = registry.resolve(record("Naukri | https://www.naukri.com/ | jobspy | false"))
    assert status.status == STATUS_DISABLED
    assert status.reasons == ("source_disabled",)
    assert status.scrapeable is False
    assert registry.scrapeable([status]) == ()


def test_adapter_kind_mismatch_is_pending() -> None:
    registry = AdapterRegistry()
    registry.register(healthy_jobspy())
    portal = record(
        "Microsoft | https://careers.microsoft.com/ | India+Global | MANGOS | true", COMPANY_PORTAL_SPEC
    )
    portal = portal.__class__(**{**portal.__dict__, "fields": {**portal.fields, "adapter": "jobspy"}})
    status = registry.resolve(portal)
    assert status.status == STATUS_PENDING
    assert status.reasons == ("unsupported_source_kind",)


@pytest.mark.parametrize(
    "health", [STATUS_TEMPORARILY_UNAVAILABLE, STATUS_BLOCKED_OR_RESTRICTED, STATUS_PENDING]
)
def test_unhealthy_adapter_health_is_surfaced(health: str) -> None:
    registry = AdapterRegistry()
    registry.register(Adapter("jobspy", "JobSpy", frozenset({"platform"}), health=health))
    status = registry.resolve(record())
    assert status.status == health
    assert status.scrapeable is False
    assert status.reasons == (f"adapter_{health}",)


def test_source_without_adapter_field_is_pending() -> None:
    registry = AdapterRegistry()
    portal = record(
        "Microsoft | https://careers.microsoft.com/ | India+Global | MANGOS | true", COMPANY_PORTAL_SPEC
    )
    status = registry.resolve(portal)
    assert status.status == STATUS_PENDING
    assert status.reasons == ("adapter_not_assigned",)


def test_resolve_all_summarize_and_scrapeable() -> None:
    registry = AdapterRegistry()
    registry.register(healthy_jobspy())
    result = parse_source_text(
        "Naukri | https://www.naukri.com/ | jobspy | true\n"
        "Hirist | https://www.hirist.com/ | pending | true\n"
        "LinkedIn Jobs | https://www.linkedin.com/jobs/ | jobspy | false\n",
        PLATFORM_SPEC,
    )
    statuses = registry.resolve_all(result.records)
    assert [status.status for status in statuses] == [STATUS_SUPPORTED, STATUS_PENDING, STATUS_DISABLED]
    assert [status.record.name for status in registry.scrapeable(statuses)] == ["Naukri"]
    summary = registry.summarize(statuses)
    assert summary[STATUS_SUPPORTED] == 1
    assert summary[STATUS_PENDING] == 1
    assert summary[STATUS_DISABLED] == 1
    assert summary[STATUS_TEMPORARILY_UNAVAILABLE] == 0


def test_default_registry_does_not_claim_untested_support() -> None:
    registry = default_registry()
    assert registry.adapter_ids() == ("jobspy",)
    status = registry.resolve(record())
    assert status.status == STATUS_PENDING
    assert status.reasons == ("adapter_pending",)
    assert status.scrapeable is False
