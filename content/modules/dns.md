# DNS

PowerDNS management, DNS records, IPAM synchronization and ACME challenges.

**Architecture role**: Infrastructure. [See the complete component map](architecture/index.html).

**Documented source**: `10f9be2df98b` · nearest local service tag `v4.3.2` · v4 major. [Repository at this revision](https://github.com/go-tangra/go-tangra-dns/tree/10f9be2df98b2476c2029afcbeb8dec622b30788). Tags are source metadata, not a claim of image publication or cross-module compatibility.


## Permissions and authorization

This catalogue contains **7 permissions** declared by the [module manifest](https://github.com/go-tangra/go-tangra-dns/blob/10f9be2df98b2476c2029afcbeb8dec622b30788/pkg/dnsmanifest/manifest.go) at the revision above. Custom-role references use `module:resource:action`; the manifest and API contract use the local `resource:action` form. The action names are distinct grants: do not assume `manage` automatically includes `read` or another action.

Server configuration, supermaster creation/deletion and cross-tenant restore require platform administration. Tenant owner/admin is not platform-admin. config:manage is absent from the built-in tenant-role grants. Mesh reads, IPAM synchronization and LCM ACME challenges have separate actor allow-lists.

[How to assign and verify permissions](architecture/security.html#assign-and-verify-permissions). Module roles and built-in grant mappings are defined in the linked manifest; review those mappings before assigning a broad role.

| Qualified permission | What it allows |
| --- | --- |
| `dns:zones:read` | List and read zones, record sets and templates, and the live stream |
| `dns:zones:manage` | Create, edit and delete zones and record sets; export zones and send NOTIFY |
| `dns:templates:manage` | Manage zone templates |
| `dns:supermasters:manage` | View supermasters (create/delete also need platform administration) |
| `dns:dashboard:read` | Read the DNS health dashboard |
| `dns:backup:manage` | Export and import tenant DNS data |
| `dns:config:manage` | Edit the DNS server configuration (platform administrators only) |

### dns:zones:read

List and read zones, record sets and templates, and the live stream.

**UI actions**: `read` on `DnsZone`, `DnsRecord`, `DnsTemplate`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Zones, Templates.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/dns/v1/zones` | listZones |
| `GET` | `/api/dns/v1/zones/{id}` | getZone |
| `GET` | `/api/dns/v1/zones/{id}/records` | listRecords |
| `GET` | `/api/dns/v1/templates` | listTemplates |
| `GET` | `/api/dns/v1/templates/{id}` | getTemplate |
| `GET` | `/api/dns/v1/stream` | streamEvents |

**Scope and additional checks**: Server configuration, supermaster creation/deletion and cross-tenant restore require platform administration. Tenant owner/admin is not platform-admin. config:manage is absent from the built-in tenant-role grants. Mesh reads, IPAM synchronization and LCM ACME challenges have separate actor allow-lists.

### dns:zones:manage

Create, edit and delete zones and record sets; export zones and send NOTIFY.

**UI actions**: `create`, `update`, `delete`, `export`, `notify` on `DnsZone`, `DnsRecord`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/dns/v1/zones` | createZone |
| `PUT` | `/api/dns/v1/zones/{id}` | updateZone |
| `DELETE` | `/api/dns/v1/zones/{id}` | deleteZone |
| `GET` | `/api/dns/v1/zones/{id}/export` | exportZone |
| `POST` | `/api/dns/v1/zones/{id}/notify` | notifyZone |
| `POST` | `/api/dns/v1/zones/{id}/records` | upsertRecordSet |
| `PUT` | `/api/dns/v1/zones/{id}/records` | updateRecordSet |
| `DELETE` | `/api/dns/v1/zones/{id}/records` | deleteRecordSet |

**Scope and additional checks**: Server configuration, supermaster creation/deletion and cross-tenant restore require platform administration. Tenant owner/admin is not platform-admin. config:manage is absent from the built-in tenant-role grants. Mesh reads, IPAM synchronization and LCM ACME challenges have separate actor allow-lists.

### dns:templates:manage

Manage zone templates.

**UI actions**: `manage` on `DnsTemplate`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/dns/v1/templates` | createTemplate |
| `PUT` | `/api/dns/v1/templates/{id}` | updateTemplate |
| `DELETE` | `/api/dns/v1/templates/{id}` | deleteTemplate |

**Scope and additional checks**: Server configuration, supermaster creation/deletion and cross-tenant restore require platform administration. Tenant owner/admin is not platform-admin. config:manage is absent from the built-in tenant-role grants. Mesh reads, IPAM synchronization and LCM ACME challenges have separate actor allow-lists.

### dns:supermasters:manage

View supermasters (create/delete also need platform administration).

**UI actions**: `read` on `DnsSupermaster`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Supermasters.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/dns/v1/supermasters` | listSupermasters |
| `POST` | `/api/dns/v1/supermasters` | createSupermaster |
| `GET` | `/api/dns/v1/supermasters/{id}` | getSupermaster |
| `DELETE` | `/api/dns/v1/supermasters/{id}` | deleteSupermaster |

**Scope and additional checks**: Server configuration, supermaster creation/deletion and cross-tenant restore require platform administration. Tenant owner/admin is not platform-admin. config:manage is absent from the built-in tenant-role grants. Mesh reads, IPAM synchronization and LCM ACME challenges have separate actor allow-lists.

### dns:dashboard:read

Read the DNS health dashboard.

**UI actions**: `read` on `DnsDashboard`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Dashboard.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/dns/v1/dashboard` | getDashboard |

**Scope and additional checks**: Server configuration, supermaster creation/deletion and cross-tenant restore require platform administration. Tenant owner/admin is not platform-admin. config:manage is absent from the built-in tenant-role grants. Mesh reads, IPAM synchronization and LCM ACME challenges have separate actor allow-lists.

### dns:backup:manage

Export and import tenant DNS data.

**UI actions**: `manage` on `DnsBackup`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/dns/v1/backup/export` | exportBackup |
| `POST` | `/api/dns/v1/backup/import` | importBackup |

**Scope and additional checks**: Server configuration, supermaster creation/deletion and cross-tenant restore require platform administration. Tenant owner/admin is not platform-admin. config:manage is absent from the built-in tenant-role grants. Mesh reads, IPAM synchronization and LCM ACME challenges have separate actor allow-lists.

### dns:config:manage

Edit the DNS server configuration (platform administrators only).

**UI actions**: `create`, `delete` on `DnsSupermaster`; `manage` on `DnsConfig`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Configuration.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/dns/v1/config` | getServerConfig |
| `PUT` | `/api/dns/v1/config` | updateServerConfig |

**Scope and additional checks**: Server configuration, supermaster creation/deletion and cross-tenant restore require platform administration. Tenant owner/admin is not platform-admin. config:manage is absent from the built-in tenant-role grants. Mesh reads, IPAM synchronization and LCM ACME challenges have separate actor allow-lists.
<div class="guide-actions"><a href="how-to/dns/docker.html">Install with Docker Compose →</a><a href="how-to/dns/native.html">Install without Docker →</a><a href="downloads/dns.zip">Download Compose bundle ↓</a></div>

## Dependencies and integration

**Required**: TimescaleDB, Valkey, PowerDNS APIs, key-encryption key, Auth, Portal, mesh identity.

**Optional or feature-dependent**: IPAM, Prometheus, Docker restart integration.

PowerDNS Authoritative and Recursor must have reachable authenticated APIs. Docker restart integration uses a root-equivalent host socket and allow-listed container names. For native installation, disable that integration and manage PowerDNS through host services.

The list describes infrastructure/features, not every transitive library. Check the linked deployment reference for exact versions, enabled features and peer grants. [Framework dependencies](architecture/dependencies.html) cover the shared Go libraries.

## Runtime and operation

| Item | Reference |
| --- | --- |
| Service binary | `dnssvc` |
| Public example configuration | `deploy/dev.yaml`; adapt endpoints and paths for your environment |
| Native source build | Go `1.26.3`, toolchain `go1.26.8`, Node 22 for UI |
| Image repository | `ghcr.io/go-tangra/go-tangra-dns`; choose a published compatible version |
| Private admin default | `127.0.0.1:9850`; check actual configuration |
| Health and readiness | `/healthz` and `/readyz` on the configured admin listener |
| Web integration | Gateway registration, permission grants and federated UI |

Bootstrap initializes or validates the module's own stores; serving still needs a valid workload identity, reachable dependencies and policy. Logs, readiness, gateway registration and module-specific checks are described in the detailed references below.

## Configuration field index

The following names and types come from the public Go configuration structures. Group names identify nested types, not flat YAML paths. Required values, defaults, cross-field checks and enabled-feature behavior are explained by the module's source/operations references; never assume every listed setting is optional.

| Configuration group | YAML key | Value type |
| --- | --- | --- |
| `Config` | `db` | `DB` |
| `Config` | `valkey` | `Valkey` |
| `Config` | `kek` | `KEK` |
| `Config` | `pdns` | `PDNS` |
| `Config` | `recursor` | `Recursor` |
| `Config` | `docker` | `Docker` |
| `Config` | `managed_files` | `ManagedFiles` |
| `Config` | `metrics` | `Metrics` |
| `Config` | `ipam_sync` | `IPAMSync` |
| `Config` | `acme` | `ACME` |
| `Config` | `records` | `Records` |
| `Config` | `secrets` | `Secrets` |
| `Config` | `events` | `Events` |
| `Config` | `gateway` | `Gateway` |
| `Config` | `mesh_enroll` | `MeshEnroll` |
| `Config` | `limits_dns` | `Limits` |
| `DB` | `dsn` | `string` |
| `DB` | `migrate_dsn` | `string` |
| `DB` | `max_conns` | `int32` |
| `Valkey` | `addresses` | `[]string` |
| `Valkey` | `username` | `string` |
| `Valkey` | `password` | `string` |
| `Valkey` | `allow_plaintext` | `bool` |
| `Valkey` | `ca_file` | `string` |
| `KEK` | `source` | `string` |
| `KEK` | `path` | `string` |
| `KEK` | `env` | `string` |
| `PDNS` | `api_url` | `string` |
| `PDNS` | `server_id` | `string` |
| `PDNS` | `api_key_ref` | `string` |
| `PDNS` | `timeout_seconds` | `int` |
| `PDNS` | `max_response_bytes` | `int64` |
| `PDNS` | `allow_plaintext` | `bool` |
| `PDNS` | `auth_forward_host` | `string` |
| `PDNS` | `auth_forward_port` | `int` |
| `Recursor` | `api_url` | `string` |
| `Recursor` | `server_id` | `string` |
| `Recursor` | `api_key_ref` | `string` |
| `Recursor` | `timeout_seconds` | `int` |
| `Recursor` | `allow_plaintext` | `bool` |
| `Recursor` | `reconcile_interval_seconds` | `int` |
| `Recursor` | `static_forwards` | `[]string` |
| `Docker` | `enabled` | `bool` |
| `Docker` | `socket` | `string` |
| `Docker` | `auth_container` | `string` |
| `Docker` | `recursor_container` | `string` |
| `Docker` | `timeout_seconds` | `int` |
| `ManagedFiles` | `recursor_path` | `string` |
| `ManagedFiles` | `auth_path` | `string` |
| `Metrics` | `prometheus_url` | `string` |
| `Metrics` | `timeout_seconds` | `int` |
| `IPAMSync` | `enabled` | `bool` |
| `IPAMSync` | `tenants` | `[]string` |
| `IPAMSync` | `service` | `string` |
| `IPAMSync` | `default_ttl` | `int` |
| `ACME` | `allowed_caller` | `string` |
| `ACME` | `max_age_seconds` | `int` |
| `Records` | `min_ttl` | `int` |
| `Records` | `max_ttl` | `int` |
| `Records` | `max_values` | `int` |
| `Records` | `max_page_size` | `int` |
| `Secrets` | `warden_service` | `string` |
| `Secrets` | `token_file` | `string` |
| `Secrets` | `refresh_seconds` | `int` |
| `Events` | `enabled` | `bool` |
| `Gateway` | `service` | `string` |
| `Gateway` | `issuer` | `string` |
| `MeshEnroll` | `enabled` | `bool` |
| `MeshEnroll` | `enroll_url` | `string` |
| `MeshEnroll` | `lcm_grpc` | `string` |
| `MeshEnroll` | `tenant_id` | `string` |
| `MeshEnroll` | `token_file` | `string` |
| `MeshEnroll` | `state_file` | `string` |
| `MeshEnroll` | `insecure` | `bool` |
| `Limits` | `max_request_bytes` | `int64` |
| `Limits` | `max_backup_bytes` | `int64` |
| `Limits` | `max_export_bytes` | `int64` |
| `Limits` | `max_page_size` | `int` |

[Configuration structures and validation](https://github.com/go-tangra/go-tangra-dns/blob/10f9be2df98b2476c2029afcbeb8dec622b30788/internal/config/config.go)

## API operation index

These operations are extracted from the module's OpenAPI contract. Read the source contract for request/response schemas, permission checks and exact route bases; internal mesh endpoints must not be treated as anonymous public APIs.

| Method | Contract path | Operation |
| --- | --- | --- |
| `GET` | `/api/dns/v1/zones` | listZones |
| `POST` | `/api/dns/v1/zones` | createZone |
| `GET` | `/api/dns/v1/zones/{id}` | getZone |
| `PUT` | `/api/dns/v1/zones/{id}` | updateZone |
| `DELETE` | `/api/dns/v1/zones/{id}` | deleteZone |
| `GET` | `/api/dns/v1/zones/{id}/export` | exportZone |
| `POST` | `/api/dns/v1/zones/{id}/notify` | notifyZone |
| `GET` | `/api/dns/v1/zones/{id}/records` | listRecords |
| `POST` | `/api/dns/v1/zones/{id}/records` | upsertRecordSet |
| `PUT` | `/api/dns/v1/zones/{id}/records` | updateRecordSet |
| `DELETE` | `/api/dns/v1/zones/{id}/records` | deleteRecordSet |
| `GET` | `/api/dns/v1/templates` | listTemplates |
| `POST` | `/api/dns/v1/templates` | createTemplate |
| `GET` | `/api/dns/v1/templates/{id}` | getTemplate |
| `PUT` | `/api/dns/v1/templates/{id}` | updateTemplate |
| `DELETE` | `/api/dns/v1/templates/{id}` | deleteTemplate |
| `GET` | `/api/dns/v1/supermasters` | listSupermasters |
| `POST` | `/api/dns/v1/supermasters` | createSupermaster |
| `GET` | `/api/dns/v1/supermasters/{id}` | getSupermaster |
| `DELETE` | `/api/dns/v1/supermasters/{id}` | deleteSupermaster |
| `GET` | `/api/dns/v1/config` | getServerConfig |
| `PUT` | `/api/dns/v1/config` | updateServerConfig |
| `GET` | `/api/dns/v1/dashboard` | getDashboard |
| `GET` | `/api/dns/v1/stream` | streamEvents |
| `POST` | `/api/dns/v1/backup/export` | exportBackup |
| `POST` | `/api/dns/v1/backup/import` | importBackup |
| `GET` | `/api/dns/v1/health` | health |

[OpenAPI: api/openapi/dns.yaml](https://github.com/go-tangra/go-tangra-dns/blob/10f9be2df98b2476c2029afcbeb8dec622b30788/api/openapi/dns.yaml)

## Detailed source references

- [README.md](sources/dns/README.html) — captured at `10f9be2df98b`.
- [deploy/README.md](sources/dns/deploy/README.html) — captured at `10f9be2df98b`.

## Limits, diagnostics and recovery

PowerDNS Authoritative and Recursor must have reachable authenticated APIs. Docker restart integration uses a root-equivalent host socket and allow-listed container names. For native installation, disable that integration and manage PowerDNS through host services.

Use the module's operations/deployment reference for retention, backup/restore, refusal behavior, interface examples and feature limitations. The installation guides cover common readiness, identity, registration and storage failures.

## Upstream overview: go-tangra-dns

PowerDNS management plane for the
[go-tangra v4 platform](https://github.com/go-tangra/go-tangra).

Tenants manage **zones and record sets** on one shared PowerDNS Authoritative
server, with global zone-name ownership (a name belongs to one tenant, and the
owner is never revealed to others). A PowerDNS **Recursor** forwards every managed
zone to the authoritative server. Zone templates, supermasters, BIND export and
NOTIFY, **IPAM sync** (IPAM addresses become A/AAAA and PTR records), the
**ACME DNS-01** challenge provider used by lcm, a curated metrics **dashboard**,
live updates and tenant backup come with it. Platform administrators edit the
**server configuration**: the service renders the PowerDNS include files and,
when enabled, restarts the two named PowerDNS containers through the Docker
Engine API. The PowerDNS API keys are secret **references** (warden in
production) that are resolved at use time and never logged.

Operations: [`deploy/README.md`](sources/dns/deploy/README.html).
Design history: `specs/015-dns-service`.

## Place in the platform

```
go-tangra/go-tangra          platform module + @go-tangra/ui kit
        |
go-tangra-auth  <---->  go-tangra-portal (gateway)  <---->  go-tangra-lcm
                                  |                              |  ACME DNS-01
go-tangra-ipam --(events)-->  go-tangra-dns  <-------------------+
                                  |
              PowerDNS Authoritative + Recursor (HTTP APIs, include files)
                                  |
                          go-tangra-warden (PowerDNS API keys)
```

- Built on `github.com/go-tangra/go-tangra/v4` (mTLS transports, identity,
  service policy, audit, observability).
- Verifies platform tokens and checks permissions through the auth SDK
  (`github.com/go-tangra/go-tangra-auth/sdk/v4`).
- Registers with the gateway through the portal SDK
  (`github.com/go-tangra/go-tangra-portal/sdk/v4`), which fronts the browser API
  (`/api/dns`) and the federated UI remote.
- Enrolls for its SVID with lcm over the network
  (`github.com/go-tangra/go-tangra-lcm/sdk/v4`), and serves lcm's DNS-01
  challenges (`dns.v1.Challenges`, only for the configured lcm SPIFFE ID).
- Reads IPAM addresses and subnets through the ipam SDK
  (`github.com/go-tangra/go-tangra-ipam/sdk/v4`) when it consumes
  `ipam.ip_address.*` events.
- Resolves `warden:` secret references through the warden SDK
  (`github.com/go-tangra/go-tangra-warden/sdk/v4`).

The repository holds one Go module, `github.com/go-tangra/go-tangra-dns/v4`.
Other services call it through `pkg/dnsclient` and the `dns.v1` protos
(not proxied by the gateway).

## Layout

| Path | What |
|------|------|
| `api/openapi/dns.yaml` | browser API contract (served under `/api/dns`) |
| `api/proto/dns/v1/` | module gRPC surface (`Zones/{List,Get,FindForName}`, `Challenges/{Present,CleanUp}`) |
| `internal/config` | configuration + validation (secure defaults, named opt-outs) |
| `internal/store`, `internal/repo` | TimescaleDB schema (RLS), repositories; `internal/memstore` is the in-memory test double |
| `internal/pdns`, `internal/recursor` | PowerDNS Authoritative and Recursor HTTP API clients (with fakes) |
| `internal/zones`, `internal/records`, `internal/templates`, `internal/supermasters`, `internal/validate` | domain services and record validation |
| `internal/dnsconf` | server configuration: include-file rendering, write-if-changed files, restart-only Docker client |
| `internal/ipamsync` | IPAM address events to A/AAAA/PTR records |
| `internal/acmechallenge` | ACME DNS-01 provider for lcm |
| `internal/secrets` | `warden:` / `file:` secret references with refresh |
| `internal/sealed` | envelope encryption with the KEK |
| `internal/authz` | permission and tenant checks |
| `internal/events`, `internal/stream` | events on the platform bus, live stream |
| `internal/backup`, `internal/dashboard`, `internal/metrics`, `internal/audit` | backup export/import, dashboard, metrics, audit |
| `internal/httpapi`, `internal/grpcapi` | browser and service APIs |
| `internal/app`, `cmd/dnssvc` | wiring and the service binary (serve, `bootstrap`, `version`) |
| `pkg/dnsmanifest` | gateway manifest, module roles and built-in role grants |
| `pkg/dnsclient` | Go client other services use |
| `testdata` | PowerDNS API, record and IPAM event fixtures |
| `tests/integration` | real TimescaleDB, Valkey and PowerDNS (testcontainers); `challengesrv` for lcm's suite |
| `tests/contract`, `tests/security` | API contract and security/redaction suites |
| `deploy` | service policy, PowerDNS base configs (`deploy/pdns`), operations notes |
| `ui/` | Vue 3 + FlyonUI federated remote on `@go-tangra/ui` |

## Build and test

You need Go 1.26, Node 22, Docker (for the integration suite and the image), and a
GitHub token with `read:packages` to install `@go-tangra/ui` from GitHub Packages.

```bash
go build ./... && go vet ./... && go test -race ./...
buf lint
make test-integration                     # -tags integration: TimescaleDB, Valkey, PowerDNS 4.9 + Recursor 5.3 via testcontainers
make lint cover vuln redaction-scan

cd ui
export NODE_AUTH_TOKEN=$(gh auth token)   # ui/.npmrc only references this variable
npm ci && npm run lint && npm run test:unit && npm run build
```

The integration suite runs the pinned PowerDNS images on a shared Docker network
and checks real DNS answers from the authoritative server and through the
recursor, including the IPAM event path over Valkey. `DNS_IT_ADMIN_DSN` points it
at an existing TimescaleDB server instead of a container. It skips when Docker is
not available.

The unit coverage gate (`make cover`) excludes generated code, SQL bindings and
wiring, which the integration suite covers instead. The Playwright specs in
`ui/tests/e2e` need a running platform and operator credentials; they skip
otherwise.

## Run

The service runs in the go-tangra platform stack (`deploy/stack` in
[go-tangra](https://github.com/go-tangra/go-tangra)), next to TimescaleDB, Valkey,
ipam and the `pdns-auth` / `pdns-recursor` containers. The stack mounts its
configuration at `/app/deploy/container.yaml` and the development key-encryption
key at `/app/deploy/kek.dev`. Its `dns-secrets-init` job generates the PowerDNS
API keys into the `dns-secrets` volume (`file:/secrets/pdns-*.key`) and writes the
API include snippets; the service renders its own include files into the shared
`pdns-auth-conf` / `pdns-recursor-conf` volumes. `deploy/kek.dev` in this
repository is a development key only; it is excluded from the image.

```bash
dnssvc bootstrap -config deploy/container.yaml    # apply migrations and exit
dnssvc -config deploy/container.yaml              # serve (applies migrations)
```

Listeners: gRPC `:9965` and HTTP `:9966` on the mesh (mTLS), admin `:9850`
(`/healthz`, `/readyz`). See `specs/015-dns-service/quickstart.md` for the
end-to-end walkthrough.

Container restart is off by default (`docker.enabled: false`). When enabled it
needs the Docker socket, which is root-equivalent on the host; the client only
restarts the two containers named in `docker.auth_container` and
`docker.recursor_container`, and only platform administrators can trigger it.
Production should put an API-filtering socket proxy in front of it
(`deploy/README.md`).

## Container image

The image is `ghcr.io/go-tangra/go-tangra-dns`, built by
`.github/workflows/ci.yaml`. It carries `dnssvc` with the embedded UI remote.

```bash
docker buildx build --secret id=npm_token,env=NODE_AUTH_TOKEN \
  --build-arg APP_VERSION=4.0.0 -t go-tangra-dns:dev .
docker run --rm go-tangra-dns:dev version
```

The image runs `dnssvc -config deploy/container.yaml` as user `app`
(uid 10001). It contains no configuration and no key material: deployments mount
their own `deploy/container.yaml`, key-encryption key and PowerDNS API key
references. `deploy/pdns/` holds the reference PowerDNS base configs; the
service does not read them at run time (the platform stack carries its own copy).

## API permissions

`zones:read/manage`, `templates:manage`, `supermasters:manage`, `dashboard:read`,
`backup:manage`, and `config:manage` (platform administrators only). The gateway
enforces the per-route permission from the manifest; the module then checks the
tenant scope.

## Roles

The module registers its permissions with auth at start and every five
minutes, together with ready-made module roles that auth offers in every
tenant (locked; administrators assign them or clone them into custom roles):

| Role | Display name | Permissions |
|---|---|---|
| `administrator` | DNS administrator | every tenant permission: `zones:read/manage`, `templates:manage`, `supermasters:manage`, `dashboard:read`, `backup:manage` (not `config:manage`) |
| `viewer` | DNS viewer | `zones:read`, `dashboard:read` |

Built-in role grants (scoped to the DNS module by auth,
`pkg/dnsmanifest.Grants`): `owner` and `admin` hold the administrator set;
`operator`, `member` and `auditor` the viewer set. No tenant role holds
`config:manage`.

## Versioning

- Releases are tagged `vX.Y.Z`. CI publishes the image as `X.Y.Z`, `X.Y`, `X`
  and `sha-<short>`. There is no `latest` tag.
- v4.0.0 rebuilds the service on the go-tangra v4 platform. The previous line
  stays on the `v3` branch and its `v3.x` tags.
