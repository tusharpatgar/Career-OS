# Running Career OS locally

Python 3.11+ is required. The runtime has no third-party dependencies; pytest is needed only for the test suite.

## GUI

```bash
python3 -m careeros.web.server --host 0.0.0.0 --port 8000
```

Open http://localhost:8000. Options:

| Flag | Purpose |
|---|---|
| `--host` | bind address (default `0.0.0.0`) |
| `--port` | port (default `8000`) |
| `--config-dir` | directory holding the three source files (default `./config`) |
| `--override-dir` | optional user override directory layered over the defaults |

Configuration is re-read on every snapshot request, so editing `config/*.txt` and pressing **Refresh** in the GUI is enough to see the change. The server is read-only: it never writes configuration.

### API

| Route | Response |
|---|---|
| `GET /` | dashboard page |
| `GET /api/health` | `{"status": "ok"}` |
| `GET /api/snapshot` | full snapshot: counts, resolved statuses per source with file/line provenance, validation issues, registered adapters |

## Tests

```bash
python3 -m pip install --target .deps --break-system-packages pytest
PYTHONPATH=.deps python3 -m pytest -q
```

`.deps/` is git-ignored; a virtualenv works equally well:

```bash
python3 -m venv .venv && .venv/bin/pip install pytest && .venv/bin/python -m pytest -q
```

## Using the parser from code

```python
from careeros.sources import load_all, default_registry

results = load_all("config", override_dir=None)
registry = default_registry()

for result in results.values():
    for issue in result.issues:
        print(issue)  # file:line: code: message
    for status in registry.resolve_all(result.records):
        print(status.record.name, status.status, status.reasons)
```

Only `status.scrapeable` records (status `supported`) may be handed to a scraper; everything else must stay visible as pending, disabled, unavailable or blocked.
