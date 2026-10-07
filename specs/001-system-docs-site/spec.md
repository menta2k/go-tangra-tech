# Feature Specification: Go-Tangra System Documentation Site

**Feature Branch**: Not created; no branch creation hook is configured.

**Created**: 2026-10-05

**Status**: Draft

**Input**: User description: "Create a static website that introduces the Go-Tangra system, provides detailed documentation of the entire architecture and each module, and includes how-to guides for installing a module with or without Docker."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Understand Go-Tangra (Priority: P1)

As a new visitor, I want an introduction explaining what Go-Tangra does, who it serves, and how its modules fit together, so I can decide whether it meets my needs and where to start.

**Why this priority**: An understandable entry point makes the detailed documentation useful to newcomers.

**Independent Test**: Open the homepage without prior system knowledge and find the system purpose, principal capabilities, architecture overview, module directory, and getting-started guide.

**Acceptance Scenarios**:

1. **Given** a first-time visitor, **When** they open the homepage, **Then** they see the system purpose, intended users, principal capabilities, and links to architecture, modules, and installation how-tos.
2. **Given** a visitor evaluating the system, **When** they follow the getting-started path, **Then** they can identify a suitable module and reach its prerequisites and installation options.

---

### User Story 2 - Explore the Entire Architecture (Priority: P1)

As an engineer or operator, I want detailed system architecture documentation so I can understand component responsibilities, interactions, dependencies, and operational boundaries.

**Why this priority**: Understanding the complete architecture is a core requested outcome and supports correct deployment and integration.

**Independent Test**: Read the architecture documentation and trace a documented end-to-end workflow through all participating components using diagrams and accompanying explanations.

**Acceptance Scenarios**:

1. **Given** a reader on the architecture overview, **When** they explore its sections, **Then** they find system boundaries, all verified components, responsibilities, relationships, deployment arrangements, communication patterns, data flows, and external dependencies.
2. **Given** a documented workflow, **When** a reader follows its diagram and explanation, **Then** they can identify the participating modules, exchanged information, and relevant failure boundaries.
3. **Given** an architecture section referring to a module, **When** the reader follows its link, **Then** they reach that module's detailed documentation.

---

### User Story 3 - Understand an Individual Module (Priority: P1)

As a developer or operator, I want a complete reference for each module so I can understand its purpose, configure it, integrate it, and operate it.

**Why this priority**: Per-module documentation is explicitly required and enables users to work with the system incrementally.

**Independent Test**: Select any module from the verified inventory and inspect its reference against the required documentation topics.

**Acceptance Scenarios**:

1. **Given** the module directory, **When** a reader selects any module, **Then** they find its purpose, capabilities, architecture role, dependencies, configuration, interfaces, operational guidance, and limitations.
2. **Given** a module depending on another component, **When** a reader examines its dependencies, **Then** required and optional dependencies are distinguished and linked to relevant documentation.
3. **Given** a module that is not independently installable, **When** a reader seeks installation instructions, **Then** its page explains how it is consumed or included and links to the relevant parent installation guide.

---

### User Story 4 - Install a Module With or Without Docker (Priority: P1)

As an operator, I want step-by-step installation how-tos for both Docker and a non-Docker environment so I can install and verify a module using the approach appropriate to my environment.

**Why this priority**: Both installation paths are explicit requirements and turn reference documentation into an actionable onboarding resource.

**Independent Test**: For each installable module, follow each supported installation path in a clean documented environment and verify the stated success result.

**Acceptance Scenarios**:

1. **Given** an installable module and a supported environment, **When** an operator selects the Docker path, **Then** the guide provides prerequisites, dependency setup, version selection, configuration, installation, startup, verification, troubleshooting, and cleanup steps in execution order.
2. **Given** the same module and a supported environment, **When** an operator selects the non-Docker path, **Then** the guide explains required tools and dependencies, obtaining or building the module, configuration, startup, verification, troubleshooting, and cleanup without requiring Docker at any step.
3. **Given** a failed verification step, **When** the operator follows troubleshooting instructions, **Then** they can compare expected output, locate relevant diagnostics, and identify documented corrective actions.
4. **Given** a module with required dependencies, **When** an operator follows either installation path, **Then** dependency setup is provided or linked before the module needs those dependencies.

