# Go-Tangra documentation site

A static introduction, architecture reference, module directory and installation documentation for the Go-Tangra v4 platform. The first implementation contains 18 component references, 34 Docker/native guides and 62 source documentation snapshots.

## Build and read

Requires Python 3.12+ and the dependencies in `requirements.txt`. No Go-Tangra services, Docker, Node packages or sibling checkouts are needed for an ordinary build.

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
make PYTHON=.venv/bin/python test
make PYTHON=.venv/bin/python serve
```

Open `http://127.0.0.1:8000/`. You can also open `dist/index.html` directly to read and navigate; browser search needs an HTTP origin to load its local index. The documentation remains readable without JavaScript.

With dependencies already installed, use `make test` and `make serve`. `make build` writes `dist/`; `make check` builds and validates internal links, fragments, assets, source hashes and the two installation methods for every service.

## Content and maintenance

- `content/pages/`: curated introduction, architecture and onboarding material.
- `content/permissions.json` and `content/permissions/`: permission catalogues and public manifest snapshots at recorded revisions.
- `content/modules/`: module references with source-derived configuration and API indexes.
- `content/guides/`: module-specific Docker and native procedures.
- `content/sources/`: selected upstream Markdown snapshots.
- `content/modules.json`: component identities, exact revisions, local tags and snapshot hashes.
- `assets/`: local CSS and optional search/code-copy enhancements.
- `deploy/compose/<module>/`: 14 module Compose bundles that enroll into an existing core, plus 3 clearly marked initial-core bootstrap bundles. Module bundles include local infrastructure and connect to your existing core over a private routed network/VPN.
- `scripts/`: explicit importing, reference/guide generation, deterministic build and integrity checks.

To deliberately refresh sources from the sibling v4 repositories:

```sh
python3 scripts/import_sources.py --root ..
python3 scripts/import_permissions.py --root ..
python3 scripts/create_compose.py --root ..
python3 scripts/write_module_content.py
make test
```

The content generator rewrites the module references and guides. Review its output before committing, especially configuration adaptation, dependency classification, build flags, image availability and module-specific exceptions. Source imports are explicit; normal builds never read sibling repositories. Do not import real deployment configuration, secrets or private key files.

## Install a module into an existing core

From `deploy/compose/<module>/`:

```sh
cp .env.example .env
# Set routable core endpoints, module advertised host/private bind IP, trust domain and image version.
# Supply a fresh Auth-signed enrollment token and the public mesh CA bundle.
python3 configure.py
docker compose config --quiet
docker compose pull
docker compose up -d
docker compose --profile checks run --rm check
```

Regular module bundles run only the selected module and local infrastructure. They use your existing Auth/Portal/LCM, routable core endpoints and a freshly supplied enrollment token; no core bootstrap or token-minting job runs locally. Auth, Portal and LCM bundles are initial-core bootstrap examples, not add-on installation procedures. Asterisk additionally needs a read-only external PBX CDR DSN; its module-owned registration database is included. The default supports a core on a different host: mesh ports bind MODULE_BIND_IP and FREYA_ADVERTISE_HOST announces MODULE_ADVERTISE_HOST. An optional compose.same-host.yaml/.env.same-host.example pair supports a core on the same Docker daemon through CORE_NETWORK. Docker bridge networks do not connect separate hosts. The manifests are workstation configurations; external providers, hardware and production setup remain deployment-specific.

Where a bundle includes `keys-init`, Compose automatically runs its bundled `init-keys.sh` to create missing application keys in private persistent volumes. Each affected Docker guide and bundle README lists the exact key files, container paths, verification commands and backup/restore requirements. Existing nonempty keys are retained; this initializer is not a rotation tool.

The site build publishes 17 ZIP downloads and raw bundle files under `dist/downloads/`. It packages only files listed in each bundle's reviewed hash manifest. Private `.env` files, generated keys and runtime state are never included; unexpected changes to reviewed bundle files fail the build. Use `make compose-bundles` for explicit source-based regeneration; ordinary builds use the checked-in bundles.

## Hosting

Upload the contents of `dist/` to your chosen static host. Relative links support a hosting subdirectory. Configure that host to return `404.html` for missing pages. No application backend, runtime package installation, CDN or Go-Tangra deployment is required. Hosting has not been configured or published by this implementation.

## Implementation and validation status

The [plan](specs/001-system-docs-site/plan.md), [tasks](specs/001-system-docs-site/tasks.md) and [validation evidence](specs/001-system-docs-site/validation.md) record progress. The source snapshots are v4 documentation at recorded commits; they are not a tested unified release matrix.

Static integrity checks and the 26-test suite pass. Clean Docker/native deployment acceptance, browser/HTTP inspection and the reader studies remain pending. The execution sandbox prevents opening a local listening socket, launching Chromium's required sockets and accessing the Docker daemon. Installation guides are source-reviewed procedures, not claimed results of live deployments.

Optional browser checks are in `tests/browser.cjs`. In an unrestricted development environment with `playwright` and `@axe-core/playwright` installed, run:

```sh
TANGRA_BROWSER_EXECUTABLE=/path/to/chrome node tests/browser.cjs
```

If those packages are installed elsewhere, set `TANGRA_BROWSER_MODULE_ROOT` to their `node_modules` directory. The runner intercepts a local test origin and serves the built files without opening an HTTP port; it checks responsive overflow, key navigation, no-JavaScript reading, search and WCAG rules. Screenshots/reports go to a temporary directory; actual module deployments are never started by this test.

## Continuous integration

GitHub Actions runs `make test` on every push, pull request and manual run with Python 3.12. A successful run publishes the complete built site as `documentation-site`, all module ZIPs as `all-module-bundles`, and a separate `compose-<module>` artifact for every checked-in bundle (including the initial-core bundles). Artifacts are retained for 30 days and are available from the workflow run's **Artifacts** section.

The artifact matrix is discovered from `deploy/compose/*/bundle.json`. CI fails if any bundle ZIP is missing or unexpected, and new bundles are included automatically. Packaging uses the reviewed manifests and existing integrity tests.

## Releases

Push a version tag such as `v1.0.0` to publish the module bundles as GitHub Release assets. The release workflow builds and validates the project, verifies that all checked-in bundles have ZIPs, then attaches every module ZIP to the release. New releases remain drafts until all assets have uploaded successfully. Re-running a release replaces its assets with the validated bundles from the same tag.

```sh
git tag v1.0.0
git push origin v1.0.0
```
