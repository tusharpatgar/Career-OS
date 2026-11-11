"""Career OS desktop-style web GUI, standard library only.

Serves a single-page dashboard plus a read-only JSON snapshot of the parsed
source configuration. Configuration is re-read on every snapshot request, so
editing config/*.txt and refreshing the page is enough to see the change.

Run:  python3 -m careeros.web.server --port 8000
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import sys
import traceback
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import unquote, urlparse

from ..sources.loader import load_all
from ..sources.parser import SPECS
from ..sources.registry import STATUSES, AdapterRegistry, default_registry

WEB_ROOT = Path(__file__).resolve().parent
STATIC_DIR = WEB_ROOT / "static"
REPO_ROOT = WEB_ROOT.parents[1]
DEFAULT_CONFIG_DIR = REPO_ROOT / "config"

KIND_LABELS = {
    "platform": "Job platforms",
    "company_portal": "Company career portals",
    "recruitment": "Consultancies & staffing",
}

STATUS_LABELS = {
    "supported": "Supported",
    "pending": "Pending",
    "disabled": "Disabled",
    "temporarily_unavailable": "Temporarily unavailable",
    "blocked_or_restricted": "Blocked or restricted",
}


def _status_payload(status) -> dict[str, Any]:
    record = status.record
    details = {
        key: value
        for key, value in record.fields.items()
        if key not in {"name", "url", "enabled", "adapter"}
    }
    return {
        "name": record.name,
        "url": record.url,
        "enabled": record.enabled,
        "origin": record.origin,
        "line": record.line,
        "filename": record.filename,
        "status": record_status_label(status.status),
        "raw_status": status.status,
        "reasons": list(status.reasons),
        "adapter": status.adapter.adapter_id if status.adapter else record.adapter_id,
        "adapter_health": status.adapter.health if status.adapter else None,
        "details": details,
    }


def record_status_label(status: str) -> str:
    return STATUS_LABELS.get(status, status)


def _adapter_payload(registry: AdapterRegistry) -> list[dict[str, Any]]:
    payload = []
    for adapter_id in registry.adapter_ids():
        adapter = registry.get(adapter_id)
        if adapter is None:  # pragma: no cover - defensive
            continue
        payload.append(
            {
                "adapter_id": adapter.adapter_id,
                "display_name": adapter.display_name,
                "kinds": sorted(adapter.kinds),
                "health": adapter.health,
                "health_label": record_status_label(adapter.health),
                "notes": adapter.notes,
            }
        )
    return payload


def build_snapshot(
    config_dir: str | Path = DEFAULT_CONFIG_DIR,
    override_dir: str | Path | None = None,
    registry: AdapterRegistry | None = None,
) -> dict[str, Any]:
    """Build the read-only JSON snapshot consumed by the GUI."""
    config_dir = Path(config_dir)
    registry = registry or default_registry()
    results = load_all(config_dir, override_dir=override_dir)
    issues = [result.issues for result in results.values()]

    summary = {status: 0 for status in STATUSES}
    kinds: dict[str, Any] = {}
    total = 0

    for spec in SPECS:
        result = results[spec.kind]
        statuses = registry.resolve_all(result.records)
        for status in statuses:
            summary[status.status] += 1
        total += len(statuses)
        kinds[spec.kind] = {
            "kind": spec.kind,
            "label": KIND_LABELS.get(spec.kind, spec.kind),
            "filename": spec.filename,
            "format": spec.summary,
            "records": [_status_payload(status) for status in statuses],
            "record_count": len(statuses),
            "issue_count": len(result.issues),
        }

    issue_payload = [
        {
            "code": issue.code,
            "message": issue.message,
            "filename": issue.filename,
            "line": issue.line,
            "raw": issue.raw,
        }
        for group in issues
        for issue in group
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "config_dir": str(config_dir),
        "override_dir": str(override_dir) if override_dir else None,
        "total": total,
        "summary": summary,
        "statuses": list(STATUSES),
        "status_labels": STATUS_LABELS,
        "kinds": kinds,
        "issues": issue_payload,
        "adapters": _adapter_payload(registry),
    }


class CareerOSHandler(BaseHTTPRequestHandler):
    server_version = "CareerOS/0.1"
    config_dir: Path = DEFAULT_CONFIG_DIR
    override_dir: Path | None = None
    registry_factory = staticmethod(default_registry)

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        path = unquote(urlparse(self.path).path)
        if path in ("/", "/index.html"):
            self._send_file(STATIC_DIR / "index.html")
            return
        if path == "/api/health":
            self._send_json({"status": "ok"})
            return
        if path == "/api/snapshot":
            try:
                snapshot = build_snapshot(
                    self.config_dir, self.override_dir, registry=self.registry_factory()
                )
            except Exception as exc:  # surfaced to the UI instead of dying silently
                traceback.print_exc()
                self._send_json(
                    {"error": "snapshot_failed", "message": str(exc)}, status=HTTPStatus.INTERNAL_SERVER_ERROR
                )
                return
            self._send_json(snapshot)
            return
        if path.startswith("/static/"):
            self._send_file((STATIC_DIR / path[len("/static/") :]).resolve())
            return
        self._send_json(
            {"error": "not_found", "message": f"no route for {path}"}, status=HTTPStatus.NOT_FOUND
        )

    def _send_json(self, payload: Mapping[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path) -> None:
        try:
            path = path.resolve()
            path.relative_to(STATIC_DIR.resolve())
        except (ValueError, OSError):
            self._send_json(
                {"error": "not_found", "message": "file is outside the static root"},
                status=HTTPStatus.NOT_FOUND,
            )
            return
        if not path.is_file():
            self._send_json(
                {"error": "not_found", "message": f"missing file {path.name}"},
                status=HTTPStatus.NOT_FOUND,
            )
            return

        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if content_type.startswith("text/") or content_type in {"application/javascript", "application/json"}:
            content_type = f"{content_type}; charset=utf-8"
        body = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        sys.stderr.write(f"[careeros] {self.address_string()} {format % args}\n")


def make_handler(
    config_dir: str | Path = DEFAULT_CONFIG_DIR,
    override_dir: str | Path | None = None,
    registry_factory=default_registry,
):
    """Return a handler class bound to the given configuration directories."""

    class BoundHandler(CareerOSHandler):
        pass

    BoundHandler.config_dir = Path(config_dir)
    BoundHandler.override_dir = Path(override_dir) if override_dir else None
    BoundHandler.registry_factory = staticmethod(registry_factory)
    return BoundHandler


def serve(
    host: str = "0.0.0.0",
    port: int = 8000,
    config_dir: str | Path = DEFAULT_CONFIG_DIR,
    override_dir: str | Path | None = None,
) -> None:
    handler = make_handler(config_dir, override_dir)
    httpd = ThreadingHTTPServer((host, port), handler)
    httpd.daemon_threads = True
    print(f"Career OS GUI on http://{host}:{port} (config: {config_dir})", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Career OS GUI", file=sys.stderr)
    finally:
        httpd.server_close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Career OS source configuration GUI")
    parser.add_argument("--host", default="0.0.0.0", help="bind address (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="port (default: 8000)")
    parser.add_argument(
        "--config-dir",
        default=str(DEFAULT_CONFIG_DIR),
        help="directory holding platforms.txt, companyportals.txt and recruitment_sources.txt",
    )
    parser.add_argument(
        "--override-dir",
        default=None,
        help="optional user override directory layered over the shared defaults",
    )
    args = parser.parse_args(argv)
    serve(args.host, args.port, args.config_dir, args.override_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
