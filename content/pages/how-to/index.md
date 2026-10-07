# Installation guides

## Choose a module, then a method

Regular-module Docker guides use downloadable Compose bundles that enroll into existing Auth/Portal/LCM, with the selected module, local infrastructure and persistent identity/data volumes. Set routable core endpoints and the module advertised host/private bind IP, provide a fresh Auth-signed token and public mesh CA, and render configuration before starting. Auth/Portal/LCM guides identify their separate initial-core bootstrap scope. Native guides build service binaries and connect to host-managed or existing infrastructure without Docker.

| Module | With Docker | Without Docker |
| --- | --- | --- |
| [Auth](modules/auth.html) | [Docker guide](how-to/auth/docker.html) | [Native guide](how-to/auth/native.html) |
| [Portal / Gateway](modules/portal.html) | [Docker guide](how-to/portal/docker.html) | [Native guide](how-to/portal/native.html) |
| [LCM](modules/lcm.html) | [Docker guide](how-to/lcm/docker.html) | [Native guide](how-to/lcm/native.html) |
| [Warden](modules/warden.html) | [Docker guide](how-to/warden/docker.html) | [Native guide](how-to/warden/native.html) |
| [Notification](modules/notification.html) | [Docker guide](how-to/notification/docker.html) | [Native guide](how-to/notification/native.html) |
| [Scheduler](modules/scheduler.html) | [Docker guide](how-to/scheduler/docker.html) | [Native guide](how-to/scheduler/native.html) |
| [Inventory](modules/inventory.html) | [Docker guide](how-to/inventory/docker.html) | [Native guide](how-to/inventory/native.html) |
| [IPAM](modules/ipam.html) | [Docker guide](how-to/ipam/docker.html) | [Native guide](how-to/ipam/native.html) |
| [DNS](modules/dns.html) | [Docker guide](how-to/dns/docker.html) | [Native guide](how-to/dns/native.html) |
| [Deployer](modules/deployer.html) | [Docker guide](how-to/deployer/docker.html) | [Native guide](how-to/deployer/native.html) |
| [Asset](modules/asset.html) | [Docker guide](how-to/asset/docker.html) | [Native guide](how-to/asset/native.html) |
| [Paperless](modules/paperless.html) | [Docker guide](how-to/paperless/docker.html) | [Native guide](how-to/paperless/native.html) |
| [Ticket](modules/ticket.html) | [Docker guide](how-to/ticket/docker.html) | [Native guide](how-to/ticket/native.html) |
| [Signing](modules/signing.html) | [Docker guide](how-to/signing/docker.html) | [Native guide](how-to/signing/native.html) |
| [HR](modules/hr.html) | [Docker guide](how-to/hr/docker.html) | [Native guide](how-to/hr/native.html) |
| [SMS Gateway](modules/sms-gw.html) | [Docker guide](how-to/sms-gw/docker.html) | [Native guide](how-to/sms-gw/native.html) |
| [Asterisk](modules/asterisk.html) | [Docker guide](how-to/asterisk/docker.html) | [Native guide](how-to/asterisk/native.html) |

## Before you begin

- Read the selected module's required and optional dependencies.
- Choose compatible service/control-plane versions. Source revisions and local tags are listed on module references; published artifact availability must be checked for the chosen version.
- Native deployments begin with [native prerequisites](how-to/native-prerequisites.html).
- Standalone Compose bundles use workstation-only fixture credentials and generate private keys in persistent volumes. For production, supply your own infrastructure, identities, encryption keys, edge certificates and policies.

## Standalone Compose bundles

Each module's Docker guide links to its complete ZIP, raw `compose.yaml` and `.env.example`. Download and extract the ZIP, copy `.env.example` to `.env`, then edit the operator email, available versions and any required external integration values. From that directory:

```sh
docker compose config --quiet
docker compose pull
docker compose up -d
docker compose --profile checks run --rm check
```

The ZIP includes all mounted configuration, policies and initialization scripts. Asterisk requires a SELECT-only DSN for your PBX's CDR database; its registration database is provisioned separately. The framework and SDKs are libraries and do not have standalone Compose daemons.

## Shared framework and libraries

The [platform framework, SDKs, contrib packages and UI kit](modules/platform.html) are consumed by services. They are not standalone daemons with Docker installations.

## Verification and recovery

Every service guide includes bootstrap/start, configured admin health/readiness checks, registration, diagnostics and shutdown. Keep the database, object data, encryption keys and enrollment state required by the module. A stopped service can retain all persistent data; deleting it is a separate operation.