### Edge Cases

- A shared library or embedded module cannot be installed independently: explain its consumption model rather than publish misleading installation commands.
- An installable module lacks one requested installation path: record the gap and resolve it before release; do not present an unverified workaround as supported.
- A platform or version is unsupported: state support boundaries before installation instructions and direct readers to supported alternatives.
- A required dependency, artifact, or configuration value is missing: show how to detect and resolve the missing prerequisite.
- A port is occupied, credentials are invalid, or persistent storage is unavailable: include relevant diagnostics and recovery steps for affected modules.
- A diagram cannot be viewed or navigation scripting is unavailable: core content and navigation remain usable, with a textual explanation of diagrams.
- A reader opens a nested page directly or requests an unknown URL: valid pages load independently and missing pages offer a route back to documentation.
- Source information is incomplete or conflicting: resolve discrepancies against authoritative module sources before publishing factual claims.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The site MUST be a public static website whose published documentation can be read without an account, a running Go-Tangra deployment, or a dedicated documentation application server.
- **FR-002**: The homepage MUST introduce Go-Tangra's purpose, intended audiences, principal capabilities, and module-based organization, with clear entry points to architecture, modules, and how-tos.
- **FR-003**: The site MUST provide a getting-started path that leads from system introduction to module selection, prerequisites, installation method, and verification.
- **FR-004**: Architecture documentation MUST cover every component in the verified system inventory, including system boundaries, responsibilities, component relationships, deployment arrangements, communication, data ownership and flows, external dependencies, security boundaries, and operational concerns. Topics that do not apply MUST include a brief explanation.
- **FR-005**: Architecture documentation MUST include a system overview diagram and diagrams for documented end-to-end workflows, with explanatory text and links to participating module references.
- **FR-006**: The module directory MUST list every module in the verified inventory, with a concise purpose, its architecture role, and a link to its dedicated reference.
- **FR-007**: Each module reference MUST document purpose, capabilities, required and optional dependencies, supported environments and versions, configuration settings and defaults, required values, interfaces and usage examples, startup behavior, health verification, diagnostics, limitations, and links to architecture and applicable installation guides. Inapplicable topics MUST be explained.
- **FR-008**: The site MUST have a dedicated how-to section organized by module and installation method, reachable from global navigation and each relevant module page.
- **FR-009**: Every independently installable module MUST have separate, complete Docker and non-Docker installation paths. Non-installable modules MUST document how they are consumed and link to the applicable installation context.
- **FR-010**: Each installation path MUST state its supported platform and module version, prerequisites, dependency setup, artifacts and their source, ordered installation and startup instructions, configuration, expected verification results, common failures and remedies, and stop/removal steps. Steps that delete persistent data MUST explicitly identify the affected data before the action.
- **FR-011**: Installation examples MUST be copyable, distinguish commands from expected output, identify placeholders and where to obtain their values, and never contain real secrets. Required dependency installation for the non-Docker path MUST also work without Docker.
- **FR-012**: Documentation MUST identify the system or module release it describes and link factual architecture, configuration, and installation details to authoritative source material. All installation paths MUST be validated against their stated environment and version before release.
- **FR-013**: Readers MUST be able to move between introduction, architecture, module references, and how-tos through consistent navigation; long pages MUST provide a local table of contents and linkable section headings.
- **FR-014**: Published pages and section links MUST be directly addressable and support browser back/forward navigation. An unknown page MUST explain that it was not found and offer links to the homepage and documentation.
- **FR-015**: Core documentation and navigation MUST be readable on phone and desktop screens, operable with a keyboard, and usable with assistive technology. Diagrams MUST have text equivalents, and wide examples MUST not cause whole-page horizontal scrolling.
- **FR-016**: All published module references and guides MUST contain verified content rather than empty sections, invented module names, unsupported commands, or claims inferred solely from naming conventions.

### Key Entities

