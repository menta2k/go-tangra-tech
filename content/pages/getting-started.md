# Getting started

## Choose your goal

| Goal | Start with | Related components |
| --- | --- | --- |
| Explore the complete platform on a workstation | [Docker installation guides](how-to/index.html) | Platform development stack, Auth, Portal and LCM |
| Run a service on a Linux host without containers | [Native prerequisites](how-to/native-prerequisites.html) | Native infrastructure, identity and policy |
| Track hosts and network addresses | [Inventory](modules/inventory.html) and [IPAM](modules/ipam.html) | [Asset](modules/asset.html), [DNS](modules/dns.html) |
| Manage certificates and their delivery | [LCM](modules/lcm.html) | [Deployer](modules/deployer.html), [Warden](modules/warden.html) |
| Manage documents and signatures | [Paperless](modules/paperless.html) and [Signing](modules/signing.html) | [HR](modules/hr.html), [Notification](modules/notification.html) |
| Connect helpdesk, SMS or PBX observation | [Ticket](modules/ticket.html), [SMS Gateway](modules/sms-gw.html), [Asterisk](modules/asterisk.html) | Auth, Portal, identities and provider/source systems |
| Develop a new module | [Platform](modules/platform.html) | [Gateway module author guide](sources/portal/docs/module-guide.html) |

## Understand the control plane

The [Portal](modules/portal.html) is the primary browser edge. [Auth](modules/auth.html) manages tenants and user authorization. [LCM](modules/lcm.html) establishes mesh identities; [Warden](modules/warden.html) manages secrets for integrations that use it. Modules register API routes and their UI with the gateway and use the shared framework for private service calls.

A module is not automatically independent of the control plane. Read its required dependencies and configuration before choosing an installation method.

## Pick an installation method

**Docker Compose**: download a module bundle and configure the running core's routable endpoints and trust domain, plus this module host's advertised address/private bind IP in `.env`. Supply an Auth-signed enrollment token and the existing public mesh CA bundle, run `python3 configure.py`, then `docker compose up -d`. The selected module enrolls into your existing Auth/Portal/LCM; only its local infrastructure is included. Core-service bundles are explicitly marked for initial bootstrap. Asterisk additionally connects to your existing PBX history source.

**Without Docker**: install the module binary and its required infrastructure as host processes or use existing managed services. Native configuration must contain host-accessible endpoints and real identity/secret paths. Building a native binary while running dependencies through Compose is not the non-Docker path.

[Browse both methods for every module](how-to/index.html).

## Select versions before starting

This site records exact source commits and nearby service tags on each module reference. Each standalone Compose bundle has a separate version variable for every included application in `.env.example`. Choose available, compatible images rather than applying one module's tag to all services. The upstream full-platform stack has its own version configuration; it remains a separate reference.

## Know when installation is complete

1. Bootstrap/migrations finish successfully.
2. The private admin health and readiness endpoints respond successfully.
3. The workload has a valid identity and gateway registration lease.
4. The module appears for an authorized user and its documented smoke operation succeeds.
5. Persistent state and shutdown behavior match the chosen deployment guide.

A running process alone does not prove that a module can serve authorized requests.
