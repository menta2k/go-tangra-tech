# Site Build and Validation Quickstart

## Prerequisites

Python 3.12+, Python-Markdown 3.5.2 (see root requirements.txt). No Go-Tangra services or containers are needed to build/read this site.

## Build and check

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build.py
.venv/bin/python scripts/check.py
.venv/bin/python -m unittest discover -s tests -v
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:8000/. Expected: introduction, architecture, complete module directory and separate install methods; links and code copy are usable. Open a module or guide URL directly. Disable JavaScript and repeat navigation. Inspect phone and desktop layouts and keyboard focus/skip navigation. To test subdirectory hosting, serve the repository root and open `/dist/index.html`; relative page links/assets must continue to work.

## Refresh content explicitly

```sh
python3 scripts/import_sources.py --root ../
python3 scripts/build.py
python3 scripts/check.py
```

Review inventory revisions and copied documentation before committing. Do not run import as a prerequisite of ordinary builds or import real deployment secrets.

## Deployment acceptance

For every service, validate Docker and native guides in isolated supported environments against a compatible release matrix, confirm actual health/readiness and module registration, then stop/remove according to the guide. Native dependencies must run without Docker. Record evidence in `validation.md`; source review and static-page checks are not substitutes for these checks. Conduct the reader tasks described in spec.md before claiming SC-001 or SC-004.
