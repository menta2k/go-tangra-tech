# Asterisk

Read-only PBX observation, call history, recordings and RTP diagnostics.

**Architecture role**: Communications. [See the complete component map](architecture/index.html).

**Documented source**: `eabd8b2810fa` · nearest local service tag `v4.0.0` · v4 major. [Repository at this revision](https://github.com/go-tangra/go-tangra-asterisk/tree/eabd8b2810fa39b670050d363ae62d7fde78600e). Tags are source metadata, not a claim of image publication or cross-module compatibility.


## Permissions and authorization

This catalogue contains **6 permissions** declared by the [module manifest](https://github.com/go-tangra/go-tangra-asterisk/blob/eabd8b2810fa39b670050d363ae62d7fde78600e/pkg/asteriskmanifest/manifest.go) at the revision above. Custom-role references use `module:resource:action`; the manifest and API contract use the local `resource:action` form. The action names are distinct grants: do not assume `manage` automatically includes `read` or another action.

The observer is pinned to one PBX and tenant and reads the PBX through SELECT-only credentials. Recordings have their own permission and are excluded from the viewer role; investigator includes them. Live, registration, recordings and monitoring still require their respective configured integrations.

[How to assign and verify permissions](architecture/security.html#assign-and-verify-permissions). Module roles and built-in grant mappings are defined in the linked manifest; review those mappings before assigning a broad role.

| Qualified permission | What it allows |
| --- | --- |
| `asterisk:calls:read` | Read calls |
| `asterisk:stats:read` | Read stats |
| `asterisk:registration:read` | Read registration |
| `asterisk:live:read` | Read live |
| `asterisk:recordings:read` | Read recordings |
| `asterisk:dashboard:read` | Read dashboard |

### asterisk:calls:read

Read calls.

**UI actions**: `read` on `AsteriskCalls`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Call history.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/asterisk/capabilities` | calls__capabilities |
| `GET` | `/api/asterisk/calls` | calls__calls |
| `GET` | `/api/asterisk/calls/{linkedid}` | calls__calls_linkedid |

**Scope and additional checks**: The observer is pinned to one PBX and tenant and reads the PBX through SELECT-only credentials. Recordings have their own permission and are excluded from the viewer role; investigator includes them. Live, registration, recordings and monitoring still require their respective configured integrations.

### asterisk:stats:read

Read stats.

**UI actions**: `read` on `AsteriskStats`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Overview, Extensions.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/asterisk/stats/overview` | stats__stats_overview |
| `GET` | `/api/asterisk/stats/extensions` | stats__stats_extensions |
| `GET` | `/api/asterisk/stats/extensions/{extension}` | stats__stats_extensions_extension |
| `GET` | `/api/asterisk/stats/ringgroups/{ring_group}` | stats__stats_ringgroups_ring_group |
| `GET` | `/api/asterisk/directory/extensions` | stats__directory_extensions |

**Scope and additional checks**: The observer is pinned to one PBX and tenant and reads the PBX through SELECT-only credentials. Recordings have their own permission and are excluded from the viewer role; investigator includes them. Live, registration, recordings and monitoring still require their respective configured integrations.

### asterisk:registration:read

Read registration.

**UI actions**: `read` on `AsteriskRegistration`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/asterisk/registration/status/{extension}` | registration__registration_status_extension |
| `GET` | `/api/asterisk/registration/events` | registration__registration_events |
| `GET` | `/api/asterisk/registration/online` | registration__registration_online |

**Scope and additional checks**: The observer is pinned to one PBX and tenant and reads the PBX through SELECT-only credentials. Recordings have their own permission and are excluded from the viewer role; investigator includes them. Live, registration, recordings and monitoring still require their respective configured integrations.

### asterisk:live:read

Read live.

**UI actions**: `read` on `AsteriskLive`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Live calls.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/asterisk/live/calls` | live__live_calls |
| `GET` | `/api/asterisk/live/calls/stream` | live__live_calls_stream |

**Scope and additional checks**: The observer is pinned to one PBX and tenant and reads the PBX through SELECT-only credentials. Recordings have their own permission and are excluded from the viewer role; investigator includes them. Live, registration, recordings and monitoring still require their respective configured integrations.

### asterisk:recordings:read

Read recordings.

**UI actions**: `read` on `AsteriskRecordings`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/asterisk/recordings/{linkedid}` | recordings__recordings_linkedid |

**Scope and additional checks**: The observer is pinned to one PBX and tenant and reads the PBX through SELECT-only credentials. Recordings have their own permission and are excluded from the viewer role; investigator includes them. Live, registration, recordings and monitoring still require their respective configured integrations.

### asterisk:dashboard:read

Read dashboard.

**UI actions**: `read` on `AsteriskDashboard`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Monitoring.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/asterisk/dashboard/query` | dashboard__dashboard_query |
| `GET` | `/api/asterisk/dashboard/query_range` | dashboard__dashboard_query_range |

**Scope and additional checks**: The observer is pinned to one PBX and tenant and reads the PBX through SELECT-only credentials. Recordings have their own permission and are excluded from the viewer role; investigator includes them. Live, registration, recordings and monitoring still require their respective configured integrations.
<div class="guide-actions"><a href="how-to/asterisk/docker.html">Install with Docker Compose →</a><a href="how-to/asterisk/native.html">Install without Docker →</a><a href="downloads/asterisk.zip">Download Compose bundle ↓</a></div>

## Dependencies and integration

**Required**: read-only PBX MySQL CDR, Auth, Portal, mesh identity.

**Optional or feature-dependent**: module-owned registration MySQL, AMI, read-only recordings, dedicated Prometheus.

This read-only observer binds one PBX to one tenant. Grant SELECT only on the PBX source. Registration history, if enabled, writes to a separate module-owned MySQL database. Recordings are read-only. The supplied Compose file needs an existing mesh network; a systemd unit is supplied for native deployment.

The list describes infrastructure/features, not every transitive library. Check the linked deployment reference for exact versions, enabled features and peer grants. [Framework dependencies](architecture/dependencies.html) cover the shared Go libraries.

## Runtime and operation

| Item | Reference |
| --- | --- |
| Service binary | `asterisksvc` |
| Public example configuration | `configs/dev.yaml`; adapt endpoints and paths for your environment |
| Native source build | Go `1.26.3`, toolchain `go1.26.8`, Node 22 for UI |
| Image repository | `ghcr.io/go-tangra/go-tangra-asterisk`; choose a published compatible version |
| Private admin default | `127.0.0.1:9094`; check actual configuration |
| Health and readiness | `/healthz` and `/readyz` on the configured admin listener |
| Web integration | Gateway registration, permission grants and federated UI |

Bootstrap initializes or validates the module's own stores; serving still needs a valid workload identity, reachable dependencies and policy. Logs, readiness, gateway registration and module-specific checks are described in the detailed references below.

## Configuration field index

The following names and types come from the public Go configuration structures. Group names identify nested types, not flat YAML paths. Required values, defaults, cross-field checks and enabled-feature behavior are explained by the module's source/operations references; never assume every listed setting is optional.

| Configuration group | YAML key | Value type |
| --- | --- | --- |
| `Config` | `binding` | `Binding` |
| `Config` | `ami` | `AMI` |
| `Config` | `gateway` | `Gateway` |
| `Config` | `mesh_enroll` | `MeshEnroll` |
| `Config` | `query_timeout_seconds` | `int` |
| `Config` | `stream_seconds` | `int` |
| `Binding` | `tenant_id` | `string` |
| `Binding` | `pbx_id` | `string` |
| `Binding` | `cdr_dsn` | `string` |
| `Binding` | `config_dsn` | `string` |
| `Binding` | `registration_dsn` | `string` |
| `Binding` | `adopt_registration` | `bool` |
| `Binding` | `registration_retention_days` | `int` |
| `Binding` | `recording_root` | `string` |
| `Binding` | `timezone` | `string` |
| `Binding` | `source_timezone` | `string` |
| `Binding` | `monitoring_url` | `string` |
| `Binding` | `monitoring_dedicated` | `bool` |
| `MeshEnroll` | `enabled` | `bool` |
| `MeshEnroll` | `enroll_url` | `string` |
| `MeshEnroll` | `lcm_grpc` | `string` |
| `MeshEnroll` | `tenant_id` | `string` |
| `MeshEnroll` | `token_file` | `string` |
| `MeshEnroll` | `state_file` | `string` |
| `MeshEnroll` | `insecure` | `bool` |
| `AMI` | `address` | `string` |
| `AMI` | `username` | `string` |
| `AMI` | `secret` | `string` |
| `AMI` | `tls` | `bool` |
| `AMI` | `enabled` | `bool` |
| `Gateway` | `service` | `string` |
| `Gateway` | `issuer` | `string` |

[Configuration structures and validation](https://github.com/go-tangra/go-tangra-asterisk/blob/eabd8b2810fa39b670050d363ae62d7fde78600e/internal/config/config.go)

## API operation index

These operations are extracted from the module's OpenAPI contract. Read the source contract for request/response schemas, permission checks and exact route bases; internal mesh endpoints must not be treated as anonymous public APIs.

| Method | Contract path | Operation |
| --- | --- | --- |
| `GET` | `/api/asterisk/capabilities` | calls__capabilities |
| `GET` | `/api/asterisk/calls` | calls__calls |
| `GET` | `/api/asterisk/calls/{linkedid}` | calls__calls_linkedid |
| `GET` | `/api/asterisk/stats/overview` | stats__stats_overview |
| `GET` | `/api/asterisk/stats/extensions` | stats__stats_extensions |
| `GET` | `/api/asterisk/stats/extensions/{extension}` | stats__stats_extensions_extension |
| `GET` | `/api/asterisk/stats/ringgroups/{ring_group}` | stats__stats_ringgroups_ring_group |
| `GET` | `/api/asterisk/directory/extensions` | stats__directory_extensions |
| `GET` | `/api/asterisk/registration/status/{extension}` | registration__registration_status_extension |
| `GET` | `/api/asterisk/registration/events` | registration__registration_events |
| `GET` | `/api/asterisk/registration/online` | registration__registration_online |
| `GET` | `/api/asterisk/live/calls` | live__live_calls |
| `GET` | `/api/asterisk/live/calls/stream` | live__live_calls_stream |
| `GET` | `/api/asterisk/recordings/{linkedid}` | recordings__recordings_linkedid |
| `GET` | `/api/asterisk/dashboard/query` | dashboard__dashboard_query |
| `GET` | `/api/asterisk/dashboard/query_range` | dashboard__dashboard_query_range |

[OpenAPI: api/openapi/asterisk.yaml](https://github.com/go-tangra/go-tangra-asterisk/blob/eabd8b2810fa39b670050d363ae62d7fde78600e/api/openapi/asterisk.yaml)

## Detailed source references

- [README.md](sources/asterisk/README.html) — captured at `eabd8b2810fa`.
- [docs/migration.md](sources/asterisk/docs/migration.html) — captured at `eabd8b2810fa`.
- [docs/validation.md](sources/asterisk/docs/validation.html) — captured at `eabd8b2810fa`.

## Limits, diagnostics and recovery

This read-only observer binds one PBX to one tenant. Grant SELECT only on the PBX source. Registration history, if enabled, writes to a separate module-owned MySQL database. Recordings are read-only. The supplied Compose file needs an existing mesh network; a systemd unit is supplied for native deployment.

Use the module's operations/deployment reference for retention, backup/restore, refusal behavior, interface examples and feature limitations. The installation guides cover common readiness, identity, registration and storage failures.

## Upstream overview: Tangra V4 Asterisk

A read-only PBX observer for the Tangra V4 portal. It provides logical call history, extension/ringgroup statistics, observed registration history, live-call SSE, confined recording playback, directional RTP diagnostics and dedicated PBX monitoring. One service instance binds one PBX exclusively to one authenticated tenant.

## Build and verification

Use Go 1.26.8 (selected by `go.mod`) and Node 22. GitHub Packages access is required for `@go-tangra/ui`; set `NODE_AUTH_TOKEN` outside the repository. Published Go dependencies and the UI package lock are committed.

```sh
make ui-install
make generate check-generated
make test test-race ui-check
make build
```

`make build` embeds the federation remote (`./routes`, `./nav`) at `/ui/`; the portal proxies it at `/m/asterisk/`. `make build-no-ui` creates a backend-only binary. The default UI development entry denies permission-dependent actions; use the portal to receive session and CASL abilities.

## Configure and run

Populate the variables referenced by `configs/dev.yaml`: `ASTERISK_TENANT_ID`, `ASTERISK_PBX_ID`, `ASTERISK_CDR_DSN`, `ASTERISK_AUTH_TARGET`, `ASTERISK_AUTH_ISSUER` and `ASTERISK_PORTAL_TARGET`. Optional variables are `ASTERISK_CONFIG_DSN`, `ASTERISK_REGISTRATION_DSN`, `ASTERISK_RECORDING_ROOT`, `ASTERISK_MONITORING_URL`. Empty optional values disable their features. DSNs use the Go MySQL driver format; the source database timezone is explicit and defaults to Europe/Sofia. Source MySQL DATETIME values represent that zone; instants returned to clients are UTC.

The service obtains its mesh SPIFFE SVID by enrolling with lcm over the network (`identity.provider: provided` plus `mesh_enroll`: `enroll_url`, `lcm_grpc`, `tenant_id`, a one-time enrollment `token_file` and a writable `state_file`), like every go-tangra v4 module; set `ASTERISK_ENROLL_URL`, `ASTERISK_LCM_GRPC`, `ASTERISK_ENROLL_TENANT_ID`, `ASTERISK_ENROLL_TOKEN_FILE` and `ASTERISK_ENROLL_STATE_FILE` for `configs/dev.yaml`. Where a SPIRE agent runs, `identity.provider: spiffe` with a `workload_socket` works instead. There is no plaintext/insecure service fallback. Adjust the gateway workload SPIFFE ID in `deploy/policy.yaml` and provide matching auth/portal peer policies allowing this service's outbound SDK calls. Discovery entries are mesh gRPC targets, following the platform deployment's endpoint conventions. Admin `/healthz`, `/readyz`, `/metrics` default to loopback port 9094; non-loopback admin requires mTLS and explicit `allow_non_loopback`. Admin readiness includes source availability. Keep scraping private; never proxy `/metrics` as a browser API.

Grant only SELECT on PBX CDR/CEL and configuration schemas. The service runs no PBX migrations or control actions. The history source is required; CEL, RTP columns and directory names are probed and optional. Mount recordings read-only. Use a dedicated Prometheus upstream for the configured PBX/tenant, set `monitoring_dedicated: true`, and isolate its scrape targets. This setting is an operator assertion of dedicated storage, not an automatic partitioning mechanism.

Registration uses a **separate module-owned** MySQL database. Only changes are stored: the minute-by-minute contact snapshot writes a row when a contact's status, AOR, user agent or address changes, or shortly before its stored expiry lapses (so a continuously registered phone never appears expired). Events older than `registration_retention_days` (default 400, `0` keeps them forever) are pruned hourly. Bootstrap is explicit:

```sh
./bin/asterisksvc bootstrap -config configs/dev.yaml
./bin/asterisksvc -config configs/dev.yaml
```

AMI is independently optional: set `ami.enabled`, address, username and secret in a private configuration file or use `${VARIABLE}` expansion. Use an AMI account whose read privileges cover call/contact events and `CoreShowChannels`/`PJSIPShowContacts` plus the optional read-only `CoreSettings`, `CoreStatus`, `PJSIPShowEndpoints`, `SIPpeers` and `QueueStatus` metrics actions; grant no dialing, hangup or configuration privileges. TLS is supported with normal certificate verification. Live monitoring works without registration storage. History works without AMI. Reconciliation records current contacts and identifies unobserved intervals; it never reconstructs lost events.

Viewer permissions exclude recordings. Investigators have all six module permissions. Owner/admin grants are investigator; operator/member/auditor grants are viewer. Authorization remains server-side for snapshots, ranges, streams and monitoring. Recording routes require both `calls:read` and `recordings:read`.

## Deployment and acceptance

`Dockerfile` builds as non-root and uses a BuildKit `npm_token` secret. `deploy/compose.yaml` joins an existing mesh network and publishes no host ports. `deploy/tangra-asterisk.service` is the systemd alternative. Adjust paths, domain, discovery targets and environment files for your installation; keep PBX/dialplan changes manual.

Use `deploy/fixtures.yaml` for a disposable MySQL 8.4 fixture. See [docs/validation.md](sources/asterisk/docs/validation.html) for commands, measured checks and release blockers. Full portal/MySQL/performance acceptance is required before release; a passing unit suite does not establish these deployment results.
