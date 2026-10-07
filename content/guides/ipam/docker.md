# Add IPAM to an existing core with Docker Compose

This bundle runs **only `ipam` and its local infrastructure**, and enrolls it into your running Auth/Portal/LCM system. It does not bootstrap a second core or install peer modules. Use your existing Portal login and Auth tenant roles.

## Prerequisites

Use Docker Engine with Compose v2 or later, Python 3 to render configuration, registry access and compatible published v4 images. `v4.10.3` is recorded source metadata, not proof of a published or compatible image.

Your existing Auth, Gateway and LCM must be healthy and mutually trusted. **The default bundle supports a core on a different host** over a private routed network or VPN. Docker bridge networks are local to a Docker daemon; naming a remote host's network does not connect to it.

Set core discovery/enrollment addresses to DNS names or IPs reachable from the module container. On the core host, expose the required mesh listeners on its private interface and permit module-host access: Auth gRPC (default 9543), Gateway registration gRPC (9643), LCM renewal gRPC (9945) and direct HTTPS enrollment (9947). Use your actual configured ports. The browser Gateway HTTPS URL is the issuer, not a replacement for those mesh endpoints.

In the reverse direction, Gateway and peer services must reach the module host's published HTTP/gRPC ports. `MODULE_ADVERTISE_HOST` sets `FREYA_ADVERTISE_HOST`, so registration advertises that reachable DNS/IP instead of a Docker container IP. `MODULE_BIND_IP` is the private IPv4 interface on the module host where Compose publishes the mesh ports. Use the same external/internal port numbers: the framework override changes the advertised host, not the port. Do not put TLS termination that strips mesh client identity in front of these mTLS listeners. Keep routes/firewall rules restricted to trusted hosts; admin ports remain unpublished. Do not use `localhost` or container-only DNS names for a remote core.

## Optional same-host topology

If the core shares the module's Docker daemon, copy `.env.same-host.example` to `.env` instead. Set its `CORE_NETWORK` to the actual existing network and its issuer to the existing Portal URL. This example sets `COMPOSE_FILE=compose.yaml:compose.same-host.yaml`, so subsequent `docker compose` commands automatically include the local mesh attachment. `MODULE_ADVERTISE_HOST` is the module's network alias and mesh port publication binds loopback. The overlay is not used for a remote core.

**Required module dependencies**: TimescaleDB, Valkey, key-encryption key, Auth, Portal, mesh identity. The local stores in this bundle use workstation credentials. Existing peer modules and their reciprocal service-policy/consumer grants must be configured separately. Inspect the [module reference](modules/ipam.html) before enabling optional integrations.

## Download and configure

[Download the IPAM bundle](downloads/ipam.zip) · [Compose manifest](downloads/ipam/compose.yaml) · [Environment example](downloads/ipam/.env.example)

```sh
unzip ipam.zip
cd ipam
cp .env.example .env
mkdir -p private
chmod 700 private
```

A repository checkout can instead use `deploy/compose/ipam`. Edit `.env` using values from the running core:

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
| `IPAM_VERSION` | Published version compatible with the existing core. |

Review `configs/module.yaml` and `policies/module.yaml`. These are templates: `@@NAME@@` placeholders are deliberately rendered by `configure.py`, because most services do not expand environment variables inside YAML. Edit peer discovery, optional integrations and local infrastructure settings here, then render after every change. The policy's SPIFFE trust domain is rendered too; review exact peer identities and operations rather than granting arbitrary callers.

## Obtain a token from the existing Auth

Enrollment tokens are signed by **Auth** and redeemed with **LCM**. Obtain one through your supported core enrollment workflow. The recorded Auth also provides a workstation CLI that uses its existing configuration/stores/signing keys. For a Compose core using service `auth`, binary `authsvc` and `/app/deploy/container.yaml`, run the following on the **core host** in a private working directory, replacing the core Compose path and trust domain. Create the private output directory first:

```sh
umask 077
mkdir -p private
docker compose -f /ABSOLUTE/PATH/TO/CORE/compose.yaml exec -T auth authsvc mint-enrollment-token -config deploy/container.yaml -spiffe spiffe://YOUR_TRUST_DOMAIN/svc/ipam -tenant 00000000-0000-0000-0000-000000000001 -ttl 30m > private/enrollment.token
chmod 600 private/enrollment.token
```

Match `-tenant` to `TENANT_ID` and your existing mesh CA tenant. Use the actual core service name/configuration path and its usual Compose project/env options. This invokes the existing Auth, not a new Auth installation. On failure, discard the output file and fix the command; never use an empty token. Transfer the token securely to the module host's configured private file path before it expires. Copy the existing **public** mesh CA bundle into `private/ca.pem` through your core's normal trust-distribution mechanism. Do not copy private Auth signing keys or CA keys into this module bundle.

The token is short-lived and single-use. Mint it immediately before initial startup. After successful enrollment the module persists its SVID in its named state volume and renews through LCM; ordinary restarts retain that identity. Deleting state or changing the identity/trust settings requires planned re-enrollment with a fresh token.

## Authorize registration on the existing core

The existing Gateway must allow `spiffe://YOUR_TRUST_DOMAIN/svc/ipam`, route prefixes **`/api/ipam`** and module name **`ipam`**. Update the allow-list through your core's managed configuration. The recorded Gateway CLI accepts a repeatable `-allow` entry; run on the **core host** for a workstation core using service `gateway` and binary `gatewaysvc`:

