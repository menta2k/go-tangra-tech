# Research: Go-Tangra Documentation Site

## Content authority and release scope

- **Decision**: Use sibling `go-tangra`, `go-tangra-auth`, service `*-v4` directories, and `hr-service-v4`. Record Git HEAD, local tag, source path and SHA-256 for each snapshot.
- **Rationale**: The platform README and module Go paths establish v4. Unsuffixed portal and most service checkouts are legacy; naming alone cannot establish currency. Later modules appear in their own READMEs but not the platform README inventory.
- **Alternatives considered**: Copy legacy docs (incorrect major); invent an inventory (unverifiable); fetch all sources during every build (unnecessary network dependence).
- **Evidence**: `../go-tangra/README.md`, each selected README and go.mod. Inventory: framework, auth, portal, lcm, warden, notification, inventory, paperless, deployer, ipam, asset, ticket, dns, scheduler, signing, sms-gw, asterisk, hr.

## Static rendering

- **Decision**: Python 3.12 and installed Python-Markdown 3.5.2, external CSS/JS and relative links.
- **Rationale**: A documentation-focused site needs no client router or server. Markdown preserves maintainable source documents, tables, fenced examples and TOCs. [Official extension documentation](https://python-markdown.github.io/extensions/) confirms bundled table, fenced-code and TOC support.
- **Alternatives considered**: A client-only app loses no-JavaScript reading; a larger site framework adds package/network setup without a requirement; hand-written Markdown parsing risks broken documentation.

## Architecture

- **Decision**: Document Freya, SPIFFE identity, mTLS, deny-by-default policy, auth/OpenFGA, gateway leases, federated UI, LCM enrollment, storage/event infrastructure, and cross-module workflows.
- **Rationale**: These are explicit in platform and module sources. Gateway is the primary browser edge, but ticket inbound email and SMS Hermes have separate documented listeners; do not claim the gateway is the only listener in all deployments.
- **Evidence**: `../go-tangra/docs/{security-model,configuration,frontend,dependencies}.md`, `../go-tangra/deploy/stack/{README,ENROLLMENT}.md`, portal/auth/LCM docs, module deployment notes.

## Installation methods and limitations

- **Decision**: Derive binary names, UI locations/tags, bootstrap flags, admin addresses and infrastructure requirements from source. Provide native dependency preparation linked to module-specific references; use published images only with an explicitly chosen version.
- **Rationale**: `make compose-up` runs container dependencies and is not a native installation. `deploy/container.yaml` contains container paths/hostnames and must be adapted for host processes. Auth requires console+remote tags; portal shell; most modules ui. Asterisk has read-only PBX dependencies and a supplied systemd unit.
- **Evidence**: README, Makefile, Dockerfile, deployment guide, and configuration reference in each selected repository.
- **Alternatives considered**: Generic docker run without enrollment/configuration (cannot work); invoking compose service names not present in the stack (invalid).
- **Resolved constraint**: Actual platform compose includes signing and HR with separate version variables, but not scheduler, SMS or Asterisk. Guides must distinguish those cases and use module-specific manifests or standalone image deployment.
- **Remaining acceptance work**: Clean native/container installations and compatible published artifact matrix. These are implementation/release validation tasks, not unresolved technology choices.

## Accessibility and maintenance

- **Decision**: Semantic HTML, visible focus, skip link, responsive sidebar, local tables of contents, plain-text workflow diagrams with prose equivalents, optional search and copy buttons.
- **Rationale**: Core reading and navigation work without browser scripting or remote services. Source link rewriting preserves provenance and keeps copied documentation navigable.
- **Alternatives considered**: Runtime diagram CDN (offline dependency); importing arbitrary repository files (risk of secrets and irrelevant content).
