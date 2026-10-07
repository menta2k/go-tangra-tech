# Implementation Plan: Go-Tangra System Documentation Site

**Branch**: No Git metadata available in this workspace | **Date**: 2026-10-05 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-system-docs-site/spec.md`

## Summary

Build a portable static documentation site introducing Go-Tangra v4, its complete verified component inventory, detailed architecture and module references, and separate Docker/native how-tos. Use a small Python build tool, Markdown content, a checked-in source inventory, and shared HTML/CSS with optional progressive JavaScript. Import selected authoritative documentation from sibling repositories into versioned snapshots so ordinary builds are self-contained. Do not deploy the website or start real infrastructure as part of this implementation.

## Technical Context

**Language/Version**: Python 3.12 build tooling; HTML5, CSS, browser JavaScript.

**Primary Dependencies**: Python-Markdown 3.5.2 (available locally), with bundled fenced-code, tables, and TOC extensions. No runtime dependencies or CDN assets.

**Storage**: Checked-in Markdown and JSON; generated `dist/` output.

**Testing**: Python unittest for route/fragment integrity, source provenance, escaping and content contract checks; Node syntax checking; local HTTP smoke checks; Chromium desktop/mobile/no-JavaScript inspection where available.

**Target Platform**: Any static HTTP host, including subdirectory hosting, current desktop/mobile browsers. Linux workstation for native module examples.

**Project Type**: Static documentation website with build/import CLI.

**Performance Goals**: Local assets only; homepage and shared assets under 150 KB uncompressed; readers reach module references and guides within three navigation selections.

**Constraints**: Readable without JavaScript; no site-specific application server; no real secrets; imports limited to explicitly selected public documentation and source references. Native guides must not use Docker for their dependencies. Never claim local tags prove published artifacts exist.

**Scale/Scope**: 18 verified v4 components (framework plus 17 services), shared framework/contrib/UI references, source documentation snapshots, architecture workflows, 34 service installation paths and platform consumption instructions.

## Constitution Check

The project's constitution is an unfilled template, so there are no adopted project-specific gates. Pre-research gate passes: plan preserves explicit static delivery, both install methods, accuracy, and accessibility requirements. Post-design gate passes: no runtime backend, factual documentation is sourced, and unresolved deployment acceptance is tracked separately from successful site builds. No extension hooks are configured.

## Project Structure

### Documentation (this feature)

```text
specs/001-system-docs-site/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/site.md
├── tasks.md
└── validation.md
```

### Source Code (repository root)

```text
content/
├── modules.json
├── pages/                 # curated introduction, architecture, how-to landing pages
├── modules/               # source-derived module references
├── guides/                # Docker/native installation pages
└── sources/               # selected source Markdown snapshots
assets/
├── site.css
└── site.js
scripts/
├── import_sources.py
├── build.py
└── check.py
tests/test_site.py
requirements.txt
Makefile
README.md
dist/                      # generated output, ignored
```

**Structure Decision**: One static project. Snapshot importing is explicit and separate from deterministic website builds. An inventory associates service names, build commands, source revisions, dependency classifications and routes. Browser enhancement is optional, preserving plain HTML links and page reading.

## Delivery Sequence

1. Record source evidence and select the v4 checkout of each component.
2. Define content/route contracts, snapshot sources and implement build/link validation.
3. Implement the visual shell, introduction, getting-started and module directory.
4. Add architecture/security/configuration/frontend references with workflow diagrams and text equivalents.
5. Populate each module reference, then Docker/native guides from verified binaries and source contracts.
6. Build and inspect desktop/mobile output; record acceptance results and unresolved clean-environment deployment checks.

## Release Gates

Site build/link checks can run locally. Installation acceptance requires isolated environments, dependency provisioning, registry artifact availability, and operator-created identities/configuration. Do not mark SC-003, SC-007 or reader studies passed on the strength of a website build. A documentation snapshot records per-repository commit and local tag, not a tested unified release. Resolve and validate a compatible release matrix before public release.

## Standalone Compose implementation extension

Generate deploy/compose/<id>/ bundles from tracked public configuration at the inventory's recorded commits. Resolve transitive module/infrastructure dependencies, isolate networks and named volumes, generate runtime keys, and adapt enrollment and policy paths. Retain workstation scope and document required external integrations. Package only SHA-256-reviewed files into deterministic downloads/<id>.zip and raw file routes; exclude runtime secrets and private .env files. Use PyYAML 6.0.1 for manifest tooling and Docker Compose config for parser validation without a daemon. Test dependency graphs, persistence, identity configuration, packaging and bootstrap behavior; record live deployment acceptance independently.

## Existing-core enrollment correction — 2026-10-07

Generate 14 add-on bundles with an external mesh network and private local infrastructure network. Supply the existing public CA bundle and short-lived Auth-signed token as read-only bind mounts. Explicit stdlib configure.py rendering adapts core endpoints, trust domain, mesh tenant, issuer and inbound peer policy; generated runtime YAML remains private and excluded from download allowlists. Local infrastructure has module-specific DNS aliases to avoid ambiguity with the existing core's stores. Do not start peer applications or mint tokens/bootstrap core locally. Keep three initial-core bootstrap bundles clearly labeled. Test configuration rendering against alternate core settings, exact application/network scope and missing/unsafe inputs. Live acceptance still requires an accessible running core.

## Remote-core topology correction — 2026-10-07

Default add-on Compose deployment must work without a shared Docker network: the existing core may run on a different host. Configure routable core endpoints and private host port publication, set FREYA_ADVERTISE_HOST through MODULE_ADVERTISE_HOST, and preserve published/listener port numbers for accurate registration. Require bidirectional connectivity and mesh mTLS; keep admin listeners unpublished. CORE_NETWORK is only used by optional compose.same-host.yaml with .env.same-host.example when both use the same Docker daemon. Enrollment material is obtained on the core host and transferred privately to the module host. This supersedes the previous external-network default.
