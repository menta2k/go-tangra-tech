# Install Portal / Gateway with Docker Compose

**Core bootstrap only**: this bundle creates an initial core. If Auth/Portal/LCM are already running, manage upgrades or replacement through that existing core; do not start this bundle to add a regular module. Regular module guides enroll into your existing core.

Install `gateway` using its standalone Compose bundle. It includes an isolated Auth/Portal/LCM control plane, required infrastructure and the enabled feature dependencies: **auth, gateway, lcm**. An existing Go-Tangra installation or module source checkout is not required.

## Prerequisites and dependencies

Use Docker Engine with Compose v2 or later and registry access. Check `docker version` and `docker compose version`, sufficient disk/memory and the host ports required by the included services. The bundle is for a local workstation: it uses development infrastructure credentials and self-signed browser TLS. Its service mesh verifies the generated CA during enrollment.

The defaults record local v4 service tags, including `v4.6.0` for Portal / Gateway; confirm image availability and compatibility before starting. Each included application has its own version variable in `.env.example`.

**Module dependencies**: Auth, LCM or supplied SVID, TimescaleDB, Valkey. The bundle provisions the local control plane and infrastructure for its enabled features. External business systems, provider accounts and hardware targets still need their own configuration.

## Download the standalone bundle

[Download the complete Portal / Gateway Compose bundle](downloads/portal.zip) · [View compose.yaml](downloads/portal/compose.yaml) · [View environment example](downloads/portal/.env.example)

Download the ZIP, then extract it:

```sh
unzip portal.zip
cd portal
cp .env.example .env
```

Alternatively, from a checkout of this documentation repository, use `cd deploy/compose/portal` and copy `.env.example` there. Keep the whole bundle together: the Compose file mounts its relative `configs/`, `policies/` and initialization files.

## Configure the installation

Edit `.env` to set `OPERATOR_EMAIL` to your first operator's address and choose published compatible versions for each application. The default gateway is `https://localhost:8443`; Mailpit is `http://localhost:8025`. The project name is `tangra-portal` and its network/volumes are isolated from other bundles.

If another bundle is running, change conflicting host port variables and the matching issuer/public/allowed-origin URLs in `configs/*.yaml`. Changing only a host port leaves the browser authentication URLs inconsistent. No admin ports or Docker daemon socket are published.

Review `configs/gateway.yaml` and the policies before enabling external integrations. Bootstrap creates database roles/schema, mesh identities, enrollment tokens and gateway registration grants. Keys are generated once inside private named volumes and retained across restarts; no private key is included in the download.

## Validate, bootstrap and start

From the bundle directory:

```sh
docker compose config --quiet
docker compose pull
docker compose up -d
docker compose ps -a
docker compose logs --tail=100 auth-bootstrap gateway
```

Expected: configuration validation succeeds, images pull, initialization jobs exit successfully and services stay running. `depends_on` gates store readiness and completed bootstrap/token jobs. Read failed job logs before retrying. The default project contains only this module's application/dependency selection, rather than the entire platform stack.

Accept the invitation from `auth-bootstrap` logs or development Mailpit, set the password and TOTP, and sign in to the gateway. Its browser certificate is self-signed for localhost; trust it only on your own development workstation.

## Verify installation

The included check service uses the module's own network namespace to probe private admin port **9290**. Run:

```sh
docker compose --profile checks run --rm check
docker compose logs --tail=100 gateway
```

Expected: `Health and readiness passed`, followed by exit status 0. The check retries startup readiness for up to two minutes. No admin port needs to be published. Then sign in with a user holding Portal / Gateway's permissions, confirm the module is registered in the gateway, and perform a small read operation from its [module reference](modules/portal.html). Test configured external integrations separately.

## Troubleshooting

