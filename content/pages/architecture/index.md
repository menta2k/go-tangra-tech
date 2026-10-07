# System architecture

## A modular platform with a shared trust model

Go-Tangra v4 separates the common framework from independently versioned services. **Freya**, the Go framework in the platform repository, builds on Kratos v3 and supplies identity, transport, authorization, audit, discovery, observability and request limits. Every service consumes the platform module; services expose versioned SDKs where other modules need typed calls.

The browser application is assembled by the Portal gateway from independently shipped module UI remotes. It shares the `@go-tangra/ui` kit rather than a separate full frontend for every service.

## System boundaries

```text
                       Browsers / API clients
                                 |
                          HTTPS + session/token
                                 |
                       Portal / Gateway shell
                       registry and route proxy
                                 |
                 SPIFFE identity + TLS 1.3 mTLS
                 service policy + module authorization
                                 |
        +------------------------+-----------------------+
        |                        |                       |
     Auth + LCM              Domain modules             Warden
 identity + mesh CA         private APIs / UI        secrets access
        |                        |                       |
        +------------------------+-----------------------+
                                 |
            Databases / event streams / objects / integrations
```

The gateway authenticates browser traffic, obtains authorization decisions and routes allowed operations to registered modules. Those private hops are mutually authenticated. The destination module still applies its tenant and operation rules. LCM issues workload identities; Warden mediates configured secret retrieval. Infrastructure and external systems form separate dependency boundaries.

The gateway is the **primary application edge**, not a universal claim that no other listeners exist: [SMS Gateway](modules/sms-gw.html) has its Hermes API, [Ticket](modules/ticket.html) has an inbound mail edge, and integration listeners are explicitly configured by their modules. Admin listeners remain private.

## Complete component map

| Layer | Components | Responsibility |
| --- | --- | --- |
| Foundation | [Platform / Freya](modules/platform.html), shared UI, SDKs, contrib modules | Common service security, lifecycle and frontend contracts |
| Control plane | [Auth](modules/auth.html), [Portal](modules/portal.html), [LCM](modules/lcm.html), [Warden](modules/warden.html) | User identity, routing, certificates and secrets |
| Platform services | [Notification](modules/notification.html), [Scheduler](modules/scheduler.html) | Message delivery and centralized scheduled execution |
| Infrastructure | [Inventory](modules/inventory.html), [IPAM](modules/ipam.html), [DNS](modules/dns.html), [Deployer](modules/deployer.html) | Hosts, networks, DNS and certificate distribution |
| Business modules | [Asset](modules/asset.html), [Paperless](modules/paperless.html), [Ticket](modules/ticket.html), [Signing](modules/signing.html), [HR](modules/hr.html) | Asset/document/helpdesk/signing/leave workflows |
| Communications | [SMS Gateway](modules/sms-gw.html), [Asterisk](modules/asterisk.html) | SMS delivery and read-only PBX observation |

## Identity, policy and tenant isolation

Workloads carry X.509 SVIDs with identities such as `spiffe://<trust-domain>/svc/<name>`. Framework channels use TLS 1.3, verify peer identity rather than only address, and deny operations without an explicit policy grant. Short-lived credentials rotate automatically. Expired or unusable identity fails closed.

Auth signs short-lived tokens for platform users. Modules verify tokens and enforce permissions and resource relationships; service authentication does not replace user authorization. Tenant data is scoped in module storage, with row-level security documented in modules that use it. [Security reference](architecture/security.html) explains transport, policy, refusal audit and revocation behavior.

## Workflow: bootstrap and enrollment

```text
Infrastructure ready
  -> LCM bootstrap: persistent mesh root and initial SVIDs
  -> Gateway bootstrap: SPIFFE identities and route allow-list
  -> Auth bootstrap: tenant, roles and first operator invitation
  -> Vault initialization for Warden
  -> Single-use join tokens for workloads
  -> Workload enrolls with LCM and persists its SVID state
  -> Workload registers a gateway lease and Auth permissions
  -> Gateway exposes the module to authorized users
```

The development stack supplies these jobs in order. Tokens authorize first enrollment; persisted state supports restart and renewal without replaying a spent token. Trust bundles and policies must agree across peers. Root-key or enrollment-state loss changes the recovery procedure. Read [stack enrollment](sources/platform/deploy/stack/ENROLLMENT.html), [LCM operations](sources/lcm/docs/operations.html) and the [stack reference](sources/platform/deploy/stack/README.html).

## Workflow: an authenticated module request

```text
Browser session / bearer token
  -> Portal session exchange or verification through Auth
  -> Permission decision and registered route selection
  -> Private, identity-pinned module channel
  -> Module rechecks tenant and operation/resource authorization
  -> Module-owned store or authorized downstream SDK call
  -> Response through Portal; correlation, traces and audit across hops
```

