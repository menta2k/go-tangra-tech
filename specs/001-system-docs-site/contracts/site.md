# Static Site Interface and Content Contract

## Routes

- `index.html`: system introduction and getting-started links.
- `getting-started.html`: choose component and install method.
- `architecture/index.html`: complete architecture overview and workflows.
- `architecture/security.html`, `configuration.html`, `frontend.html`, `dependencies.html`: detailed platform references.
- `modules/index.html`: full inventory grouped by responsibility.
- `modules/<id>.html`: module reference including sources, related references and guides.
- `how-to/index.html`: installation directory.
- `how-to/<id>/docker.html` and `native.html`: installable-module procedures.
- `sources/<id>/<path>.html`: readable, cited snapshot documentation.
- `404.html`: missing-page explanation and documentation links.
- `assets/site.css`, `assets/site.js`, `assets/search.json`: local resources.

All links are relative to the current output page; the site works under a hosting subdirectory. Hosts configure `404.html` as their missing-page response. No redirect/router server is required.

## Build/import CLI

`python3 scripts/import_sources.py --root <sibling-repositories>` refreshes selected snapshots and inventory explicitly. It fails for missing required repositories or source files. Ordinary builds never inspect sibling checkouts.

`python3 scripts/build.py` reads checked-in content and assets, validates inventory, emits `dist/` deterministically and removes stale generated pages. Fail on malformed content or duplicate routes.

`python3 scripts/check.py` checks every internal link, resource, fragment, heading-id uniqueness, source hash, and pair of installation routes. Exit nonzero for any violation.

## User interactions

Global links, sidebar links, headings and local TOC work without JS. Enhancements: search across page titles/section headings using a local index, code copy with accessible status, a collapsible narrow-screen menu. Enhancement failures leave reading intact. Search results use text nodes, not untrusted HTML.

## Guide contract

Each installable module has Docker/native procedures covering environment/version, prerequisites, required and optional dependencies, obtaining/building, configuration and identity/policy, bootstrap/start, success verification, diagnostics, stop/removal and data effects. Every command must distinguish documented upstream behavior from a site-authored adaptation. Native instructions do not invoke Docker for infrastructure. Unsupported/unverified environment acceptance remains recorded in `validation.md`.

## Standalone installation downloads

Each of the 17 service ids has downloads/<id>.zip and downloads/<id>/<file> routes. Archives contain a single <id>/ root with compose.yaml, .env.example, README.md, reviewed public configuration/policies and bootstrap assets. bundle.json is the source packaging allowlist; missing or changed reviewed files fail builds. Runtime .env, keys and state are excluded. Docker guides use docker compose for lifecycle and a private namespace check profile for health/readiness. Asterisk requires an external read-only PBX DSN. Normal builds package checked-in bundles without reading sibling repositories.

## Existing-core installation contract (supersedes standalone core inclusion)

For 14 regular modules, bundle.json mode is existing-core; applications contains only the selected module. The mesh network is external and supplied by CORE_NETWORK. No Auth/Portal/LCM, peer-module installation or token-minting job is present. configure.py renders reviewed templates using private .env inputs and externally supplied token/public CA files into runtime/config.yaml and runtime/policy.yaml. Those generated files and private/ inputs are excluded from downloads and version control. Three core bundles use mode core-bootstrap and explain their initial-installation scope. Docker guides document Auth token issuance, LCM exchange, Gateway allow-list updates, reciprocal service policies, persisted identity and registration verification against the running core.

## Remote-core topology correction — 2026-10-07

Default add-on Compose deployment must work without a shared Docker network: the existing core may run on a different host. Configure routable core endpoints and private host port publication, set FREYA_ADVERTISE_HOST through MODULE_ADVERTISE_HOST, and preserve published/listener port numbers for accurate registration. Require bidirectional connectivity and mesh mTLS; keep admin listeners unpublished. CORE_NETWORK is only used by optional compose.same-host.yaml with .env.same-host.example when both use the same Docker daemon. Enrollment material is obtained on the core host and transferred privately to the module host. This supersedes the previous external-network default.
