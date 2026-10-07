# Add Signing to an existing Go-Tangra core

Runs only `signing` and its local infrastructure. Auth, Portal/Gateway, LCM and peer modules must already be reachable. Docker networks do not span hosts; default installation uses routed core addresses and publishes the module mesh listeners on its private host interface. This is a workstation example with development store credentials; choose published compatible images and adapt infrastructure for production.

1. Set routable core endpoints in .env. The default compose.yaml supports a core on another host over a private routed network/VPN. Set MODULE_ADVERTISE_HOST to the module host DNS/IP reachable from the core and MODULE_BIND_IP to that host’s private interface IP. Mesh ports are published unchanged, matching their registered ports; keep admin listeners private. CORE_NETWORK is only used by the optional compose.same-host.yaml overlay when the core shares this Docker daemon.
2. Using the existing Auth signing keys, mint a short-lived token for `spiffe://YOUR_TRUST_DOMAIN/svc/signing`. Save it privately at the configured ENROLLMENT_TOKEN_FILE path, and copy the existing mesh CA bundle to MESH_CA_FILE. Never copy a CA private key. The download contains neither token nor CA material.
For same-host installation, use .env.same-host.example as .env and set CORE_NETWORK to a network on this Docker daemon. Its COMPOSE_FILE setting enables compose.same-host.yaml automatically.

3. Authorize that exact SPIFFE identity/prefix on the existing gateway and allow required RPCs on Auth/LCM and other peers. Do this through the existing core's managed configuration, not by running a new core bootstrap job. See the website guide for registration instructions.
4. Configure required existing peer modules and reciprocal policy/consumer grants. Templates retain peer discovery addresses from the recorded source; edit configs/module.yaml for your topology and optional feature settings. Run configure.py after every template/.env change. Runtime YAML is rendered explicitly because most services do not expand environment variables in YAML.

```sh
cp .env.example .env
# Edit .env, install the enrollment token/CA files, and review templates/policies.
python3 configure.py
docker compose config --quiet
docker compose pull
docker compose up -d
docker compose logs --tail=100 signing
docker compose --profile checks run --rm check
```

Sign into your existing Portal, confirm Signing appears, assign its module permissions in Auth and perform an authorized read. Enrollment obtains identity, registration announces routes/UI and Auth permissions, and resource/user grants remain separate. Readiness alone does not prove those business operations.

Identity is persisted in `signing-state`; keys and stores also use named volumes. A token is short-lived and single-use: restarting preserves state, but deleting identity requires a fresh token. `docker compose down` removes these containers and the local network, preserves volumes, and does not touch the remote core; the optional same-host external network is also retained. `docker compose down -v` irreversibly deletes this module's data/keys/identity; revoke its identity and retire its gateway/permission registrations deliberately when uninstalling.

Existing peers are not started automatically. For Asterisk supply SELECT-only external PBX CDR credentials; registration storage is separate. For SMS configure a carrier/client. DNS socket restart control is disabled; restart its local PowerDNS services explicitly. Optional integrations require their own configuration and acceptance checks.

No live deployment acceptance or published release compatibility is claimed. Documentation and templates are derived from the recorded public sources.

## Key initialization: init-keys.sh

The bundle includes `init-keys.sh`; keep it beside `compose.yaml` when copying or extracting the bundle. You do not need to create the script or run it on the host. Compose mounts it read-only into the one-shot Alpine `keys-init` container and invokes it with `sh /init-keys.sh`, so an executable bit is not required. `docker compose up -d` runs the job automatically. Dependent application/initialization services wait for its successful completion (`service_completed_successfully`).

The script reads 32 random bytes from `/dev/urandom` for each missing or empty key file and writes them as base64 text. It uses a temporary file followed by a rename, sets `umask 077`, and applies file mode `0600`. Existing nonempty key files are preserved; the script does not validate or rotate them. The workstation container runs as root so it can initialize these private named volumes; application containers mount their key volume read-only.

| Named volume | File created inside keys-init | Application path | Purpose |
| --- | --- | --- | --- |
| `signing-keys` | `/keys/signing/kek` | `/keys/kek` | signing key-encryption key (KEK) |

These are application secrets, not enrollment tokens, mesh CA keys or workload certificates. In the existing-core workflow you still supply the Auth-signed enrollment token and public mesh CA separately. The SMS Hermes JWT secret is separate from Auth's platform token signing keys. No generated key is included in the downloadable bundle or printed by the script.

Check initialization without displaying keys:

```sh
docker compose ps -a keys-init
docker compose logs --tail=100 keys-init
```

Expected: the job exits with code 0. An exited one-shot container is normal; a nonzero exit blocks dependent services. For a failure, check the script mount, volume permissions and available disk space, then correct the issue before retrying startup. Do not delete a key volume as a troubleshooting shortcut.

Named volumes preserve these keys across container recreation and `docker compose down`. Back up each key volume together with the database/object data it protects, and restore the matching set. `docker compose down -v` deletes the keys along with this project's other named volumes. A subsequent startup creates new keys, which cannot decrypt data encrypted with the old keys. For an existing-data migration, restore its original keys before startup rather than letting this script generate replacements. Key rotation requires the module's supported migration/rotation procedure; rerunning this initializer is not rotation.