```sh
docker compose -f /ABSOLUTE/PATH/TO/CORE/compose.yaml exec -T gateway gatewaysvc bootstrap -config deploy/container.yaml -allow 'spiffe://YOUR_TRUST_DOMAIN/svc/ipam=/api/ipam;ipam'
```

Use the running core's configuration/store and its normal deployment procedure. Review this administrative change against your existing allow-list; do not replace it with this module's entry. Gateway enrollment/registration authorization and Auth permission registration are distinct from the user's module roles.

Review Auth and LCM's inbound peer policies for this exact module identity, including permission/role registration, authorization and SVID renewal. Review reciprocal policies on any optional peer module. The bundled policy controls inbound calls to `ipam`; it cannot grant access on another service. A service name in discovery or an enrollment token alone does not grant every RPC.

## Render, validate and start

```sh
python3 configure.py
# Review runtime/config.yaml and runtime/policy.yaml privately.
docker compose config --quiet
docker compose pull
docker compose up -d
docker compose ps -a
docker compose logs --tail=100 ipam
```

The renderer checks required settings and token/CA file presence, creates private runtime files and never prints credential values. Input files, `.env` and runtime configuration are excluded from website downloads. Compose mounts the token and trust bundle read-only. Local initialization jobs prepare only this module's stores/keys; they do not initialize Auth, Gateway or LCM.

Expected startup sequence: local stores become ready, the module verifies the existing LCM identity against the supplied CA and expected SPIFFE ID, exchanges its token for an SVID, persists enrollment state, registers routes/UI with Gateway, and registers permission/role information with Auth. Inspect module logs for enrollment and registration failures. Initialization/runtime logs can contain operational data; handle them privately.

## Verify installation

```sh
docker compose --profile checks run --rm check
docker compose logs --tail=100 ipam
```

The check probes `/healthz` and `/readyz` on private admin port 9820 without publishing it. Confirm successful enrollment and renewal in LCM/module logs, module visibility in your **existing Portal**, and permission catalogue registration in existing Auth. Assign a suitable [module permission](modules/ipam.html#permissions-and-authorization) to a test user and execute a small read. Also check denial for an ungranted action; readiness alone does not establish authorization or external feature acceptance.

## Module-specific setup

Inventory/Warden/Scheduler are existing peer services, not included installations. Configure their discovery addresses and grants, including Inventory host-report consumer access. NET_RAW is enabled for ICMP scans; BMC credentials and endpoint agents remain external.

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
docker compose stop ipam
docker compose up -d
docker compose down
```

`down` removes this project's containers/local network and preserves its named volumes. The running remote Auth/Portal/LCM are unaffected. When using the same-host overlay, its external core network is retained too. `docker compose down -v` destroys this module's stores, keys and SVID state; back them up before a deliberate reset and issue a fresh enrollment token afterward. For permanent removal, retire its existing-core registration/permissions and revoke its workload identity through the core's managed process. Other modules may depend on it.

## Sources and validation scope

[Module source at recorded revision](https://github.com/go-tangra/go-tangra-ipam/tree/df4cab11e3d0a69aac0f90d97b83006dd808ab8a) · [Module reference](modules/ipam.html) · [Upstream stack reference](sources/platform/deploy/stack/README.html).

The configuration/network rendering is authored here from recorded public deployment contracts. Manifest parsing and fixture tests do not establish live enrollment acceptance or image compatibility; test the documented workflow against your chosen core release before production use.

## Key initialization: init-keys.sh

The bundle includes `init-keys.sh`; keep it beside `compose.yaml` when copying or extracting the bundle. You do not need to create the script or run it on the host. Compose mounts it read-only into the one-shot Alpine `keys-init` container and invokes it with `sh /init-keys.sh`, so an executable bit is not required. `docker compose up -d` runs the job automatically. Dependent application/initialization services wait for its successful completion (`service_completed_successfully`).

The script reads 32 random bytes from `/dev/urandom` for each missing or empty key file and writes them as base64 text. It uses a temporary file followed by a rename, sets `umask 077`, and applies file mode `0600`. Existing nonempty key files are preserved; the script does not validate or rotate them. The workstation container runs as root so it can initialize these private named volumes; application containers mount their key volume read-only.

| Named volume | File created inside keys-init | Application path | Purpose |
| --- | --- | --- | --- |
| `ipam-keys` | `/keys/ipam/kek` | `/keys/kek` | ipam key-encryption key (KEK) |

These are application secrets, not enrollment tokens, mesh CA keys or workload certificates. In the existing-core workflow you still supply the Auth-signed enrollment token and public mesh CA separately. The SMS Hermes JWT secret is separate from Auth's platform token signing keys. No generated key is included in the downloadable bundle or printed by the script.

Check initialization without displaying keys:

```sh
docker compose ps -a keys-init
docker compose logs --tail=100 keys-init
```

Expected: the job exits with code 0. An exited one-shot container is normal; a nonzero exit blocks dependent services. For a failure, check the script mount, volume permissions and available disk space, then correct the issue before retrying startup. Do not delete a key volume as a troubleshooting shortcut.

Named volumes preserve these keys across container recreation and `docker compose down`. Back up each key volume together with the database/object data it protects, and restore the matching set. `docker compose down -v` deletes the keys along with this project's other named volumes. A subsequent startup creates new keys, which cannot decrypt data encrypted with the old keys. For an existing-data migration, restore its original keys before startup rather than letting this script generate replacements. Key rotation requires the module's supported migration/rotation procedure; rerunning this initializer is not rotation.
