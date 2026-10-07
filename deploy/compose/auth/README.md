**Initial core bootstrap only.** If Auth/Portal/LCM already run, use the add-on module bundles to enroll services; do not start a second core from this directory.

# Standalone Auth Compose installation

Includes an isolated Auth/Portal/LCM control plane and the dependencies of the enabled module features. No existing Go-Tangra stack or sibling source checkout is required. The framework and SDKs are libraries rather than standalone daemons.

This is a local workstation configuration (development database/Valkey/object-store credentials, self-signed browser TLS and private internal plaintext infrastructure). Mesh enrollment verifies the generated CA. Encryption keys are generated once in private named volumes; no private keys are shipped in this bundle.

```sh
cp .env.example .env
# Edit .env: operator email, available image versions, and any required integration values.
docker compose config --quiet
docker compose pull
docker compose up -d
docker compose logs auth-bootstrap
docker compose --profile checks run --rm check
```

Accept the operator invitation from auth-bootstrap logs or http://localhost:8025 and sign in at https://localhost:8443. The named project is `tangra-auth`. Use only the versions available in your registry; recorded local tags are not a verified compatible release matrix.

Stop the deployment with `docker compose stop`, start it again with `docker compose up -d`, and remove its containers with `docker compose down`. Named volumes preserve databases, objects, keys, identity and bootstrap state. **`docker compose down -v` deletes that state** and requires fresh initialization. When Vault is included, its single-node persistent file backend and private recovery volume survive restart; auto-unseal with co-located recovery material is for workstation use.

No admin ports or Docker daemon socket are published. The `check` service probes the module's own network namespace on private admin port 9190. For multiple simultaneous bundles, change conflicting host ports and matching origins in configs/*.yaml. DNS configuration saves require `docker compose restart pdns-auth pdns-recursor` to apply managed server files; Docker-socket restart control is disabled.

For Asterisk, populate `ASTERISK_CDR_DSN` with a reachable SELECT-only PBX source. Its bundled registration database is separate; PBX data is never initialized or migrated. For SMS, create a provider/client through the management UI before sending; no real carrier is included. Configure optional external targets (AMI, SMTP delivery, qualified signing, real ACME, endpoint agents) separately.

Main service: `auth`. Included application services: auth, gateway, lcm.
Source review and Compose validation do not establish clean-environment deployment acceptance; see the website Docker guide for module-specific checks and source links.

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