| Symptom | Check and remedy |
| --- | --- |
| Compose rejects an environment value | Populate the required `.env` fields; Asterisk needs a read-only CDR DSN. Run `docker compose config --quiet` again. |
| Image pull fails | Select a published compatible version for that service in `.env`; local source tags alone do not prove registry availability. |
| A bootstrap job fails | Use `docker compose logs JOB_NAME`; check store health, role/schema setup, paths and the generated key volumes before retrying `docker compose up -d`. |
| Module is not registered | Check `gateway` logs, readiness, its persisted enrollment state, and the bundled gateway allow-list/policy. A spent token cannot replace deleted identity state. |
| Browser sign-in URL is wrong | Match host port changes with public/issuer/origin values in the configuration files, then recreate affected services. |
| Sealed records fail after restore | Restore matching key volumes along with database/object data. Never overwrite an existing key with a new random key. |
| Vault is sealed after restart | Where included, check `docker compose logs vault`; the private recovery volume must match `vault-data`. Recreate the dependent AppRole job with `docker compose up -d --force-recreate vault-init warden`. |
| A port is already occupied | Stop the other bundle, or change the conflicting ports and matching configuration origins consistently. |

## Stop and remove

Stop only this service while preserving data:

```sh
docker compose stop gateway
```

Stop all services in the standalone installation, then bring them back:

```sh
docker compose stop
docker compose up -d
```

Remove containers/network while preserving persistent volumes:

```sh
docker compose down
```

**Destructive reset**: `docker compose down -v` also deletes databases, objects, mesh CA/identity, keys, tokens and any Vault/registration state in the bundle. Back up the complete set before deliberately resetting; this requires fresh initialization. The external PBX/carrier/targets are never cleanup targets.

## Sources and scope

[Module README](sources/portal/README.html) · [Module configuration and interfaces](modules/portal.html) · [Platform stack reference](sources/platform/deploy/stack/README.html)

This bundle adapts the recorded public platform/service deployment contracts into a standalone directory. Its added Compose integration is maintained in this repository; the upstream base stack does not contain every later module. Configuration and integrity validation do not establish live deployment acceptance or a tested release matrix.

## Key initialization: init-keys.sh

The bundle includes `init-keys.sh`; keep it beside `compose.yaml` when copying or extracting the bundle. You do not need to create the script or run it on the host. Compose mounts it read-only into the one-shot Alpine `keys-init` container and invokes it with `sh /init-keys.sh`, so an executable bit is not required. `docker compose up -d` runs the job automatically. Dependent application/initialization services wait for its successful completion (`service_completed_successfully`).

The script reads 32 random bytes from `/dev/urandom` for each missing or empty key file and writes them as base64 text. It uses a temporary file followed by a rename, sets `umask 077`, and applies file mode `0600`. Existing nonempty key files are preserved; the script does not validate or rotate them. The workstation container runs as root so it can initialize these private named volumes; application containers mount their key volume read-only.

| Named volume | File created inside keys-init | Application path | Purpose |
| --- | --- | --- | --- |
| `auth-keys` | `/keys/auth/kek` | `/keys/kek` | auth key-encryption key (KEK) |
| `lcm-keys` | `/keys/lcm/kek` | `/keys/kek` | lcm key-encryption key (KEK) |

These are application secrets, not enrollment tokens, mesh CA keys or workload certificates. In the existing-core workflow you still supply the Auth-signed enrollment token and public mesh CA separately. The SMS Hermes JWT secret is separate from Auth's platform token signing keys. No generated key is included in the downloadable bundle or printed by the script.

Check initialization without displaying keys:

```sh
docker compose ps -a keys-init
docker compose logs --tail=100 keys-init
```

Expected: the job exits with code 0. An exited one-shot container is normal; a nonzero exit blocks dependent services. For a failure, check the script mount, volume permissions and available disk space, then correct the issue before retrying startup. Do not delete a key volume as a troubleshooting shortcut.

Named volumes preserve these keys across container recreation and `docker compose down`. Back up each key volume together with the database/object data it protects, and restore the matching set. `docker compose down -v` deletes the keys along with this project's other named volumes. A subsequent startup creates new keys, which cannot decrypt data encrypted with the old keys. For an existing-data migration, restore its original keys before startup rather than letting this script generate replacements. Key rotation requires the module's supported migration/rotation procedure; rerunning this initializer is not rotation.
