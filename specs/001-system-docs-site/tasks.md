# Tasks: Go-Tangra System Documentation Site

**Input**: [plan.md](plan.md), [spec.md](spec.md), research.md, data-model.md, contracts/site.md, quickstart.md

## Phase 1: Setup

- [X] T001 Create build dependencies, commands and ignore patterns in requirements.txt, Makefile, .gitignore and .dockerignore.
- [X] T002 Create source snapshot importer and verified inventory in scripts/import_sources.py and content/modules.json.

## Phase 2: Foundational

- [X] T003 Implement deterministic Markdown rendering, relative routes, provenance and static assets in scripts/build.py.
- [X] T004 Implement link/fragment/content integrity checks in scripts/check.py and tests/test_site.py.
- [X] T005 Create accessible responsive shared navigation, sidebar, typography, code blocks and optional enhancements in assets/site.css and assets/site.js.

## Phase 3: US1 — Understand Go-Tangra (P1, MVP)

**Goal**: A newcomer understands the system and finds the next step.
**Independent test**: Open homepage, explain system purpose and reach a module guide without JavaScript.

- [X] T006 [US1] Write verified introduction and homepage layout in content/pages/index.md and scripts/build.py.
- [X] T007 [P] [US1] Write getting-started decisions and supported-release guidance in content/pages/getting-started.md.

## Phase 4: US2 — Explore Architecture (P1)

**Goal**: Engineers trace component interactions and deployment boundaries.
**Independent test**: Trace enrollment, browser request, certificate deployment and HR signing workflows using prose and diagrams.

- [X] T008 [US2] Write complete architecture overview and workflow diagrams in content/pages/architecture/index.md.
- [X] T009 [P] [US2] Add detailed platform security, configuration, frontend and dependency references in content/pages/architecture/ and content/sources/platform/.

## Phase 5: US3 — Understand Modules (P1)

**Goal**: Every verified module has a sourced reference.
**Independent test**: Pick any inventory entry and find purpose, dependencies, configuration/interface details, operation and related guides.

- [X] T010 [US3] Create grouped module directory in content/pages/modules/index.md.
- [X] T011 [US3] Populate 18 source-derived module references and configuration/API indexes in content/modules/ and content/sources/.

## Phase 6: US4 — Install Modules (P1)

**Goal**: Separate Docker/native guides cover each service and platform libraries have consumption instructions.
**Independent test**: Inspect both guide paths per service, then execute them in the documented clean environments before release.

- [X] T012 [US4] Create method/module installation directory and shared prerequisites in content/pages/how-to/index.md and content/pages/how-to/native-prerequisites.md.
- [X] T013 [US4] Create 17 Docker procedures including stack exceptions and persistent state in content/guides/.
- [X] T014 [US4] Create 17 native procedures with verified build flags, dependency/configuration adaptation, bootstrap, verification and teardown in content/guides/.
- [X] T015 [US4] Document framework/contrib/SDK/UI consumption in content/modules/platform.md.
- [ ] T016 [US4] Execute clean Docker/native deployment acceptance for all 17 services and record environments/results in specs/001-system-docs-site/validation.md.

## Phase 7: Polish and Release Evidence

- [X] T017 Add 404 output, local search index, source attribution and maintenance/run instructions in scripts/build.py and README.md.
- [ ] T018 Run static build, all link/content checks, meaningful test suite and HTTP smoke checks; record results in specs/001-system-docs-site/validation.md.
- [ ] T019 Inspect desktop/mobile/no-JavaScript layouts and keyboard navigation; record results in specs/001-system-docs-site/validation.md.
- [ ] T020 Validate a compatible published module release matrix and update content/modules.json and specs/001-system-docs-site/validation.md.
- [ ] T021 Conduct five-reader discovery/workflow studies and record SC-001/SC-004 evidence in specs/001-system-docs-site/validation.md.

## Dependencies & Execution Order

T001 → T002 → T003/T004/T005 → story content → T017/T018/T019. All stories require the shared renderer/inventory. US2–US4 are independently reviewable after foundations; cross-links integrate them with US1. T016 requires completed guide content, real dependency provisioning, identities and a chosen compatible release matrix (T020). T021 requires the assembled site and readers.

## Parallel Opportunities

US1: getting-started text can be drafted separately from homepage rendering. US2: each detailed platform reference can be imported independently of overview prose. US3: references for distinct component ids occupy different content/modules files. US4: per-service Docker/native procedures occupy different guide files after shared prerequisites are established. Shared importer/builder changes remain sequential.

## Implementation Strategy

Build the introduction MVP first, then add architecture, module references and guide content incrementally. Run integrity checks after integration. Track environment acceptance and reader studies honestly as pending until actual evidence exists; do not turn source-reviewed commands into claimed deployment validation.

## Current Validation Status

T018 is partially complete: build, source/content checks, Node syntax and all 26 tests pass; HTTP smoke execution is blocked by sandbox socket restrictions. T019 remains pending because Chromium launch fails on a denied socket operation. T016 requires an accessible Docker/native environment; Docker daemon access is denied here. T020 and T021 require a tested published version matrix and representative readers. See validation.md for evidence.

## Standalone Compose extension — 2026-10-06

- [X] T022 [US4] Generate 17 isolated standalone Compose bundles with required control-plane services, dependency closure, configuration, policies, bootstrap, persistent state and source provenance in deploy/compose/ and scripts/create_compose.py.
- [X] T023 [US4] Replace Docker procedures with Compose lifecycle instructions and module-specific integrations; publish reviewed ZIP/raw downloads through scripts/build.py.
- [X] T024 [US4] Validate all 17 manifests with Docker Compose, verify dependency/storage/enrollment contracts and secret-safe packaging, and test key/Vault bootstrap scripts in tests/test_compose.py.

T016 remains pending: parsing and bootstrap fixture tests do not establish live deployment success or published image compatibility.

## Permission reference extension — 2026-10-06

- [X] T025 [US3] Snapshot public manifests at recorded revisions and document all 148 permissions from 16 declaring services, including qualified names, descriptions, UI abilities, navigation gates and matching API operations. Explain framework/Portal behavior explicitly.
- [X] T026 [US3] Add assignment, resource access, tenant scope, exceptional access and verification guidance; test catalogue provenance, complete rendering and sensitive scope explanations.

## Existing-core enrollment correction — 2026-10-07

- [X] T027 [US4] Replace regular-module own-core deployments with 14 external-core enrollment bundles, one application each, private infrastructure, verified CA/token mounts and persistent SVID state; clearly label 3 initial-core bootstrap bundles.
- [X] T028 [US4] Add explicit private configuration/policy rendering and document existing Auth token issuance, LCM exchange, Gateway allow-list/permissions registration, reciprocal peer grants and lifecycle.
- [X] T029 [US4] Validate alternate-core rendering, missing/unsafe inputs, unique local infrastructure addresses, external-network/application boundaries and all Compose manifests.

T016 remains pending for live enrollment, renewal and authorization against a supported existing core.

- [X] T030 [US4] Make remote-core routing the default, publish module mesh ports on a configured private host interface and register a reachable FREYA_ADVERTISE_HOST; retain CORE_NETWORK only in optional same-host overrides. Update topology/token-transfer/firewall documentation and validate both variants.