Gateway registration uses leases. Only allowed workload identities may own granted route prefixes. Lost readiness or expired leases remove routing; an unavailable authorization service fails protected operations closed. [Gateway security](sources/portal/docs/security-model.html) and [module author guide](sources/portal/docs/module-guide.html) describe the route and manifest contracts.

## Workflow: certificate issuance and deployment

```text
Operator / workload -> LCM issuance or renewal
  -> tenant/trust-domain issuer, CSR or generated key
  -> sealed certificate/key state and lifecycle event
  -> Deployer target workflow
  -> target connection / credential retrieval from Warden when configured
  -> delivery result and audited operational status
```

[LCM](modules/lcm.html) owns issuance, renewal and revocation. [Deployer](modules/deployer.html) owns target-specific delivery; configured credentials may be provided through [Warden](modules/warden.html). Target connectivity and permissions are independent of successful certificate issuance. DNS-01 challenges can use [DNS](modules/dns.html) through its supported ACME provider.

## Workflow: inventory into managed assets

```text
Endpoint agent -> Inventory host report / snapshot
  -> Asset inventory-sync preview and filters
  -> selected create/update changes in Asset
  -> attached documents in Paperless, photos in object storage
  -> Scheduler invokes configured inventory-sync task
```

[Inventory](modules/inventory.html) owns endpoint observations; [Asset](modules/asset.html) owns the managed lifecycle. Sync does not turn every observed machine into an asset without its configured filters and decisions. [Asset deployment notes](sources/asset/deploy/README.html) describe matching, consumer policy, scheduled execution and Paperless integration.

## Workflow: a signed leave request

```text
Employee -> HR request -> manager approval
  -> Signing submission (for a signing-required absence type)
  -> parties complete signatures
  -> tenant event stream and HR reconciliation
  -> HR marks approved and charges allowance
  -> Notification delivers configured messages
```

[HR](modules/hr.html) owns allowances, routing and leave state. [Signing](modules/signing.html) owns templates and signing outcomes. An approval requiring signatures waits in `awaiting_signing`; rejection/cancellation/expiry returns the request to the documented state rather than silently charging days. [HR deployment notes](sources/hr/deploy/README.html) document the event consumer and reconciliation contract.

## Data and external dependencies

- **TimescaleDB/PostgreSQL** stores module data and audit history. Modules have application/migration roles and database boundaries; do not substitute a superuser application DSN.
- **Valkey** carries configured event streams, caches and policy distribution. Losing it affects the features using those contracts.
- **OpenFGA** supplies fine-grained authorization relationships for Auth and configured sharing workflows.
- **Vault** backs Warden's secret store. Its KV mount, policy and AppRole need their own initialization.
- **S3-compatible object storage** holds module-owned blobs with tenant-prefixed keys; database backups alone do not include those objects.
- **Tika/Gotenberg** support document extraction/conversion, **PowerDNS** provides DNS serving, and SMTP/carriers/PBX systems remain external integrations.
- **Mailpit and Pebble** are development email/ACME fixtures. Prometheus and OpenLDAP are optional stack integrations.

Each [module reference](modules/index.html) distinguishes required and optional dependencies. [Framework dependencies](architecture/dependencies.html) explain library choices separately from service infrastructure.

## Deployment and operational boundaries

The upstream platform stack runs container images and workstation fixtures. This site's [Docker installation guides](how-to/index.html) provide module Compose bundles that enroll into a running core using routable core endpoints, a reachable advertised module host, an Auth-signed token and public CA trust bundle. They run only the selected module and local infrastructure; peer modules must already exist for enabled integrations. The three core-service bundles are initial-bootstrap examples. Scheduler, SMS Gateway and Asterisk are absent from the recorded upstream base stack; the site's bundles explicitly integrate them. Native services can use host-managed or existing infrastructure, but their endpoints, secret locations, identity paths and writable state must be configured for that environment. Services have independent versions.

Admin `/healthz`, `/readyz` and `/metrics` listeners are separate from public APIs. Keep them private. Audit, traces and request correlation show failures across hops; [configuration](architecture/configuration.html) lists framework defaults and limits. Recovery must preserve the database, encryption keys, blobs, mesh root and enrollment state appropriate to each module.

## Frontend composition

The gateway shell loads a module remote from `/m/<module>/mf-manifest.json` after registration. Shared Vue, router, state, permissions and UI kit contracts bind the runtime. An incompatible UI kit major fails inside that module's boundary; the rest of the shell remains usable. [Frontend reference](architecture/frontend.html) details federation, forms, theming, CSP and image builds.

## Source authority

This overview is synthesized from the [platform README](sources/platform/README.html), [security model](sources/platform/docs/security-model.html), [gateway README](sources/portal/README.html), [stack README](sources/platform/deploy/stack/README.html) and linked module references at their recorded commits. The module inventory includes newer services documented by their repositories even when the older platform inventory table omits them.
