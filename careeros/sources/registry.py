"""Adapter registry and source health resolution.

A configured source is not scraper support. Every record resolves to a visible
status; only records whose adapter is registered, kind-compatible and healthy
are returned as scrapeable.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from .parser import SourceRecord

STATUS_SUPPORTED = "supported"
STATUS_PENDING = "pending"
STATUS_DISABLED = "disabled"
STATUS_TEMPORARILY_UNAVAILABLE = "temporarily_unavailable"
STATUS_BLOCKED_OR_RESTRICTED = "blocked_or_restricted"

STATUSES: tuple[str, ...] = (
    STATUS_SUPPORTED,
    STATUS_PENDING,
    STATUS_DISABLED,
    STATUS_TEMPORARILY_UNAVAILABLE,
    STATUS_BLOCKED_OR_RESTRICTED,
)

_ADAPTER_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]{0,39}$")


@dataclass(frozen=True)
class Adapter:
    adapter_id: str
    display_name: str
    kinds: frozenset[str]
    health: str = STATUS_PENDING
    notes: str = ""


@dataclass(frozen=True)
class SourceStatus:
    record: SourceRecord
    status: str
    adapter: Adapter | None = None
    reasons: tuple[str, ...] = ()

    @property
    def scrapeable(self) -> bool:
        return self.status == STATUS_SUPPORTED


class AdapterRegistry:
    """Holds adapters by ID and resolves configured sources to health states."""

    def __init__(self) -> None:
        self._adapters: dict[str, Adapter] = {}

    def register(self, adapter: Adapter) -> None:
        if not _ADAPTER_ID_PATTERN.match(adapter.adapter_id):
            raise ValueError(
                f"adapter ID {adapter.adapter_id!r} must be lowercase letters, digits or underscores "
                "and start with a letter"
            )
        if adapter.health not in STATUSES or adapter.health == STATUS_DISABLED:
            raise ValueError(
                f"adapter health {adapter.health!r} is not a valid adapter health state; "
                f"choose from {', '.join(s for s in STATUSES if s != STATUS_DISABLED)}"
            )
        if not adapter.kinds:
            raise ValueError(f"adapter {adapter.adapter_id!r} must declare at least one source kind")
        if adapter.adapter_id in self._adapters:
            raise ValueError(f"adapter {adapter.adapter_id!r} is already registered")
        self._adapters[adapter.adapter_id] = adapter

    def get(self, adapter_id: str | None) -> Adapter | None:
        if not adapter_id:
            return None
        return self._adapters.get(adapter_id)

    def adapter_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._adapters))

    def resolve(self, record: SourceRecord) -> SourceStatus:
        if not record.enabled:
            return SourceStatus(record, STATUS_DISABLED, reasons=("source_disabled",))

        if record.adapter_id is None:
            return SourceStatus(record, STATUS_PENDING, reasons=("adapter_not_assigned",))

        adapter = self.get(record.adapter_id)
        if adapter is None:
            return SourceStatus(record, STATUS_PENDING, reasons=("unknown_adapter",))

        if record.kind not in adapter.kinds:
            return SourceStatus(
                record,
                STATUS_PENDING,
                adapter=adapter,
                reasons=("unsupported_source_kind",),
            )

        if adapter.health != STATUS_SUPPORTED:
            return SourceStatus(
                record,
                adapter.health,
                adapter=adapter,
                reasons=(f"adapter_{adapter.health}",),
            )

        return SourceStatus(record, STATUS_SUPPORTED, adapter=adapter, reasons=("adapter_healthy",))

    def resolve_all(self, records: Iterable[SourceRecord]) -> tuple[SourceStatus, ...]:
        return tuple(self.resolve(record) for record in records)

    @staticmethod
    def scrapeable(statuses: Iterable[SourceStatus]) -> tuple[SourceStatus, ...]:
        return tuple(status for status in statuses if status.scrapeable)

    @staticmethod
    def summarize(statuses: Iterable[SourceStatus]) -> dict[str, int]:
        summary = {status: 0 for status in STATUSES}
        for item in statuses:
            summary[item.status] += 1
        return summary


def default_registry() -> AdapterRegistry:
    """Registry for the current milestone.

    JobSpy is registered but explicitly pending: no adapter code has been
    implemented or tested yet, so no configured source may be reported as
    supported.
    """
    registry = AdapterRegistry()
    registry.register(
        Adapter(
            adapter_id="jobspy",
            display_name="JobSpy",
            kinds=frozenset({"platform"}),
            health=STATUS_PENDING,
            notes="Adapter not implemented yet; see the JobSpy audit (COS-001).",
        )
    )
    return registry
