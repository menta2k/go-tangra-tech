"""Docker guide for adding a module to an existing core."""

def guide(module, bundle):
    id_, svc = module['id'], bundle['service']
    prefixes = '/api/warden,/warden/share' if id_ == 'warden' else '/api/' + id_
    source = lambda m, path: f"{m['repository']}/blob/{m['commit']}/{path}"
    return f'''# Add {module['name']} to an existing core with Docker Compose

This bundle runs **only `{svc}` and its local infrastructure**, and enrolls it into your running Auth/Portal/LCM system. It does not bootstrap a second core or install peer modules. Use your existing Portal login and Auth tenant roles.

## Prerequisites

Use Docker Engine with Compose v2 or later, Python 3 to render configuration, registry access and compatible published v4 images. `{module['tag']}` is recorded source metadata, not proof of a published or compatible image.

Your existing Auth, Gateway and LCM must be healthy and mutually trusted. **The default bundle supports a core on a different host** over a private routed network or VPN. Docker bridge networks are local to a Docker daemon; naming a remote host's network does not connect to it.

Set core discovery/enrollment addresses to DNS names or IPs reachable from the module container. On the core host, expose the required mesh listeners on its private interface and permit module-host access: Auth gRPC (default 9543), Gateway registration gRPC (9643), LCM renewal gRPC (9945) and direct HTTPS enrollment (9947). Use your actual configured ports. The browser Gateway HTTPS URL is the issuer, not a replacement for those mesh endpoints.

In the reverse direction, Gateway and peer services must reach the module host's published HTTP/gRPC ports. `MODULE_ADVERTISE_HOST` sets `FREYA_ADVERTISE_HOST`, so registration advertises that reachable DNS/IP instead of a Docker container IP. `MODULE_BIND_IP` is the private IPv4 interface on the module host where Compose publishes the mesh ports. Use the same external/internal port numbers: the framework override changes the advertised host, not the port. Do not put TLS termination that strips mesh client identity in front of these mTLS listeners. Keep routes/firewall rules restricted to trusted hosts; admin ports remain unpublished. Do not use `localhost` or container-only DNS names for a remote core.

## Optional same-host topology

If the core shares the module's Docker daemon, copy `.env.same-host.example` to `.env` instead. Set its `CORE_NETWORK` to the actual existing network and its issuer to the existing Portal URL. This example sets `COMPOSE_FILE=compose.yaml:compose.same-host.yaml`, so subsequent `docker compose` commands automatically include the local mesh attachment. `MODULE_ADVERTISE_HOST` is the module's network alias and mesh port publication binds loopback. The overlay is not used for a remote core.

**Required module dependencies**: {', '.join(module['required'])}. The local stores in this bundle use workstation credentials. Existing peer modules and their reciprocal service-policy/consumer grants must be configured separately. Inspect the [module reference](modules/{id_}.html) before enabling optional integrations.

## Download and configure

[Download the {module['name']} bundle](downloads/{id_}.zip) · [Compose manifest](downloads/{id_}/compose.yaml) · [Environment example](downloads/{id_}/.env.example)

```sh
unzip {id_}.zip
cd {id_}
cp .env.example .env
mkdir -p private
chmod 700 private
```

A repository checkout can instead use `deploy/compose/{id_}`. Edit `.env` using values from the running core:

| Setting | Meaning |
| --- | --- |
| `MODULE_ADVERTISE_HOST` | Module host DNS/IP resolvable and reachable from the core; used for registered HTTP/gRPC endpoints. |
| `MODULE_BIND_IP` | Private IPv4 address on this Docker host to publish module mesh listeners. |
| `CORE_NETWORK` | Only for the optional same-host overlay; never identifies a network on another host. |
| `TRUST_DOMAIN` | Trust domain of existing workload identities; do not introduce a new domain. |
| `TENANT_ID` | LCM mesh-CA enrollment tenant, matching the token. The recorded default is the mesh tenant, not automatically a business tenant. |
| `MESH_ENV` | Environment expected by your mesh identity conventions. |
| `AUTH_GRPC`, `GATEWAY_GRPC`, `LCM_GRPC` | Core service DNS names/ports reachable from the module container. Default examples use `core.internal.example` with ports 9543, 9643 and 9945. Replace the hostname with your reachable core host(s). |
| `LCM_ENROLL_URL` | Direct HTTPS LCM enrollment endpoint; default path `/api/lcm/v1/enroll` on port 9947. |
| `GATEWAY_ISSUER` | Existing browser/token issuer URL, matching the running core. |
| `ENROLLMENT_TOKEN_FILE` | Private file containing the fresh enrollment token for this workload. |
| `MESH_CA_FILE` | Existing public mesh CA trust bundle; never the CA private key. |
| `{id_.upper().replace('-', '_')}_VERSION` | Published version compatible with the existing core. |

Review `configs/module.yaml` and `policies/module.yaml`. These are templates: `@@NAME@@` placeholders are deliberately rendered by `configure.py`, because most services do not expand environment variables inside YAML. Edit peer discovery, optional integrations and local infrastructure settings here, then render after every change. The policy's SPIFFE trust domain is rendered too; review exact peer identities and operations rather than granting arbitrary callers.

## Obtain a token from the existing Auth

Enrollment tokens are signed by **Auth** and redeemed with **LCM**. Obtain one through your supported core enrollment workflow. The recorded Auth also provides a workstation CLI that uses its existing configuration/stores/signing keys. For a Compose core using service `auth`, binary `authsvc` and `/app/deploy/container.yaml`, run the following on the **core host** in a private working directory, replacing the core Compose path and trust domain. Create the private output directory first:

```sh
umask 077
mkdir -p private
docker compose -f /ABSOLUTE/PATH/TO/CORE/compose.yaml exec -T auth authsvc mint-enrollment-token -config deploy/container.yaml -spiffe spiffe://YOUR_TRUST_DOMAIN/svc/{svc} -tenant 00000000-0000-0000-0000-000000000001 -ttl 30m > private/enrollment.token
chmod 600 private/enrollment.token
```

Match `-tenant` to `TENANT_ID` and your existing mesh CA tenant. Use the actual core service name/configuration path and its usual Compose project/env options. This invokes the existing Auth, not a new Auth installation. On failure, discard the output file and fix the command; never use an empty token. Transfer the token securely to the module host's configured private file path before it expires. Copy the existing **public** mesh CA bundle into `private/ca.pem` through your core's normal trust-distribution mechanism. Do not copy private Auth signing keys or CA keys into this module bundle.

The token is short-lived and single-use. Mint it immediately before initial startup. After successful enrollment the module persists its SVID in its named state volume and renews through LCM; ordinary restarts retain that identity. Deleting state or changing the identity/trust settings requires planned re-enrollment with a fresh token.

## Authorize registration on the existing core

The existing Gateway must allow `spiffe://YOUR_TRUST_DOMAIN/svc/{svc}`, route prefixes **`{prefixes}`** and module name **`{svc}`**. Update the allow-list through your core's managed configuration. The recorded Gateway CLI accepts a repeatable `-allow` entry; run on the **core host** for a workstation core using service `gateway` and binary `gatewaysvc`:

```sh
docker compose -f /ABSOLUTE/PATH/TO/CORE/compose.yaml exec -T gateway gatewaysvc bootstrap -config deploy/container.yaml -allow 'spiffe://YOUR_TRUST_DOMAIN/svc/{svc}={prefixes};{svc}'
```

Use the running core's configuration/store and its normal deployment procedure. Review this administrative change against your existing allow-list; do not replace it with this module's entry. Gateway enrollment/registration authorization and Auth permission registration are distinct from the user's module roles.

Review Auth and LCM's inbound peer policies for this exact module identity, including permission/role registration, authorization and SVID renewal. Review reciprocal policies on any optional peer module. The bundled policy controls inbound calls to `{svc}`; it cannot grant access on another service. A service name in discovery or an enrollment token alone does not grant every RPC.

## Render, validate and start

```sh
python3 configure.py
# Review runtime/config.yaml and runtime/policy.yaml privately.
docker compose config --quiet
docker compose pull
docker compose up -d
docker compose ps -a
docker compose logs --tail=100 {svc}
```

The renderer checks required settings and token/CA file presence, creates private runtime files and never prints credential values. Input files, `.env` and runtime configuration are excluded from website downloads. Compose mounts the token and trust bundle read-only. Local initialization jobs prepare only this module's stores/keys; they do not initialize Auth, Gateway or LCM.

Expected startup sequence: local stores become ready, the module verifies the existing LCM identity against the supplied CA and expected SPIFFE ID, exchanges its token for an SVID, persists enrollment state, registers routes/UI with Gateway, and registers permission/role information with Auth. Inspect module logs for enrollment and registration failures. Initialization/runtime logs can contain operational data; handle them privately.

## Verify installation

```sh
docker compose --profile checks run --rm check
docker compose logs --tail=100 {svc}
```

The check probes `/healthz` and `/readyz` on private admin port {bundle['admin_port']} without publishing it. Confirm successful enrollment and renewal in LCM/module logs, module visibility in your **existing Portal**, and permission catalogue registration in existing Auth. Assign a suitable [module permission](modules/{id_}.html#permissions-and-authorization) to a test user and execute a small read. Also check denial for an ungranted action; readiness alone does not establish authorization or external feature acceptance.

## Module-specific setup

'''+specific(id_)+f'''

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Remote host cannot resolve/reach core | Use routable core DNS/IPs, private listener publication and firewall/VPN routes; Docker service names work only on the same-host overlay. |
| Enrolled but Gateway cannot reach module | Verify `MODULE_ADVERTISE_HOST` from the core host, module private port bindings, matching advertised/listener ports and reverse firewall routes. |
| Same-host external network missing | Set `CORE_NETWORK` to a network on this Docker daemon and enable only the same-host overlay. |
| Enrollment TLS/SPIFFE rejection | Match CA bundle, trust domain, LCM HTTPS endpoint and `spiffe://TRUST_DOMAIN/svc/lcm`; keep `insecure: false`. |
| Token expired/used/rejected | Obtain a fresh Auth-signed token for the exact module SPIFFE ID and mesh tenant. Retain existing valid identity state on ordinary restarts. |
| Core connection refused | Check container DNS names/ports, routing/VPN/firewall rules and reciprocal reachability; `localhost` inside the module refers to itself. |
| Enrolled but not registered | Check existing Gateway allow-list, Auth/peer inbound policies, module identity and registration logs. |
| Missing UI/action or forbidden resource | Check selected business tenant, direct/group roles, exact qualified permission and resource grants; mesh identity is separate. |
| Renderer fails or config change has no effect | Correct .env/input files, edit the source template, rerun `python3 configure.py`, then recreate the module with Compose. |
| Restored encrypted data fails | Restore matching module keys with its database/object data; do not replace retained keys. |

## Stop and remove

```sh
docker compose stop {svc}
docker compose up -d
docker compose down
```

`down` removes this project's containers/local network and preserves its named volumes. The running remote Auth/Portal/LCM are unaffected. When using the same-host overlay, its external core network is retained too. `docker compose down -v` destroys this module's stores, keys and SVID state; back them up before a deliberate reset and issue a fresh enrollment token afterward. For permanent removal, retire its existing-core registration/permissions and revoke its workload identity through the core's managed process. Other modules may depend on it.

## Sources and validation scope

[Module source at recorded revision]({module['repository']}/tree/{module['commit']}) · [Module reference](modules/{id_}.html) · [Upstream stack reference](sources/platform/deploy/stack/README.html).

The configuration/network rendering is authored here from recorded public deployment contracts. Manifest parsing and fixture tests do not establish live enrollment acceptance or image compatibility; test the documented workflow against your chosen core release before production use.
'''


