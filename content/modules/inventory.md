# Inventory

Endpoint agents, hardware/software snapshots and change tracking.

**Architecture role**: Infrastructure. [See the complete component map](architecture/index.html).

**Documented source**: `cfa3a28445fc` · nearest local service tag `v4.7.0` · v4 major. [Repository at this revision](https://github.com/go-tangra/go-tangra-inventory/tree/cfa3a28445fc7d175b900df81aecdac0dd6d9707). Tags are source metadata, not a claim of image publication or cross-module compatibility.


## Permissions and authorization

This catalogue contains **9 permissions** declared by the [module manifest](https://github.com/go-tangra/go-tangra-inventory/blob/cfa3a28445fc7d175b900df81aecdac0dd6d9707/pkg/inventorymanifest/manifest.go) at the revision above. Custom-role references use `module:resource:action`; the manifest and API contract use the local `resource:action` form. The action names are distinct grants: do not assume `manage` automatically includes `read` or another action.

User UI permissions do not grant peer services access to host reports. A consumer needs the configured consumer allow-list and matching service policy; endpoint agents use their own enrollment/reporting identity.

[How to assign and verify permissions](architecture/security.html#assign-and-verify-permissions). Module roles and built-in grant mappings are defined in the linked manifest; review those mappings before assigning a broad role.

| Qualified permission | What it allows |
| --- | --- |
| `inventory:inventory:read` | List and read hosts, snapshots and the live stream |
| `inventory:inventory:write` | Contribute inventory data (manual snapshots, imports) |
| `inventory:hosts:manage` | Tag, retire and delete hosts |
| `inventory:agents:manage` | Enroll, refresh, list, upgrade and revoke endpoint agents |
| `inventory:agentupgrades:manage` | Configure automatic agent upgrades and the target agent version |
| `inventory:snapshots:read` | Read snapshot history, diffs and change records |
| `inventory:snapshots:manage` | Delete snapshots |
| `inventory:stats:read` | Read inventory statistics |
| `inventory:backup:manage` | Export and import tenant inventory data |

### inventory:inventory:read

List and read hosts, snapshots and the live stream.

**UI actions**: `read`, `create`, `update`, `delete` on `InventoryHost`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Hosts.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/inventory/v1/hosts` | listHosts |
| `GET` | `/api/inventory/v1/hosts/{id}` | getHost |
| `GET` | `/api/inventory/v1/hosts/{id}/latest` | getHostLatestSnapshot |
| `GET` | `/api/inventory/v1/hosts/{id}/certificates` | The host's current certificates, one row per name (feature 033); no material |
| `GET` | `/api/inventory/v1/certificate-deliveries` | Certificate delivery items, paged (feature 033); reads work while delivery is disabled |
| `GET` | `/api/inventory/v1/certificate-deliveries/{item_id}` | One delivery item with its delivery (configuration, trigger, requested by) |
| `GET` | `/api/inventory/v1/stream` | streamEvents |

**Scope and additional checks**: User UI permissions do not grant peer services access to host reports. A consumer needs the configured consumer allow-list and matching service policy; endpoint agents use their own enrollment/reporting identity.

### inventory:inventory:write

Contribute inventory data (manual snapshots, imports).

The imported OpenAPI operations do not declare a matching `x-freya-permission` for this grant. Use the manifest and server authorization implementation to identify its enforcement; this absence does not indicate public access.

**Scope and additional checks**: User UI permissions do not grant peer services access to host reports. A consumer needs the configured consumer allow-list and matching service policy; endpoint agents use their own enrollment/reporting identity.

### inventory:hosts:manage

Tag, retire and delete hosts.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `DELETE` | `/api/inventory/v1/hosts/{id}` | deleteHost |
| `POST` | `/api/inventory/v1/hosts/{id}/tags` | setHostTags |
| `POST` | `/api/inventory/v1/hosts/{id}/retire` | retireHost |

**Scope and additional checks**: User UI permissions do not grant peer services access to host reports. A consumer needs the configured consumer allow-list and matching service policy; endpoint agents use their own enrollment/reporting identity.

### inventory:agents:manage

Enroll, refresh, list, upgrade and revoke endpoint agents.

**UI actions**: `manage` on `InventoryAgent`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Agents.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/inventory/v1/certificate-deliveries/{item_id}/cancel` | Cancel a queued delivery item (cancelled_by_user) |
| `GET` | `/api/inventory/v1/agents` | Every enrolled agent (online and offline) with its version and upgrade state |
| `GET` | `/api/inventory/v1/agents/upgrades` | listAgentUpgrades |
| `POST` | `/api/inventory/v1/agents/upgrades` | Upgrade one agent, a selection or every outdated agent to the tenant target version |
| `POST` | `/api/inventory/v1/agents/upgrades/{id}/cancel` | cancelAgentUpgrade |
| `GET` | `/api/inventory/v1/agents/upgrade-policy` | The tenant's automatic agent upgrade policy (defaults when none is stored) |
| `GET` | `/api/inventory/v1/agents/auto-enroll` | The tenant's automatic enrollment switch and keys (secrets are never returned) |
| `PUT` | `/api/inventory/v1/agents/auto-enroll` | Turn automatic enrollment on or off for the tenant |
| `POST` | `/api/inventory/v1/agents/auto-enroll/keys` | Create an auto-enrollment key (the secret is returned once) |
| `PATCH` | `/api/inventory/v1/agents/auto-enroll/keys/{id}` | Change an auto-enrollment key (name, networks, on/off, expiry, limit) |
| `DELETE` | `/api/inventory/v1/agents/auto-enroll/keys/{id}` | Delete an auto-enrollment key (enrolled agents keep working) |
| `POST` | `/api/inventory/v1/agents/auto-enroll/keys/{id}/rotate` | Replace the key's secret (returned once); the key id stays |
| `GET` | `/api/inventory/v1/agent-releases` | Signed agent releases stored on the platform |
| `GET` | `/api/inventory/v1/agents/{id}` | getAgent |
| `POST` | `/api/inventory/v1/agents/enroll-token` | mintEnrollmentToken |
| `POST` | `/api/inventory/v1/agents/{host_id}/refresh` | refreshInventory |
| `POST` | `/api/inventory/v1/agents/{id}/revoke` | revokeAgent |

**Scope and additional checks**: User UI permissions do not grant peer services access to host reports. A consumer needs the configured consumer allow-list and matching service policy; endpoint agents use their own enrollment/reporting identity.

### inventory:agentupgrades:manage

Configure automatic agent upgrades and the target agent version.

**UI actions**: `manage` on `InventoryAgentUpgradePolicy`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `PUT` | `/api/inventory/v1/agents/upgrade-policy` | Configure automatic agent upgrades and the target agent version |
| `POST` | `/api/inventory/v1/agents/upgrade-policy/resume` | Resume automatic upgrades paused by a failed automatic upgrade |

**Scope and additional checks**: User UI permissions do not grant peer services access to host reports. A consumer needs the configured consumer allow-list and matching service policy; endpoint agents use their own enrollment/reporting identity.

### inventory:snapshots:read

Read snapshot history, diffs and change records.

**UI actions**: `read`, `create`, `update`, `delete` on `InventorySnapshot`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/inventory/v1/hosts/{id}/snapshots` | listHostSnapshots |
| `GET` | `/api/inventory/v1/hosts/{id}/changes` | listHostChanges |
| `GET` | `/api/inventory/v1/snapshots/{id}` | getSnapshot |
| `GET` | `/api/inventory/v1/snapshots/{id}/diff/{other}` | diffSnapshots |

**Scope and additional checks**: User UI permissions do not grant peer services access to host reports. A consumer needs the configured consumer allow-list and matching service policy; endpoint agents use their own enrollment/reporting identity.

### inventory:snapshots:manage

Delete snapshots.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `DELETE` | `/api/inventory/v1/snapshots/{id}` | deleteSnapshot |

**Scope and additional checks**: User UI permissions do not grant peer services access to host reports. A consumer needs the configured consumer allow-list and matching service policy; endpoint agents use their own enrollment/reporting identity.

### inventory:stats:read

Read inventory statistics.

**UI actions**: `read` on `InventoryStats`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Dashboard.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/inventory/v1/statistics/tenant` | getTenantStatistics |
| `GET` | `/api/inventory/v1/statistics/system` | getSystemStatistics |

**Scope and additional checks**: User UI permissions do not grant peer services access to host reports. A consumer needs the configured consumer allow-list and matching service policy; endpoint agents use their own enrollment/reporting identity.

### inventory:backup:manage

Export and import tenant inventory data.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/inventory/v1/backup/export` | exportBackup |
| `POST` | `/api/inventory/v1/backup/import` | importBackup |

**Scope and additional checks**: User UI permissions do not grant peer services access to host reports. A consumer needs the configured consumer allow-list and matching service policy; endpoint agents use their own enrollment/reporting identity.
<div class="guide-actions"><a href="how-to/inventory/docker.html">Install with Docker Compose →</a><a href="how-to/inventory/native.html">Install without Docker →</a><a href="downloads/inventory.zip">Download Compose bundle ↓</a></div>

## Dependencies and integration

**Required**: TimescaleDB, Valkey, Auth, Portal, mesh identity.

**Optional or feature-dependent**: endpoint agents, LCM certificate delivery.

Endpoint agents need their own enrollment and reporting configuration. Consumer access to host reports requires the documented consumer allow-list and matching service policy; it is not inherited from UI permissions.

The list describes infrastructure/features, not every transitive library. Check the linked deployment reference for exact versions, enabled features and peer grants. [Framework dependencies](architecture/dependencies.html) cover the shared Go libraries.

## Runtime and operation

| Item | Reference |
| --- | --- |
| Service binary | `inventorysvc` |
| Public example configuration | `deploy/dev.yaml`; adapt endpoints and paths for your environment |
| Native source build | Go `1.26.3`, toolchain `go1.26.8`, Node 22 for UI |
| Image repository | `ghcr.io/go-tangra/go-tangra-inventory`; choose a published compatible version |
| Private admin default | `127.0.0.1:9810`; check actual configuration |
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
| `Config` | `ingest` | `Ingest` |
| `Config` | `registry` | `Registry` |
| `Config` | `retention` | `Retention` |
| `Config` | `stale` | `Stale` |
| `Config` | `jobs` | `Jobs` |
| `Config` | `events` | `Events` |
| `Config` | `gateway` | `Gateway` |
| `Config` | `enroll` | `Enroll` |
| `Config` | `mesh_enroll` | `MeshEnroll` |
| `Config` | `limits_inventory` | `Limits` |
| `Config` | `host_reports` | `HostReports` |
| `Config` | `agent_releases` | `AgentReleases` |
| `Config` | `cert_delivery` | `CertDelivery` |
| `CertDelivery` | `enabled` | `bool` |
| `CertDelivery` | `sources` | `[]string` |
| `CertDelivery` | `lcm_service` | `string` |
| `CertDelivery` | `pending_ttl_hours` | `int` |
| `CertDelivery` | `report_timeout_minutes` | `int` |
| `CertDelivery` | `max_concurrent_fetches` | `int` |
| `CertDelivery` | `lcm_timeout_seconds` | `int` |
| `CertDelivery` | `allow_plaintext_ingest` | `bool` |
| `AgentReleases` | `bundle_dir` | `string` |
| `AgentReleases` | `keep_versions` | `int` |
| `AgentReleases` | `max_concurrent_downloads` | `int` |
| `AgentReleases` | `chunk_bytes` | `int` |
| `AgentReleases` | `request_ttl_hours` | `int` |
| `AgentReleases` | `progress_timeout_minutes` | `int` |
| `HostReports` | `consumers` | `[]string` |
| `HostReports` | `max_page_bytes` | `int` |
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
| `Ingest` | `addr` | `string` |
| `Ingest` | `insecure` | `bool` |
| `Ingest` | `tls_cert_file` | `string` |
| `Ingest` | `tls_key_file` | `string` |
| `Ingest` | `tls_reload_seconds` | `int` |
| `Registry` | `instance_id` | `string` |
| `Registry` | `heartbeat_seconds` | `int` |
| `Retention` | `days` | `int` |
| `Stale` | `after_seconds` | `int` |
| `Jobs` | `workers` | `int` |
| `Jobs` | `interval_seconds` | `int` |
| `Jobs` | `purge_interval_seconds` | `int` |
| `Events` | `enabled` | `bool` |
| `Gateway` | `service` | `string` |
| `Gateway` | `issuer` | `string` |
| `Enroll` | `token_ttl_seconds` | `int` |
| `MeshEnroll` | `enabled` | `bool` |
| `MeshEnroll` | `enroll_url` | `string` |
| `MeshEnroll` | `lcm_grpc` | `string` |
| `MeshEnroll` | `tenant_id` | `string` |
| `MeshEnroll` | `token_file` | `string` |
| `MeshEnroll` | `state_file` | `string` |
| `MeshEnroll` | `insecure` | `bool` |
| `Limits` | `max_request_bytes` | `int64` |
| `Limits` | `max_snapshot_bytes` | `int64` |
| `AgentConfig` | `ingest_endpoint` | `string` |
| `AgentConfig` | `interval_seconds` | `int` |
| `AgentConfig` | `token_file` | `string` |
| `AgentConfig` | `credential_file` | `string` |
| `AgentConfig` | `auto_enroll` | `AgentAutoEnroll` |
| `AgentConfig` | `state_file` | `string` |
| `AgentConfig` | `insecure` | `bool` |
| `AgentConfig` | `ca_file` | `string` |
| `AgentConfig` | `server_name` | `string` |
| `AgentConfig` | `collect_bmc` | `bool` |
| `AgentConfig` | `collect_updates` | `bool` |
| `AgentConfig` | `refresh_package_lists` | `bool` |
| `AgentConfig` | `update_timeout_seconds` | `int` |
| `AgentConfig` | `collect_disks` | `bool` |
| `AgentConfig` | `upgrade` | `AgentUpgrade` |
| `AgentConfig` | `certificates` | `AgentCertificates` |
| `AgentCertificates` | `enabled` | `bool` |
| `AgentCertificates` | `directory` | `string` |
| `AgentCertificates` | `owner` | `string` |
| `AgentCertificates` | `group` | `string` |
| `AgentCertificates` | `dir_mode` | `string` |
| `AgentCertificates` | `cert_mode` | `string` |
| `AgentCertificates` | `key_mode` | `string` |
| `AgentCertificates` | `keep_previous` | `int` |
| `AgentCertificates` | `deploy_hook` | `string` |
| `AgentCertificates` | `hook_timeout_seconds` | `int` |
| `AgentCertificates` | `allow_insecure_transport` | `bool` |
| `AgentAutoEnroll` | `key_id` | `string` |
| `AgentAutoEnroll` | `key_file` | `string` |
| `AgentUpgrade` | `enabled` | `bool` |
| `AgentUpgrade` | `confirm_timeout_seconds` | `int` |
| `AgentUpgrade` | `staging_dir` | `string` |

[Configuration structures and validation](https://github.com/go-tangra/go-tangra-inventory/blob/cfa3a28445fc7d175b900df81aecdac0dd6d9707/internal/config/config.go)

## API operation index

These operations are extracted from the module's OpenAPI contract. Read the source contract for request/response schemas, permission checks and exact route bases; internal mesh endpoints must not be treated as anonymous public APIs.

| Method | Contract path | Operation |
| --- | --- | --- |
| `GET` | `/api/inventory/v1/hosts` | listHosts |
| `GET` | `/api/inventory/v1/hosts/{id}` | getHost |
| `DELETE` | `/api/inventory/v1/hosts/{id}` | deleteHost |
| `GET` | `/api/inventory/v1/hosts/{id}/latest` | getHostLatestSnapshot |
| `POST` | `/api/inventory/v1/hosts/{id}/tags` | setHostTags |
| `POST` | `/api/inventory/v1/hosts/{id}/retire` | retireHost |
| `GET` | `/api/inventory/v1/hosts/{id}/snapshots` | listHostSnapshots |
| `GET` | `/api/inventory/v1/hosts/{id}/changes` | listHostChanges |
| `GET` | `/api/inventory/v1/hosts/{id}/certificates` | The host's current certificates, one row per name (feature 033); no material |
| `GET` | `/api/inventory/v1/certificate-deliveries` | Certificate delivery items, paged (feature 033); reads work while delivery is disabled |
| `GET` | `/api/inventory/v1/certificate-deliveries/{item_id}` | One delivery item with its delivery (configuration, trigger, requested by) |
| `POST` | `/api/inventory/v1/certificate-deliveries/{item_id}/cancel` | Cancel a queued delivery item (cancelled_by_user) |
| `GET` | `/api/inventory/v1/snapshots/{id}` | getSnapshot |
| `DELETE` | `/api/inventory/v1/snapshots/{id}` | deleteSnapshot |
| `GET` | `/api/inventory/v1/snapshots/{id}/diff/{other}` | diffSnapshots |
| `GET` | `/api/inventory/v1/agents` | Every enrolled agent (online and offline) with its version and upgrade state |
| `GET` | `/api/inventory/v1/agents/upgrades` | listAgentUpgrades |
| `POST` | `/api/inventory/v1/agents/upgrades` | Upgrade one agent, a selection or every outdated agent to the tenant target version |
| `POST` | `/api/inventory/v1/agents/upgrades/{id}/cancel` | cancelAgentUpgrade |
| `GET` | `/api/inventory/v1/agents/upgrade-policy` | The tenant's automatic agent upgrade policy (defaults when none is stored) |
| `PUT` | `/api/inventory/v1/agents/upgrade-policy` | Configure automatic agent upgrades and the target agent version |
| `POST` | `/api/inventory/v1/agents/upgrade-policy/resume` | Resume automatic upgrades paused by a failed automatic upgrade |
| `GET` | `/api/inventory/v1/agents/auto-enroll` | The tenant's automatic enrollment switch and keys (secrets are never returned) |
| `PUT` | `/api/inventory/v1/agents/auto-enroll` | Turn automatic enrollment on or off for the tenant |
| `POST` | `/api/inventory/v1/agents/auto-enroll/keys` | Create an auto-enrollment key (the secret is returned once) |
| `PATCH` | `/api/inventory/v1/agents/auto-enroll/keys/{id}` | Change an auto-enrollment key (name, networks, on/off, expiry, limit) |
| `DELETE` | `/api/inventory/v1/agents/auto-enroll/keys/{id}` | Delete an auto-enrollment key (enrolled agents keep working) |
| `POST` | `/api/inventory/v1/agents/auto-enroll/keys/{id}/rotate` | Replace the key's secret (returned once); the key id stays |
| `GET` | `/api/inventory/v1/agent-releases` | Signed agent releases stored on the platform |
| `GET` | `/api/inventory/v1/agents/{id}` | getAgent |
| `POST` | `/api/inventory/v1/agents/enroll-token` | mintEnrollmentToken |
| `POST` | `/api/inventory/v1/agents/{host_id}/refresh` | refreshInventory |
| `POST` | `/api/inventory/v1/agents/{id}/revoke` | revokeAgent |
| `GET` | `/api/inventory/v1/statistics/tenant` | getTenantStatistics |
| `GET` | `/api/inventory/v1/statistics/system` | getSystemStatistics |
| `POST` | `/api/inventory/v1/backup/export` | exportBackup |
| `POST` | `/api/inventory/v1/backup/import` | importBackup |
| `GET` | `/api/inventory/v1/stream` | streamEvents |

[OpenAPI: api/openapi/inventory.yaml](https://github.com/go-tangra/go-tangra-inventory/blob/cfa3a28445fc7d175b900df81aecdac0dd6d9707/api/openapi/inventory.yaml)

## Detailed source references

- [README.md](sources/inventory/README.html) — captured at `cfa3a28445fc`.
- [deploy/README.md](sources/inventory/deploy/README.html) — captured at `cfa3a28445fc`.

## Limits, diagnostics and recovery

Endpoint agents need their own enrollment and reporting configuration. Consumer access to host reports requires the documented consumer allow-list and matching service policy; it is not inherited from UI permissions.

Use the module's operations/deployment reference for retention, backup/restore, refusal behavior, interface examples and feature limitations. The installation guides cover common readiness, identity, registration and storage failures.

## Upstream overview: go-tangra-inventory

IT asset inventory service for the
[go-tangra v4 platform](https://github.com/go-tangra/go-tangra).

Endpoint agents collect hardware (SMBIOS/DMI), software/OS, network and storage
inventory and report immutable snapshots to the service. The service resolves each
snapshot to a stable host identity (hardware UUID, then machine id, then hostname),
keeps the full time-series history in TimescaleDB, records what changed between
snapshots, and serves query, diff, statistics, on-demand refresh and backup
export/import over the gateway and service-to-service gRPC, plus a federated UI
remote. Agent and enrollment credentials are sealed with envelope encryption, and
every tenant is isolated by PostgreSQL row-level security.

Since 4.7.0 the service also relays lcm certificates to Linux agents for the
deployer's `inventory-agent` provider (feature 033): the deployer asks for a
delivery by reference, inventory pushes an item id to the agent, the agent
pulls the certificate (and, by policy, the private key) over its
authenticated ingest connection and installs it under a certbot-style
directory, optionally running a locally configured deploy hook. Inventory
never stores certificate material; renewals and offline hosts are delivered
automatically, and every transition is audited
([Certificates on the host](#certificates-on-the-host-feature-033),
[deploy/README.md](sources/inventory/deploy/README.html#certificate-delivery-deployer-feature-033)).

Operations: [`deploy/README.md`](sources/inventory/deploy/README.html).
Design history: `specs/010-inventory-service`.

## Place in the platform

```
go-tangra/go-tangra          platform module + @go-tangra/ui kit
        |
go-tangra-auth  <---->  go-tangra-portal (gateway)  <---->  go-tangra-inventory  <----  inventory-agent
                                    |                              ^                   (off-mesh, ingest edge)
                              go-tangra-lcm (mesh SVID)       go-tangra-asset (inventory sdk)
```

- Built on `github.com/go-tangra/go-tangra/v4` (mTLS transports, identity,
  service policy, audit, observability).
- Verifies platform tokens and registers its permissions with the auth SDK
  (`github.com/go-tangra/go-tangra-auth/sdk/v4`).
- Registers routes, permissions, abilities and navigation with the gateway through
  the portal SDK (`github.com/go-tangra/go-tangra-portal/sdk/v4`).
- Enrolls for its own mesh SVID over lcm (`github.com/go-tangra/go-tangra-lcm/sdk/v4`).

## Two trust planes

| Listener | Default | Who calls it |
|---|---|---|
| mesh gRPC (`inventory.v1`) / HTTP | `:9975` / `:9976` | the gateway (browser API under `/api/inventory`) and other services, SPIFFE mTLS |
| ingest edge | `:9977` | untrusted off-mesh agents, authenticated by a per-agent credential |
| admin (health, readiness, metrics) | `127.0.0.1:9810` | the container runtime |

An agent exchanges a tenant-scoped, single-use, expiring enrollment token — or,
when the tenant allows it, a proof made with a network-restricted
auto-enrollment key (feature 029) — for its per-agent credential, then submits
snapshots and holds a command stream for refresh.

## Modules in this repository

| Module | Path | Consumers |
|---|---|---|
| `github.com/go-tangra/go-tangra-inventory/v4` | `/` | the service (`cmd/inventorysvc`), the agent (`cmd/inventory-agent`) and `pkg/inventorymanifest` |
| `github.com/go-tangra/go-tangra-inventory/sdk/v4` | `sdk/` | other services (asset, ipam): the `inventory.v1` protobuf API and `pkg/inventoryclient` |

The service builds against the in-repo SDK through
`replace github.com/go-tangra/go-tangra-inventory/sdk/v4 => ./sdk`. Consumers use the
SDK's published `sdk/vX.Y.Z` tag.

## Layout

| Path | Purpose |
|------|---------|
| `cmd/inventorysvc` | service binary (serve, `bootstrap`, `version`) |
| `cmd/inventory-agent` | endpoint agent for Linux and Windows (one-shot, daemon, Windows service; run under systemd on Linux) |
| `internal/app` | wiring: config, platform, stores, services, HTTP/gRPC, ingest edge |
| `internal/...` | hosts, snapshots, diff, enrollment, ingest, registry, streams, sealing, authz, audit, events, stats, backup and their SQL bindings; agent-side collector, sender, daemon and Windows service |
| `internal/agentfacts` | pure, fuzzed parsers behind the agent's host report collection (netlink, sysfs, Windows adapters, virtualization, Proxmox, package managers, BMC LAN parameters) |
| `internal/hostreport` | the host report projection and digest served to IPAM |
| `internal/certmaterial` | pure, fuzzed certificate rules shared by server and agent: names, host tags, certificate ids, PEM bundle parsing and limits, key ↔ certificate match |
| `internal/certdelivery` | the certificate delivery relay (feature 033): create/replay/supersede, fetch from lcm, report, sweep, re-arm, revoke, verify, views |
| `internal/lcmclient` | mesh client of `lcm.v1.Certificates/Download` with a closed error mapping |
| `internal/agentcerts` | agent certificate store: `live/`→`archive/` symlink layout, atomic switch, crash recovery, pruning, deploy hook |
| `ui` | Vue 3 + FlyonUI federated remote on `@go-tangra/ui` |
| `api/openapi`, `sdk/api/proto` | contracts (`inventory.yaml`, `inventory.v1`) |
| `deploy` | operations guide, service policy and the development KEK (never copied into the image) |

## Build and test

You need Go 1.26, Node 22, Docker (for integration tests and the image), and a
GitHub token with `read:packages` to install `@go-tangra/ui` from GitHub Packages.

```bash
go build ./... && go vet ./... && go test -race ./...
(cd sdk && go vet ./... && go test -race ./...)
make proto-check                          # buf lint + buf breaking against sdk/v4.1.0
make test-integration                     # -tags integration, needs Docker
make lint cover vuln
make fuzz                                 # every Fuzz* target, FUZZTIME=10s each
make e2e-upgrade                          # agent self-upgrade in systemd containers, needs privileged Docker

cd ui
export NODE_AUTH_TOKEN=$(gh auth token)   # ui/.npmrc only references this variable
npm ci && npm run lint && npm run test:unit && npm run build
```

The unit coverage gate requires at least 80 % overall and 100 % for the
authorization, sealing, enrollment, host report projection, release
verification (`agentrelease`), agent self-update and upgrade lifecycle packages. Generated code, SQL bindings,
wiring and the agent's platform collectors are covered by the integration suite
or excluded on purpose.

## The agent

`inventory-agent` is not part of the container image. Build it for the hosts you
manage:

```bash
make agent                                # bin/inventory-agent-{linux,windows}-{amd64,arm64}[.exe]
inventory-agent -ingest <host:9977> -token <token-file>        # one-shot enroll + collect + submit
inventory-agent -config agent.yaml -daemon                      # periodic submit + refresh stream
inventory-agent -o ./out                                        # collect to JSON, no submit
inventory-agent -service install                                # Windows only: installs the Windows service
```

`-service install` exists on Windows only; it does not create a systemd unit.
On Linux install the `tangra-inventory-agent` .deb/.rpm attached to each
release (systemd unit included; `make packages` builds them), see
[deploy/README.md](sources/inventory/deploy/README.html#installing-the-agent-from-a-package), or
run the daemon under systemd yourself
([example](sources/inventory/deploy/README.html#running-the-agent-under-systemd)).

Besides hardware, software and disks the agent reports what IPAM needs to keep
its devices current: per-interface kind, speed, bond/bridge master, VLAN id,
addresses with prefix and DHCP/temporary/deprecated flags, gateway and default
route, the primary IPv4/IPv6 address, the virtualization role, the BMC LAN
settings (Linux, read-only, never credentials), Proxmox guests (Linux) and the
package update state (Linux: pending and security updates, reboot required,
automatic updates). Every list is bounded and what is dropped is counted.
`collect_bmc`, `collect_updates`, `refresh_package_lists` (off: the agent never
refreshes package lists unless told to) and `update_timeout_seconds` tune it;
see [deploy/README.md](sources/inventory/deploy/README.html#host-report-collection).

The ingest edge serves TLS from `ingest.tls_cert_file`/`ingest.tls_key_file`
(hot-reloaded). Only the development opt-out `ingest.insecure: true` serves
plaintext, and it is refused with `env: production`. The agent verifies the
server certificate against the system roots, or only against `ca_file`
(`-ca-file`) for a private CA; `server_name` (`-server-name`) overrides the
verified name. See [deploy/README.md](sources/inventory/deploy/README.html#ingest-tls).

Hardware comes from the raw SMBIOS table (Linux sysfs, go-smbios as the
fallback on other platforms), decoded against DSP0134: BIOS vendor, version and
date; system, board and chassis identity; every processor socket with family,
cores and threads; the physical memory arrays (location, use, ECC, maximum
capacity, slot count) and every memory slot, populated or empty, with type,
type detail, rated and configured speed, bank and locator. `collect_disks`
(default on) adds the physical disks (name, model, serial, size, SSD/HDD/NVMe,
interface, removable; Linux sysfs, Windows `Get-PhysicalDisk`) and maps every
filesystem to its disk. The dashboard's disk total counts physical disks only.
Snapshots from older agents keep their hardware as sent and are marked
`hardware_schema < 2` in the UI.

### Agent self-upgrade

From agent 4.4.0 on the platform upgrades agents itself. The first 4.4.0 is
installed by hand once per host (package or binary as above); after that:

- **Fleet view** (Inventory > Agents): every enrolled agent, online or not, with
  version, target version and upgrade state (`up_to_date`, `available`,
  `pending`, `in_progress`, `failed`, `rolled_back`, `manual_upgrade_required`
  for agents older than 4.4.0, `unsupported`). **Upgrade**, **Upgrade
  selected**, **Upgrade all outdated** and **Cancel** need `agents:manage`.
- **Delivery**: the request reaches online agents at once over the command
  stream and offline agents when they connect. The agent downloads the artifact
  for its platform (linux/windows, amd64/arm64, deb/rpm/binary) over the same
  mTLS ingest connection with its own credential.
- **Verification**: the Ed25519 signature of the release manifest is checked
  against the release keys compiled into the agent, then size and SHA-256 of the
  artifact while it streams. Nothing is installed from an unverified download;
  downgrades need an explicit pin, never below 4.4.0.
- **Install**: Linux needs systemd. deb and rpm installs upgrade through
  `dpkg -i` / `rpm -U` in a transient systemd unit, binary installs by an
  atomic swap; Windows swaps the binary and restarts the service. Hosts without
  systemd report `unsupported_install`: upgrade them by hand.
- **Rollback**: the new version must connect and submit within
  `upgrade.confirm_timeout_seconds` (default 300). Otherwise the previous
  package (or binary) is put back and the request ends `rolled_back`.
- **On the host**: `inventory-agent update -check` prints the current and the
  available version (exit 0 up to date, 10 upgrade available, 1 error, 2 another
  upgrade running); `inventory-agent update` upgrades now. `upgrade.enabled:
  false` ignores upgrade requests from the platform.
- **Automatic upgrades** (off by default, `agentupgrades:manage`): per tenant a
  maintenance window (HH:MM, may wrap midnight, timezone), a concurrency limit
  and an optional pinned version (which also allows downgrades). Until one
  agent of the tenant runs the target version the policy upgrades a single
  agent at a time (canary); a failed or rolled-back automatic upgrade pauses the
  policy until an administrator resumes it.

Releases are bundled in the image (`agent-releases/<version>/`: manifest,
signature and the eight artifacts), verified and copied into PostgreSQL at
start; the newest bundled version is the platform's current version and the
last `agent_releases.keep_versions` (default 5) are kept, about 80 MB per
release. Offline sites or other versions: `inventorysvc agent-release import
-config <file> <release dir>` (same verification). Every request, transition,
refusal, policy change and import is audited. Operations:
[deploy/README.md](sources/inventory/deploy/README.html#agent-self-upgrade).

### Agent release signing

Release artifacts are signed with an Ed25519 key that never enters the
repository or the image. The public half is compiled into `inventorysvc` and
`inventory-agent` through `-ldflags -X
github.com/go-tangra/go-tangra-inventory/v4/internal/agentrelease.productionKeys=<id>:<base64>[,<id>:<base64>]`
(`make ... AGENT_RELEASE_KEYS=...`; a build without keys trusts nothing and
refuses every release).

Key generation (once, on an offline or trusted machine):

```bash
go run ./cmd/agent-release keygen -key-id release-2026 -out-private release-2026.key > release-2026.pub
cat release-2026.pub      # "release-2026:<base64 public key>"
```

GitHub setup:

1. Create the environment **`release`** (Settings > Environments) with required
   reviewers and deployment restricted to `v*` tags.
2. Store the content of `release-2026.key` (base64 seed) as the environment
   secret **`AGENT_RELEASE_SIGNING_KEY`**, then delete the local file (keep an
   offline backup per SECURITY.md).
3. Store the content of `release-2026.pub` as the repository variable
   **`AGENT_RELEASE_PUBLIC_KEYS`** (comma-separate several keys during a
   rotation).

On a `v*` tag the CI `sign` job (environment `release`) runs `agent-release
sign` on the eight artifacts, `agent-release verify` and `make release-check`
(every binary carries the keyring and version, no `dev-` key). It fails with a
clear error when the secret or the variable is missing. The `docker` job bakes
the signed bundle into the image; the GitHub release carries artifacts,
manifest, signature and `SHA256SUMS`.

Local testing uses a throwaway key: `make agent-release-dev AGENT_VERSION=4.4.1`
generates `.dev/agent-release/dev.key` (git-ignored, key id `dev-local`) and
copies a dev-signed release into `agent-releases/`, which only an image built
with that dev keyring accepts. `make e2e-upgrade` runs the systemd container
end-to-end test (Debian 12, Rocky 9) with its own throwaway key.

CI cross-compiles the agent for every supported platform on each change and
builds the signed release only on tags.

### Certificates on the host (feature 033)

Linux agents receive certificates that the deployer's `inventory-agent`
provider delivers (server side: [deploy/README.md](sources/inventory/deploy/README.html#certificate-delivery-deployer-feature-033)).
The agent announces the `cert.v1` capability when `certificates.enabled`
(default true) and the ingest connection uses TLS (or
`certificates.allow_insecure_transport`, development only); Windows agents
never announce it. A `CERTIFICATE` command carries only an item id and a
name; the agent pulls the bundle over its authenticated connection,
validates it again (name, PEM, key ↔ certificate, validity, sizes) and
writes it only below `certificates.directory` (default
`/etc/inventory-agent/certs`). Configuration (`agent.yaml`, all keys
optional, defaults shown; invalid values refuse to start):

```yaml
certificates:
  enabled: true                       # false: deliveries are answered disabled_locally
  directory: /etc/inventory-agent/certs   # absolute; not under /proc /sys /dev /home /root /tmp
  owner: root                         # file owner (directories stay root-owned)
  group: root                         # e.g. nginx, so a service reads its key via the group
  dir_mode: "0750"                    # 0700-0755, no world write
  cert_mode: "0644"
  key_mode: "0600"                    # 0600 or 0640
  keep_previous: 1                    # 0-5 older generations kept
  deploy_hook: ""                     # absolute path; empty = nothing ever runs
  hook_timeout_seconds: 300           # 30-1800; keep below the server's report_timeout_minutes
  allow_insecure_transport: false     # development only (plaintext ingest edge)
```

```text
live/<name> -> ../archive/<name>/<generation>   symlink, switched with one rename(2)
archive/<name>/<generation>/{cert,chain,fullchain,privkey}.pem
renewal/<name>.json                             v3 metadata + certificate/item ids
```

Consumers use `live/<name>/fullchain.pem` and `live/<name>/privkey.pem`
(certbot paths); a reader never sees a certificate with the wrong key.
Directories are `root:<group>`, files `<owner>:<group>` with the configured
modes; `keep_previous` (default 1) older generations stay for a manual
restore (`ln -sfn ../archive/<name>/<previous> live/<name>`). The same
certificate again is reported `unchanged` without writing anything;
`certificate_only` deliveries keep an existing matching `privkey.pem` and
fail with `key_mismatch` otherwise.

**Deploy hook** (off by default, never sent by the platform): set
`certificates.deploy_hook` to an absolute path. It runs after a new or
renewed installation (and when the platform retries a failed hook), only if
the file is a regular, root-owned file, executable and not writable by group
or others, and its directory and every ancestor up to `/` are root-owned
and not writable by group or others (so no hook under `/tmp` or a user's
tree) — otherwise `hook_refused`. It is executed directly (no shell, no arguments)
in `live/<name>`, in its own process group, with stdin from `/dev/null` and
exactly this environment: `PATH`, `LANG=C.UTF-8`, `LCM_CERT_NAME`,
`LCM_CERT_DIR`, `LCM_CERT_PATH`, `LCM_KEY_PATH` (empty without a key),
`LCM_CHAIN_PATH`, `LCM_FULLCHAIN_PATH`, `LCM_COMMON_NAME`, `LCM_DNS_NAMES`,
`LCM_IP_ADDRESSES`, `LCM_SERIAL_NUMBER`, `LCM_EXPIRES_AT`, `LCM_IS_RENEWAL`,
`LCM_CERTIFICATE_ID` (validated `[A-Za-z0-9._:-]{1,128}`). Control
characters are stripped, but `LCM_COMMON_NAME` and `LCM_DNS_NAMES` come from
the certificate, so a hook must quote them (`"$LCM_DNS_NAMES"`) and never
`eval` them. After `hook_timeout_seconds` (default 300) the group
gets SIGTERM and 5 s later SIGKILL (`hook_timeout`, exit 256). A non-zero
exit is reported as `hook_failed` with the exit code; the files stay
installed. Hook output (first 4 KiB) goes to the agent log only. The systemd
unit sets `ProtectHome`, `PrivateTmp` and `NoNewPrivileges`, so a hook sees
no `/home` and a private `/tmp`; `systemctl reload nginx` works. Example:

```sh
#!/bin/sh
## Upstream overview: /usr/local/sbin/reload-nginx.sh  (root:root 0755)
nginx -t && systemctl reload nginx
```

`make test-agent-certs` runs the store and hook tests as root in a container.

## Host reports for IPAM

`inventory.v1.HostReportService` (mesh only, not proxied by the gateway) serves a
slim projection of each host's latest snapshot: identity, interfaces and
addresses, primary addresses, virtualization, BMC, guests, update state and only
the packages with a pending update. Each host keeps a digest of its projection
and the time it last changed, so a consumer polls "tenants changed since",
"host reports changed since" (full or digest view, paged) and "one host report"
without re-reading unchanged hosts. The IPAM host sync is its consumer
(`pkg/inventoryclient`: `ListReportTenants`, `ListHostReports`, `GetHostReport`).

Access needs both the inbound policy rule `ipam-hostsync` in
`deploy/policy.yaml` (the three RPCs and health, for `svc/ipam` only) and the
caller's service name in `host_reports.consumers` (default `[ipam]`), which the
handler checks for every RPC.

## Container image

The image is `ghcr.io/go-tangra/go-tangra-inventory`, built by
`.github/workflows/ci.yaml`. It carries `inventorysvc` with the embedded UI remote.

```bash
docker buildx build --secret id=npm_token,env=NODE_AUTH_TOKEN \
  --build-arg APP_VERSION=4.0.0 -t go-tangra-inventory:dev .
docker run --rm go-tangra-inventory:dev version
```

The image runs `inventorysvc -config deploy/container.yaml` as user `app`
(uid 10001). It ships `deploy/policy.yaml` but no configuration and no key
material: the deployment mounts `deploy/container.yaml` and the key-encryption key
(the go-tangra platform stack mounts its dev KEK at `/app/deploy/kek.dev`) and
publishes the ingest edge port.

## API permissions and module roles

`inventory:read/write`, `hosts:manage`, `agents:manage` (enroll, refresh,
list, upgrade and revoke agents), `agentupgrades:manage` (automatic upgrades
and the pinned agent version, including downgrades; owner, admin and the module
administrator only, not operator), `snapshots:read/manage`, `stats:read`,
`backup:manage`. The gateway enforces the per-route permission from the
manifest; the module checks it again.

The module registers its permissions, its module roles and the built-in role
grants (`pkg/inventorymanifest.Grants`, scoped to inventory by auth) with auth
at start and every five minutes (`pkg/inventorymanifest.Registration`). Module
roles are provided in every tenant; administrators assign them or clone them
into custom roles:

| Role | Display name | Permissions |
|---|---|---|
| `administrator` | Inventory administrator | all inventory permissions |
| `editor` | Inventory editor | `inventory:read`, `inventory:write`, `snapshots:read` |
| `viewer` | Inventory viewer | `inventory:read`, `snapshots:read`, `stats:read` |

## Versioning

- Service releases are tagged `vX.Y.Z`. CI publishes the image as `X.Y.Z`,
  `X.Y`, `X` and `sha-<short>`. There is no `latest` tag.
- The SDK is released separately with `sdk/vX.Y.Z` tags. These tags never build an image.
- v4.0.0 rebuilds the service on the go-tangra v4 platform. The previous line stays on
  the `v3` branch and its existing `v1.x` tags.
