# Add Scheduler to an existing Go-Tangra core

Runs only `scheduler` and its local infrastructure. Auth, Portal/Gateway, LCM and peer modules must already be reachable. Docker networks do not span hosts; default installation uses routed core addresses and publishes the module mesh listeners on its private host interface. This is a workstation example with development store credentials; choose published compatible images and adapt infrastructure for production.

1. Set routable core endpoints in .env. The default compose.yaml supports a core on another host over a private routed network/VPN. Set MODULE_ADVERTISE_HOST to the module host DNS/IP reachable from the core and MODULE_BIND_IP to that host’s private interface IP. Mesh ports are published unchanged, matching their registered ports; keep admin listeners private. CORE_NETWORK is only used by the optional compose.same-host.yaml overlay when the core shares this Docker daemon.
2. Using the existing Auth signing keys, mint a short-lived token for `spiffe://YOUR_TRUST_DOMAIN/svc/scheduler`. Save it privately at the configured ENROLLMENT_TOKEN_FILE path, and copy the existing mesh CA bundle to MESH_CA_FILE. Never copy a CA private key. The download contains neither token nor CA material.
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
docker compose logs --tail=100 scheduler
docker compose --profile checks run --rm check
```

Sign into your existing Portal, confirm Scheduler appears, assign its module permissions in Auth and perform an authorized read. Enrollment obtains identity, registration announces routes/UI and Auth permissions, and resource/user grants remain separate. Readiness alone does not prove those business operations.

Identity is persisted in `scheduler-state`; keys and stores also use named volumes. A token is short-lived and single-use: restarting preserves state, but deleting identity requires a fresh token. `docker compose down` removes these containers and the local network, preserves volumes, and does not touch the remote core; the optional same-host external network is also retained. `docker compose down -v` irreversibly deletes this module's data/keys/identity; revoke its identity and retire its gateway/permission registrations deliberately when uninstalling.

Existing peers are not started automatically. For Asterisk supply SELECT-only external PBX CDR credentials; registration storage is separate. For SMS configure a carrier/client. DNS socket restart control is disabled; restart its local PowerDNS services explicitly. Optional integrations require their own configuration and acceptance checks.

No live deployment acceptance or published release compatibility is claimed. Documentation and templates are derived from the recorded public sources.