def specific(id_):
    notes = {
        'asterisk': 'Set ASTERISK_CDR_DSN to reachable SELECT-only PBX credentials. Set binding.tenant_id in the template to the business tenant bound to the PBX (it may differ from the mesh enrollment tenant). The local registration database is separate. Enable AMI, read-only recordings and monitoring only after configuring them.',
        'sms-gw': 'Configure the carrier/provider and API client in the existing Portal before sending. Its Hermes HTTP listener uses host loopback port 9901 by default; configure public TLS separately. Local KEK/JWT and enrollment state are persisted.',
        'dns': 'Local PowerDNS and Prometheus are included. Existing IPAM/Inventory/Warden peers must match discovery and policy settings for enabled integrations. Docker-socket control is disabled; apply managed DNS settings with docker compose restart pdns-auth pdns-recursor.',
        'ipam': 'Inventory/Warden/Scheduler are existing peer services, not included installations. Configure their discovery addresses and grants, including Inventory host-report consumer access. NET_RAW is enabled for ICMP scans; BMC credentials and endpoint agents remain external.',
        'asset': 'Inventory/Paperless/Scheduler are existing peers. Configure object storage, discovery and reciprocal consumer/resource grants; disable unused features explicitly.',
        'deployer': 'Configure existing Inventory discovery and consumer grants where used, plus the target credentials and network reachability. Verify each delivery target independently.',
        'hr': 'Signing/Notification/Scheduler are existing peers. Configure matching templates, event consumers, reconciliation and user relationships before testing signature-required absence requests.',
        'signing': 'Notification/Warden/Scheduler are existing peers. Configure tenant signing CA/template lifecycle, scheduled tasks and external B-Trust environment as needed.',
        'ticket': 'Configure existing Warden and any notification/mail integrations you enable. The inbound mail listener is a separate edge with a relay token; keep private API/admin listeners private.',
        'notification': 'Configure an SMTP channel and its resource grants before testing delivery. Mesh enrollment and module readiness do not configure an email provider.',
        'inventory': 'Enroll endpoint agents separately. Peer consumers need the configured report allow-list and matching policy, independent of human UI roles.',
        'warden': 'Local persistent workstation Vault is included; configure its required mount/AppRole and back up its data/recovery state with the module database and KEK.',
        'paperless': 'Local object storage and extractors are included. Configure categories/document sharing and verify actual extraction/download behavior after registration.',
        'scheduler': 'Task-producing/executing peer modules must already exist, resolve through discovery and allow the task-registration/executor RPCs. A running scheduler does not automatically create every tenant task.',
    }
    return notes[id_]
