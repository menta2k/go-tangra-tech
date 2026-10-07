# Implementation Validation Evidence

**Recorded**: 2026-10-05
**Status**: Working static implementation; release acceptance remains pending.

## Completed checks

- `make test`: successful static build of **125 HTML pages**, integrity checks and **10 passing tests**.
- `python3 scripts/check.py`: all internal page/resource links and fragments resolve; every page has exactly one main/title/h1 and English language metadata; no duplicate ids or root-relative asset links.
- Provenance: **18 v4 components**, **62 source Markdown snapshots**, exact source commits and SHA-256 hashes; hash checks pass. The source files inspected during import were clean in their original repositories.
- Per-module indexes: **1013 configuration fields** and **738 API operations** extracted from public configuration structures and OpenAPI contracts. These indexes supplement detailed copied upstream references, not inferred configuration defaults.
- Coverage: all **17 independently installable services** have distinct Docker/native pages (**34 guides**); the framework, SDKs, UI kit and contrib modules are documented as consumed packages.
- Native command checks: none of the native guide shell blocks invokes Docker/Compose dependency setup.
- `node --check assets/site.js` and `node --check tests/browser.cjs`: passed.
- `python3 -m compileall -q scripts tests`: passed.
- Deterministic rebuild: 129 generated files had identical SHA-256 digests across consecutive unchanged builds. The later narrow-screen TOC addition is included in the final successful build.
- Homepage plus shared CSS/JS/favicon: **24,452 bytes**, below the plan's 150 KB uncompressed budget.

## Tests exercised

The suite detects broken fragment/resource links, duplicate heading ids, root-relative paths, unsafe link schemes, missing guide pairs, source hash changes and framework/service deployment confusion. It also checks deep relative routes, escaped titles, upstream source-link rewriting and the known base-stack exceptions.

## Environment restrictions and pending checks

| Task | Status | Evidence / remaining work |
| --- | --- | --- |
| T016 — clean Docker/native installation acceptance | Pending | `docker version` reports client 29.1.3 but Docker daemon access is denied at `/var/run/docker.sock`. No module or infrastructure deployment was started. Validate every guide in isolated supported environments. |
| T018 — HTTP smoke portion | Pending; static/test portions pass | `python3 -m http.server 8000 --bind 127.0.0.1 --directory dist` fails creating a listening socket with `PermissionError: Operation not permitted`. Run HTTP/subdirectory smoke checks outside this sandbox. |
| T019 — browser, accessibility and interaction inspection | Pending | Chromium launch through Playwright fails at `setsockopt: Operation not permitted` and exits before any page inspection. No screenshot, axe result, keyboard, search or responsive-runtime pass is claimed. Reusable scenarios are in `tests/browser.cjs`. |
| T020 — compatible published release matrix | Pending | Local tags and source commits are recorded. Registry artifact publication and cross-service combinations were not verified. |
| T021 — representative reader studies | Pending | No five-reader discovery/workflow study has occurred. |

## Specification outcomes

- SC-001 / SC-004: reader success rates and timings require the pending study.
- SC-002: inventory and reference coverage are implemented; content completeness/defaults and feature support need maintainer review before release approval.
- SC-003: guide pair coverage is implemented; clean-environment success is unverified.
- SC-005: internal link integrity passes. Reference and install directories place module/guide destinations within three navigation selections of the homepage.
- SC-006: semantic landmarks, keyboard-oriented navigation/focus/skip link, local diagram descriptions and responsive styles are implemented; actual browser/assistive-technology acceptance is pending.
- SC-007: source provenance is present. A tested supported release matrix and resolution of remaining deployment/content gaps are still release gates.

## Hooks and scope

No extension hooks are configured, so before/after plan, tasks and implementation hook stages are skipped. Website hosting and real infrastructure changes were not part of this implementation. This repository lacks usable Git metadata, so no branch, commit or PR was created.

## Standalone Compose validation — 2026-10-06

- make test passes: 125 HTML pages, all link/source/guide checks, 17 bundle integrity checks and 19 tests.
- python3 scripts/check_compose.py --docker passes for all 17 bundles. The Asterisk parser check supplies a fixture DSN solely to validate syntax; no external database connection is attempted.
- Shell syntax checks and Python compilation pass. Bootstrap fixture tests verify persistent key generation and Vault recovery-material parsing without printing secrets.
- ZIP contents match reviewed hash manifests; tests reject path traversal and modified files and prove private .env files are excluded. Dependency graphs, mounts, persistent storage, enrollment trust and private health probes pass static checks.
- Docker guides now describe standalone Compose installation with downloadable bundles and module-specific external integration steps. These are workstation configurations; published image availability and actual module startup remain unverified under T016/T020.

## Permission documentation validation — 2026-10-06

All 148 declared permissions from 16 module manifests are documented. Platform and Portal references explain why they have no independent user permission catalogue. Source snapshots are read with git show at the inventory revisions and stored with SHA-256 hashes. Each permission includes its description, declared UI actions/navigation and matching imported OpenAPI operations; missing operation annotations are explicitly identified rather than inferred. The security reference covers qualified permission assignment, group roles, resource grants, tenant boundaries and verification. make test passes all 22 tests and all 125 generated pages pass link/content checks. Live authorization testing remains part of pending deployment acceptance.

## Existing-core enrollment correction — 2026-10-07

14 regular-module bundles now run only the chosen application plus local infrastructure, connect through an existing external mesh network and consume externally supplied enrollment tokens and public CA bundles. Auth/Portal/LCM bundles are explicitly scoped to initial core bootstrap. Guides use existing Auth token issuance, LCM redemption, Gateway allow-list registration and peer-policy configuration. Source provenance includes the recorded Auth token and Gateway bootstrap CLI implementations.

make test passes all 26 tests, all 125 HTML pages, guide/link/source checks and all 17 bundle integrity checks. Docker Compose parses all manifests without starting containers. New fixtures render all 14 add-ons with alternate trust domains, core DNS/ports and issuer URLs, check CA verification/pinned identity and private runtime modes, reject missing credentials/unsafe interpolation, and prove the application/network scope excludes a second core. Published image compatibility and real enrollment/renewal/registration remain unverified; T016/T020 still require a running supported core.

## Key initializer documentation — 2026-10-07

Documented init-keys.sh in every affected Docker guide and downloadable bundle README, with per-bundle volume/file mappings derived from its actual Compose mounts. Covers automatic one-shot execution, random/base64 generation, preserved existing keys, file modes, exit/log checks, enrollment distinction and matching backup/restore. The implementation and key-generation behavior are unchanged. Regenerated downloads pass the existing 26-test suite and all site/bundle checks.

## Remote-core topology — 2026-10-07

The default 14 module bundles no longer require an external Docker network. They use routable core endpoints, MODULE_BIND_IP for private-interface port publication, and MODULE_ADVERTISE_HOST/FREYA_ADVERTISE_HOST for reachable registration. Tests check unchanged internal/published mesh ports and no external network in the default. Compose CLI also validates each of the 14 same-host overlay combinations using its separate environment example. All 26 tests and site/bundle checks pass. Cross-host enrollment, routing, mTLS and registered-endpoint reachability remain unverified in a live environment.