- **System Documentation**: Introduction, architecture, and getting-started material associated with a documented system release and authoritative sources.
- **Module**: A verified system unit with a name, purpose, architecture role, dependencies, supported versions, and whether it is independently installable.
- **Module Reference**: A module's configuration, interfaces, operation, limitations, source references, and related guides.
- **Installation Guide**: A module-specific procedure associated with an installation method, supported environment and version, prerequisites, steps, verification results, troubleshooting, and removal instructions.
- **Architecture Workflow**: A documented interaction spanning components, with a diagram, textual explanation, and links to module references.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: At least 4 of 5 representative first-time readers can describe Go-Tangra's purpose and find a relevant module and its installation options within 3 minutes using only the site.
- **SC-002**: 100% of components and modules in the verified release inventory appear in architecture documentation and have complete module references, with every required topic covered or explicitly explained as inapplicable.
- **SC-003**: 100% of independently installable modules have two validated installation paths; a tester starting in each documented clean environment reaches the guide's stated verification result without undocumented steps.
- **SC-004**: At least 4 of 5 representative engineers can trace a documented end-to-end workflow and identify its participating modules and dependencies within 10 minutes.
- **SC-005**: Every module reference and installation guide is reachable within three navigation selections from the homepage, and all internal page and section links resolve successfully.
- **SC-006**: All primary reading and navigation journeys can be completed using only a keyboard at phone and desktop viewport sizes, with no inaccessible required content or whole-page horizontal overflow.
- **SC-007**: Every published factual architecture claim and installation procedure is traceable to an authoritative source and a documented release; no unresolved content gaps remain at launch.

## Assumptions

- This invocation creates the feature specification, not the website implementation or a deployment.
- Initial content is in English and serves newcomers, developers, and operators. Localization and historical version browsing are outside the initial scope.
- The initial site documents one explicitly identified supported system release and compatible module versions. Selecting those versions depends on authoritative project information.
- The current repository contains Spec Kit scaffolding but no system source, module inventory, or substantive architecture documentation. Access to authoritative Go-Tangra repositories, release artifacts, configuration references, and maintainers' architecture information is a content dependency for planning and implementation.
- The complete module inventory and supported environments will be established from those sources; this specification deliberately does not invent module names, system relationships, or installation commands.
- Each installable module is expected to support both requested installation methods. Missing support must be resolved during planning and implementation before the site's completeness criteria can pass.
- The site provides instructions for readers to execute in their own environments; interactive deployment, account management, and a live administrative console are outside scope.
- Site technology, visual design, hosting provider, and automated content maintenance are decisions for planning. Search is optional; global navigation, the module directory, and page tables of contents are required.
- The repository's constitution is an unfilled template and currently provides no adopted project-specific principles. No extension hooks or template overrides are configured.

## Additional requested scope — standalone Compose

Every independently installable service must have a checked-in standalone Docker Compose bundle and a Docker guide using Compose. Each bundle includes its own Auth/Portal/LCM control plane and required infrastructure and module dependencies. External providers and PBX integrations must be explicit. Documentation must link downloadable bundles, explain configuration, startup, verification, logs and teardown, and identify persistent data. Runtime secrets must never enter site downloads. Live acceptance remains required separately from manifest validation.

## Clarification — existing-core enrollment (2026-10-07)

The module Compose installation requirement means adding an individual service to already running Portal/Auth/LCM. This supersedes the earlier own-control-plane interpretation for regular modules. Each add-on runs only its selected application and local infrastructure, joins an existing external Docker mesh network, verifies the existing CA, exchanges an Auth-signed token with LCM and registers its UI/routes and permissions with existing core services. Peer modules are separately running dependencies. Initial Auth/Portal/LCM setup is a distinct core-bootstrap procedure, not an add-on enrollment workflow.

## Remote-core topology correction — 2026-10-07

Default add-on Compose deployment must work without a shared Docker network: the existing core may run on a different host. Configure routable core endpoints and private host port publication, set FREYA_ADVERTISE_HOST through MODULE_ADVERTISE_HOST, and preserve published/listener port numbers for accurate registration. Require bidirectional connectivity and mesh mTLS; keep admin listeners unpublished. CORE_NETWORK is only used by optional compose.same-host.yaml with .env.same-host.example when both use the same Docker daemon. Enrollment material is obtained on the core host and transferred privately to the module host. This supersedes the previous external-network default.
