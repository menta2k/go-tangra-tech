# IPAM

IP addresses, networks, active discovery and IPMI/KVM operations.

**Architecture role**: Infrastructure. [See the complete component map](architecture/index.html).

**Documented source**: `df4cab11e3d0` · nearest local service tag `v4.10.3` · v4 major. [Repository at this revision](https://github.com/go-tangra/go-tangra-ipam/tree/df4cab11e3d0a69aac0f90d97b83006dd808ab8a). Tags are source metadata, not a claim of image publication or cross-module compatibility.


## Permissions and authorization

This catalogue contains **14 permissions** declared by the [module manifest](https://github.com/go-tangra/go-tangra-ipam/blob/df4cab11e3d0a69aac0f90d97b83006dd808ab8a/pkg/ipammanifest/manifest.go) at the revision above. Custom-role references use `module:resource:action`; the manifest and API contract use the local `resource:action` form. The action names are distinct grants: do not assume `manage` automatically includes `read` or another action.

Module permissions gate actions within the authenticated tenant. The endpoint still enforces its resource and workflow checks; a UI ability describes presentation and does not replace server authorization.

[How to assign and verify permissions](architecture/security.html#assign-and-verify-permissions). Module roles and built-in grant mappings are defined in the linked manifest; review those mappings before assigning a broad role.

| Qualified permission | What it allows |
| --- | --- |
| `ipam:ipam:read` | List and read subnets, addresses, devices, groups, scans and the live stream |
| `ipam:subnets:manage` | Create, update and delete subnets |
| `ipam:addresses:manage` | Create, update and delete IP addresses |
| `ipam:addresses:allocate` | Allocate next-free and bulk IP addresses |
| `ipam:devices:manage` | Create, update and delete devices, interfaces and packages |
| `ipam:vlans:manage` | Create, update and delete VLANs |
| `ipam:locations:manage` | Create, update and delete locations |
| `ipam:groups:manage` | Create, update and delete IP and host groups and their members |
| `ipam:scan:run` | Start subnet and address discovery scans and ping |
| `ipam:dns:manage` | Read and update the per-tenant DNS configuration |
| `ipam:backup:manage` | Export and import tenant IPAM data |
| `ipam:power:control` | Out-of-band power status and actions via device BMC (platform-admin) |
| `ipam:kvm:access` | Start token-gated KVM console sessions (platform-admin) |
| `ipam:hostsync:manage` | Enable or disable the host sync and edit its interface exclusions |

### ipam:ipam:read

List and read subnets, addresses, devices, groups, scans and the live stream.

**UI actions**: `read` on `Subnet`, `IpAddress`, `Device`, `Vlan`, `Location`, `IpGroup`, `HostGroup`, `IpScan`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Subnets, IP Addresses, Devices, VLANs, Locations, Groups, Scans, Host sync, Dashboard.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/ipam/v1/subnets` | listSubnets |
| `GET` | `/api/ipam/v1/subnets/tree` | getSubnetTree |
| `GET` | `/api/ipam/v1/subnets/{id}` | getSubnet |
| `GET` | `/api/ipam/v1/subnets/{id}/stats` | getSubnetStats |
| `GET` | `/api/ipam/v1/subnets/{id}/snmp` | getSubnetSnmp |
| `GET` | `/api/ipam/v1/ip-addresses` | listIpAddresses |
| `GET` | `/api/ipam/v1/ip-addresses/find` | findIpAddress |
| `GET` | `/api/ipam/v1/ip-addresses/suggest` | suggestIpAddresses |
| `GET` | `/api/ipam/v1/ip-addresses/{id}` | getIpAddress |
| `GET` | `/api/ipam/v1/devices` | listDevices |
| `GET` | `/api/ipam/v1/devices/{id}` | getDevice |
| `GET` | `/api/ipam/v1/devices/{id}/addresses` | getDeviceAddresses |
| `GET` | `/api/ipam/v1/devices/{id}/interfaces` | getDeviceInterfaces |
| `GET` | `/api/ipam/v1/devices/{id}/packages` | listDevicePackages |
| `GET` | `/api/ipam/v1/devices/{id}/host-groups` | getDeviceHostGroups |
| `GET` | `/api/ipam/v1/devices/{id}/bmc` | getDeviceBmc |
| `GET` | `/api/ipam/v1/devices/{id}/host-sync` | getDeviceHostSync |
| `GET` | `/api/ipam/v1/devices/{id}/hardware` | getDeviceHardware |
| `GET` | `/api/ipam/v1/devices/{id}/guests` | listDeviceGuests |
| `GET` | `/api/ipam/v1/host-sync/settings` | getHostSyncSettings |
| `GET` | `/api/ipam/v1/host-sync/status` | getHostSyncStatus |
| `GET` | `/api/ipam/v1/arp/settings` | getArpSettings |
| `GET` | `/api/ipam/v1/vlans` | listVlans |
| `GET` | `/api/ipam/v1/vlans/{id}` | getVlan |
| `GET` | `/api/ipam/v1/vlans/{id}/subnets` | getVlanSubnets |
| `GET` | `/api/ipam/v1/locations` | listLocations |
| `GET` | `/api/ipam/v1/locations/tree` | getLocationTree |
| `GET` | `/api/ipam/v1/locations/{id}` | getLocation |
| `GET` | `/api/ipam/v1/ip-groups` | listIpGroups |
| `GET` | `/api/ipam/v1/ip-groups/check` | checkIpInGroup |
| `GET` | `/api/ipam/v1/ip-groups/{id}` | getIpGroup |
| `GET` | `/api/ipam/v1/ip-groups/{id}/members` | listIpGroupMembers |
| `GET` | `/api/ipam/v1/host-groups` | listHostGroups |
| `GET` | `/api/ipam/v1/host-groups/{id}` | getHostGroup |
| `GET` | `/api/ipam/v1/host-groups/{id}/members` | listHostGroupMembers |
| `GET` | `/api/ipam/v1/ip-scans` | listIpScans |
| `GET` | `/api/ipam/v1/ip-scans/{id}` | getIpScan |
| `GET` | `/api/ipam/v1/stats` | getStats |
| `GET` | `/api/ipam/v1/dns-config` | getDnsConfig |
| `GET` | `/api/ipam/v1/stream` | streamEvents |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### ipam:subnets:manage

Create, update and delete subnets.

**UI actions**: `configure` on `SubnetSnmp`; `configure` on `ArpSettings`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/ipam/v1/subnets` | createSubnet |
| `PUT` | `/api/ipam/v1/subnets/{id}` | updateSubnet |
| `DELETE` | `/api/ipam/v1/subnets/{id}` | deleteSubnet |
| `POST` | `/api/ipam/v1/subnets/{id}/split` | splitSubnet |
| `PUT` | `/api/ipam/v1/subnets/{id}/snmp` | setSubnetSnmp |
| `DELETE` | `/api/ipam/v1/subnets/{id}/snmp` | clearSubnetSnmp |
| `PUT` | `/api/ipam/v1/arp/settings` | updateArpSettings |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### ipam:addresses:manage

Create, update and delete IP addresses.

**UI actions**: `clear` on `AddressConflict`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/ipam/v1/ip-addresses` | createIpAddress |
| `PUT` | `/api/ipam/v1/ip-addresses/{id}` | updateIpAddress |
| `DELETE` | `/api/ipam/v1/ip-addresses/{id}` | deleteIpAddress |
| `POST` | `/api/ipam/v1/ip-addresses/{id}/clear-conflict` | clearIpAddressConflict |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### ipam:addresses:allocate

Allocate next-free and bulk IP addresses.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/ipam/v1/ip-addresses/allocate` | allocateIpAddress |
| `POST` | `/api/ipam/v1/ip-addresses/bulk-allocate` | bulkAllocateIpAddresses |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### ipam:devices:manage

Create, update and delete devices, interfaces and packages.

**UI actions**: `resync` on `HostSync`; `configure` on `DeviceBmc`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/ipam/v1/devices` | createDevice |
| `PUT` | `/api/ipam/v1/devices/{id}` | updateDevice |
| `DELETE` | `/api/ipam/v1/devices/{id}` | deleteDevice |
| `POST` | `/api/ipam/v1/devices/{id}/interfaces` | createDeviceInterface |
| `DELETE` | `/api/ipam/v1/devices/{id}/interfaces/{ifid}` | deleteDeviceInterface |
| `POST` | `/api/ipam/v1/devices/{id}/packages/sync` | syncDevicePackages |
| `PUT` | `/api/ipam/v1/devices/{id}/bmc` | setDeviceBmc |
| `DELETE` | `/api/ipam/v1/devices/{id}/bmc` | clearDeviceBmc |
| `POST` | `/api/ipam/v1/devices/{id}/host-sync` | resyncDeviceHostSync |
| `POST` | `/api/ipam/v1/host-sync/resync` | resyncAllHosts |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### ipam:vlans:manage

Create, update and delete VLANs.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/ipam/v1/vlans` | createVlan |
| `PUT` | `/api/ipam/v1/vlans/{id}` | updateVlan |
| `DELETE` | `/api/ipam/v1/vlans/{id}` | deleteVlan |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### ipam:locations:manage

Create, update and delete locations.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/ipam/v1/locations` | createLocation |
| `PUT` | `/api/ipam/v1/locations/{id}` | updateLocation |
| `DELETE` | `/api/ipam/v1/locations/{id}` | deleteLocation |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### ipam:groups:manage

Create, update and delete IP and host groups and their members.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/ipam/v1/ip-groups` | createIpGroup |
| `PUT` | `/api/ipam/v1/ip-groups/{id}` | updateIpGroup |
| `DELETE` | `/api/ipam/v1/ip-groups/{id}` | deleteIpGroup |
| `POST` | `/api/ipam/v1/ip-groups/{id}/members` | addIpGroupMember |
| `PUT` | `/api/ipam/v1/ip-groups/{id}/members/{mid}` | updateIpGroupMember |
| `DELETE` | `/api/ipam/v1/ip-groups/{id}/members/{mid}` | removeIpGroupMember |
| `POST` | `/api/ipam/v1/host-groups` | createHostGroup |
| `PUT` | `/api/ipam/v1/host-groups/{id}` | updateHostGroup |
| `DELETE` | `/api/ipam/v1/host-groups/{id}` | deleteHostGroup |
| `POST` | `/api/ipam/v1/host-groups/{id}/members` | addHostGroupMember |
| `PUT` | `/api/ipam/v1/host-groups/{id}/members/{mid}` | updateHostGroupMember |
| `DELETE` | `/api/ipam/v1/host-groups/{id}/members/{mid}` | removeHostGroupMember |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### ipam:scan:run

Start subnet and address discovery scans and ping.

**UI actions**: `test` on `SubnetSnmp`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/ipam/v1/subnets/{id}/snmp/test` | testSubnetSnmp |
| `POST` | `/api/ipam/v1/subnets/{id}/scan` | scanSubnet |
| `POST` | `/api/ipam/v1/ip-addresses/{id}/ping` | pingIpAddress |
| `POST` | `/api/ipam/v1/ip-scans` | startIpScan |
| `POST` | `/api/ipam/v1/ip-scans/{id}/cancel` | cancelIpScan |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### ipam:dns:manage

Read and update the per-tenant DNS configuration.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `PUT` | `/api/ipam/v1/dns-config` | updateDnsConfig |
| `POST` | `/api/ipam/v1/dns-config/test` | testDnsConfig |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### ipam:backup:manage

Export and import tenant IPAM data.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/ipam/v1/backup/export` | exportBackup |
| `POST` | `/api/ipam/v1/backup/import` | importBackup |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### ipam:power:control

Out-of-band power status and actions via device BMC (platform-admin).

**UI actions**: `control` on `Power`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/ipam/v1/devices/{id}/power` | getDevicePower |
| `POST` | `/api/ipam/v1/devices/{id}/power` | setDevicePower |
| `GET` | `/api/ipam/v1/devices/{id}/sensors` | getDeviceSensors |
| `GET` | `/api/ipam/v1/devices/{id}/sel` | getDeviceSel |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### ipam:kvm:access

Start token-gated KVM console sessions (platform-admin).

**UI actions**: `access` on `Kvm`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/ipam/v1/devices/{id}/kvm-session` | startDeviceKvmSession |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### ipam:hostsync:manage

Enable or disable the host sync and edit its interface exclusions.

**UI actions**: `manage` on `HostSync`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `PUT` | `/api/ipam/v1/host-sync/settings` | updateHostSyncSettings |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.
<div class="guide-actions"><a href="how-to/ipam/docker.html">Install with Docker Compose →</a><a href="how-to/ipam/native.html">Install without Docker →</a><a href="downloads/ipam.zip">Download Compose bundle ↓</a></div>

## Dependencies and integration

**Required**: TimescaleDB, Valkey, key-encryption key, Auth, Portal, mesh identity.

**Optional or feature-dependent**: Inventory, Warden, Scheduler, ICMP capability, IPMI targets.

ICMP scanning needs `CAP_NET_RAW`; Docker deployments need the corresponding container capability. Host sync needs a compatible Inventory version and its host-report consumer/policy grants. IPMI/KVM and Warden integrations are configured separately.

The list describes infrastructure/features, not every transitive library. Check the linked deployment reference for exact versions, enabled features and peer grants. [Framework dependencies](architecture/dependencies.html) cover the shared Go libraries.

## Runtime and operation

| Item | Reference |
| --- | --- |
| Service binary | `ipamsvc` |
| Public example configuration | `deploy/dev.yaml`; adapt endpoints and paths for your environment |
| Native source build | Go `1.26.3`, toolchain `go1.26.8`, Node 22 for UI |
| Image repository | `ghcr.io/go-tangra/go-tangra-ipam`; choose a published compatible version |
| Private admin default | `127.0.0.1:9820`; check actual configuration |
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
| `Config` | `warden` | `Warden` |
| `Config` | `scan` | `Scan` |
| `Config` | `allocation` | `Allocation` |
| `Config` | `ipmi` | `IPMI` |
| `Config` | `kvm` | `KVM` |
| `Config` | `events` | `Events` |
| `Config` | `gateway` | `Gateway` |
| `Config` | `mesh_enroll` | `MeshEnroll` |
| `Config` | `limits_ipam` | `Limits` |
| `Config` | `host_sync` | `HostSync` |
| `Config` | `task_scheduler` | `TaskScheduler` |
| `TaskScheduler` | `enabled` | `bool` |
| `TaskScheduler` | `service` | `string` |
| `HostSync` | `enabled` | `bool` |
| `HostSync` | `inventory_service` | `string` |
| `HostSync` | `poll_interval_seconds` | `int` |
| `HostSync` | `workers` | `int` |
| `HostSync` | `page_size` | `int` |
| `HostSync` | `pace_ms` | `int` |
| `HostSync` | `request_timeout_seconds` | `int` |
| `HostSync` | `conflict_moves` | `int` |
| `HostSync` | `conflict_window_hours` | `int` |
| `HostSync` | `max_macs_per_port` | `int` |
| `HostSync` | `link_stale_days` | `int` |
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
| `Warden` | `endpoint` | `string` |
| `Warden` | `service` | `string` |
| `Scan` | `max_hosts` | `int` |
| `Scan` | `concurrency` | `int` |
| `Scan` | `timeout_ms` | `int` |
| `Scan` | `workers` | `int` |
| `Scan` | `max_retries` | `int` |
| `Scan` | `snmp_timeout_ms` | `int` |
| `Allocation` | `skip_first` | `int` |
| `Allocation` | `skip_last` | `int` |
| `Allocation` | `reserved_ranges` | `[]string` |
| `IPMI` | `timeout_seconds` | `int` |
| `KVM` | `token_ttl_seconds` | `int` |
| `KVM` | `session_seconds` | `int` |
| `KVM` | `console_origin` | `string` |
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

[Configuration structures and validation](https://github.com/go-tangra/go-tangra-ipam/blob/df4cab11e3d0a69aac0f90d97b83006dd808ab8a/internal/config/config.go)

## API operation index

These operations are extracted from the module's OpenAPI contract. Read the source contract for request/response schemas, permission checks and exact route bases; internal mesh endpoints must not be treated as anonymous public APIs.

| Method | Contract path | Operation |
| --- | --- | --- |
| `GET` | `/api/ipam/v1/subnets` | listSubnets |
| `POST` | `/api/ipam/v1/subnets` | createSubnet |
| `GET` | `/api/ipam/v1/subnets/tree` | getSubnetTree |
| `GET` | `/api/ipam/v1/subnets/{id}` | getSubnet |
| `PUT` | `/api/ipam/v1/subnets/{id}` | updateSubnet |
| `DELETE` | `/api/ipam/v1/subnets/{id}` | deleteSubnet |
| `GET` | `/api/ipam/v1/subnets/{id}/stats` | getSubnetStats |
| `POST` | `/api/ipam/v1/subnets/{id}/split` | splitSubnet |
| `GET` | `/api/ipam/v1/subnets/{id}/snmp` | getSubnetSnmp |
| `PUT` | `/api/ipam/v1/subnets/{id}/snmp` | setSubnetSnmp |
| `DELETE` | `/api/ipam/v1/subnets/{id}/snmp` | clearSubnetSnmp |
| `POST` | `/api/ipam/v1/subnets/{id}/snmp/test` | testSubnetSnmp |
| `POST` | `/api/ipam/v1/subnets/{id}/scan` | scanSubnet |
| `GET` | `/api/ipam/v1/ip-addresses` | listIpAddresses |
| `POST` | `/api/ipam/v1/ip-addresses` | createIpAddress |
| `POST` | `/api/ipam/v1/ip-addresses/allocate` | allocateIpAddress |
| `POST` | `/api/ipam/v1/ip-addresses/bulk-allocate` | bulkAllocateIpAddresses |
| `GET` | `/api/ipam/v1/ip-addresses/find` | findIpAddress |
| `GET` | `/api/ipam/v1/ip-addresses/suggest` | suggestIpAddresses |
| `GET` | `/api/ipam/v1/ip-addresses/{id}` | getIpAddress |
| `PUT` | `/api/ipam/v1/ip-addresses/{id}` | updateIpAddress |
| `DELETE` | `/api/ipam/v1/ip-addresses/{id}` | deleteIpAddress |
| `POST` | `/api/ipam/v1/ip-addresses/{id}/clear-conflict` | clearIpAddressConflict |
| `POST` | `/api/ipam/v1/ip-addresses/{id}/ping` | pingIpAddress |
| `GET` | `/api/ipam/v1/devices` | listDevices |
| `POST` | `/api/ipam/v1/devices` | createDevice |
| `GET` | `/api/ipam/v1/devices/{id}` | getDevice |
| `PUT` | `/api/ipam/v1/devices/{id}` | updateDevice |
| `DELETE` | `/api/ipam/v1/devices/{id}` | deleteDevice |
| `GET` | `/api/ipam/v1/devices/{id}/addresses` | getDeviceAddresses |
| `GET` | `/api/ipam/v1/devices/{id}/interfaces` | getDeviceInterfaces |
| `POST` | `/api/ipam/v1/devices/{id}/interfaces` | createDeviceInterface |
| `DELETE` | `/api/ipam/v1/devices/{id}/interfaces/{ifid}` | deleteDeviceInterface |
| `GET` | `/api/ipam/v1/devices/{id}/packages` | listDevicePackages |
| `POST` | `/api/ipam/v1/devices/{id}/packages/sync` | syncDevicePackages |
| `GET` | `/api/ipam/v1/devices/{id}/host-groups` | getDeviceHostGroups |
| `GET` | `/api/ipam/v1/devices/{id}/power` | getDevicePower |
| `POST` | `/api/ipam/v1/devices/{id}/power` | setDevicePower |
| `GET` | `/api/ipam/v1/devices/{id}/sensors` | getDeviceSensors |
| `GET` | `/api/ipam/v1/devices/{id}/sel` | getDeviceSel |
| `GET` | `/api/ipam/v1/devices/{id}/bmc` | getDeviceBmc |
| `PUT` | `/api/ipam/v1/devices/{id}/bmc` | setDeviceBmc |
| `DELETE` | `/api/ipam/v1/devices/{id}/bmc` | clearDeviceBmc |
| `GET` | `/api/ipam/v1/devices/{id}/host-sync` | getDeviceHostSync |
| `POST` | `/api/ipam/v1/devices/{id}/host-sync` | resyncDeviceHostSync |
| `GET` | `/api/ipam/v1/devices/{id}/hardware` | getDeviceHardware |
| `GET` | `/api/ipam/v1/devices/{id}/guests` | listDeviceGuests |
| `POST` | `/api/ipam/v1/devices/{id}/kvm-session` | startDeviceKvmSession |
| `GET` | `/api/ipam/v1/host-sync/settings` | getHostSyncSettings |
| `PUT` | `/api/ipam/v1/host-sync/settings` | updateHostSyncSettings |
| `GET` | `/api/ipam/v1/host-sync/status` | getHostSyncStatus |
| `POST` | `/api/ipam/v1/host-sync/resync` | resyncAllHosts |
| `GET` | `/api/ipam/v1/arp/settings` | getArpSettings |
| `PUT` | `/api/ipam/v1/arp/settings` | updateArpSettings |
| `GET` | `/api/ipam/v1/vlans` | listVlans |
| `POST` | `/api/ipam/v1/vlans` | createVlan |
| `GET` | `/api/ipam/v1/vlans/{id}` | getVlan |
| `PUT` | `/api/ipam/v1/vlans/{id}` | updateVlan |
| `DELETE` | `/api/ipam/v1/vlans/{id}` | deleteVlan |
| `GET` | `/api/ipam/v1/vlans/{id}/subnets` | getVlanSubnets |
| `GET` | `/api/ipam/v1/locations` | listLocations |
| `POST` | `/api/ipam/v1/locations` | createLocation |
| `GET` | `/api/ipam/v1/locations/tree` | getLocationTree |
| `GET` | `/api/ipam/v1/locations/{id}` | getLocation |
| `PUT` | `/api/ipam/v1/locations/{id}` | updateLocation |
| `DELETE` | `/api/ipam/v1/locations/{id}` | deleteLocation |
| `GET` | `/api/ipam/v1/ip-groups` | listIpGroups |
| `POST` | `/api/ipam/v1/ip-groups` | createIpGroup |
| `GET` | `/api/ipam/v1/ip-groups/check` | checkIpInGroup |
| `GET` | `/api/ipam/v1/ip-groups/{id}` | getIpGroup |
| `PUT` | `/api/ipam/v1/ip-groups/{id}` | updateIpGroup |
| `DELETE` | `/api/ipam/v1/ip-groups/{id}` | deleteIpGroup |
| `GET` | `/api/ipam/v1/ip-groups/{id}/members` | listIpGroupMembers |
| `POST` | `/api/ipam/v1/ip-groups/{id}/members` | addIpGroupMember |
| `PUT` | `/api/ipam/v1/ip-groups/{id}/members/{mid}` | updateIpGroupMember |
| `DELETE` | `/api/ipam/v1/ip-groups/{id}/members/{mid}` | removeIpGroupMember |
| `GET` | `/api/ipam/v1/host-groups` | listHostGroups |
| `POST` | `/api/ipam/v1/host-groups` | createHostGroup |
| `GET` | `/api/ipam/v1/host-groups/{id}` | getHostGroup |
| `PUT` | `/api/ipam/v1/host-groups/{id}` | updateHostGroup |
| `DELETE` | `/api/ipam/v1/host-groups/{id}` | deleteHostGroup |
| `GET` | `/api/ipam/v1/host-groups/{id}/members` | listHostGroupMembers |
| `POST` | `/api/ipam/v1/host-groups/{id}/members` | addHostGroupMember |
| `PUT` | `/api/ipam/v1/host-groups/{id}/members/{mid}` | updateHostGroupMember |
| `DELETE` | `/api/ipam/v1/host-groups/{id}/members/{mid}` | removeHostGroupMember |
| `GET` | `/api/ipam/v1/ip-scans` | listIpScans |
| `POST` | `/api/ipam/v1/ip-scans` | startIpScan |
| `GET` | `/api/ipam/v1/ip-scans/{id}` | getIpScan |
| `POST` | `/api/ipam/v1/ip-scans/{id}/cancel` | cancelIpScan |
| `GET` | `/api/ipam/v1/health` | health |
| `GET` | `/api/ipam/v1/stats` | getStats |
| `GET` | `/api/ipam/v1/dns-config` | getDnsConfig |
| `PUT` | `/api/ipam/v1/dns-config` | updateDnsConfig |
| `POST` | `/api/ipam/v1/dns-config/test` | testDnsConfig |
| `POST` | `/api/ipam/v1/backup/export` | exportBackup |
| `POST` | `/api/ipam/v1/backup/import` | importBackup |
| `GET` | `/api/ipam/v1/stream` | streamEvents |

[OpenAPI: api/openapi/ipam.yaml](https://github.com/go-tangra/go-tangra-ipam/blob/df4cab11e3d0a69aac0f90d97b83006dd808ab8a/api/openapi/ipam.yaml)

## Detailed source references

- [README.md](sources/ipam/README.html) — captured at `df4cab11e3d0`.
- [deploy/README.md](sources/ipam/deploy/README.html) — captured at `df4cab11e3d0`.

## Limits, diagnostics and recovery

ICMP scanning needs `CAP_NET_RAW`; Docker deployments need the corresponding container capability. Host sync needs a compatible Inventory version and its host-report consumer/policy grants. IPMI/KVM and Warden integrations are configured separately.

Use the module's operations/deployment reference for retention, backup/restore, refusal behavior, interface examples and feature limitations. The installation guides cover common readiness, identity, registration and storage failures.

## Upstream overview: go-tangra-ipam

Tenant-scoped IP address management for the
[go-tangra v4 platform](https://github.com/go-tangra/go-tangra).

Hierarchical subnets with utilization, IP addresses (first-free and bulk
allocation, conflict detection, find/suggest), devices (interfaces, L2 links, OS
packages), VLANs, a location hierarchy and IP/host groups. The module also runs
**active network operations**: asynchronous discovery scans (ICMP/SNMP/TCP),
ping, IPMI/BMC power control and a token-gated KVM console proxy. Power, IPMI
and KVM are platform-admin only; every active operation is tenant-scoped,
bounded and audited.

**SNMP credentials** live on subnets, sealed by ipam itself and write-only;
child subnets inherit them (see [SNMP credentials](#snmp-credentials)). **BMC
credentials** are not stored by ipam: a device holds only a Warden secret
reference, and the password is fetched from Warden for the signed-in user at
each power, sensor or KVM action (see [BMC credentials](#bmc-credentials)).

**Host sync**: hosts running the inventory agent keep their devices,
interfaces, addresses (in auto-created subnets when needed), BMC management
addresses, hypervisor guests, pending updates and switch ports current in IPAM
(see [Host sync](#host-sync)).

**ARP-based MAC linking**: scans with SNMP discovery read the ARP and
neighbour tables of the routers, firewalls and layer-3 switches that answer,
record the MAC of every active address (never overwriting an agent or manual
MAC) and link agentless hosts to their switch port (see
[ARP-based MAC linking](#arp-based-mac-linking)).

Operations: [`deploy/README.md`](sources/ipam/deploy/README.html).
Design history: `specs/011-ipam-service` (walkthrough in `quickstart.md`).

## Place in the platform

```
go-tangra/go-tangra          platform module + @go-tangra/ui kit
        |
go-tangra-auth  <---->  go-tangra-portal (gateway)  <---->  go-tangra-ipam
                              |                              |       ^
                         go-tangra-lcm (SVIDs)        go-tangra-warden   dns (ipam sdk)
                                                             go-tangra-inventory (host reports)
```

- Built on `github.com/go-tangra/go-tangra/v4` (mTLS transports, identity,
  service policy, audit, observability).
- Verifies platform tokens and registers its permissions, module roles and
  built-in role grants with the auth SDK (`github.com/go-tangra/go-tangra-auth/sdk/v4`).
- Registers with the gateway through the portal SDK
  (`github.com/go-tangra/go-tangra-portal/sdk/v4`), which fronts the browser API
  (`/api/ipam`), the KVM proxy (`/bmc/`) and the federated UI remote.
- Enrolls for its workload identity with lcm (`github.com/go-tangra/go-tangra-lcm/sdk/v4`).
- Reads host reports from inventory (`github.com/go-tangra/go-tangra-inventory/sdk/v4`,
  `inventory.v1.HostReportService`, inventory >= 4.3.0).

## Modules in this repository

| Module | Path | Consumers |
|---|---|---|
| `github.com/go-tangra/go-tangra-ipam/v4` | `/` | the service (`cmd/ipamsvc`) and `pkg/ipammanifest` |
| `github.com/go-tangra/go-tangra-ipam/sdk/v4` | `sdk/` | other services: the `ipam.v1` protobuf API and `pkg/ipamclient` (mTLS client) |

The service builds against the in-repo SDK through
`replace github.com/go-tangra/go-tangra-ipam/sdk/v4 => ./sdk`. Consumers use the
SDK's published `sdk/vX.Y.Z` tag.

## Layout

| Path | Purpose |
|------|---------|
| `cmd/ipamsvc` | service binary (serve, `bootstrap`: migrate and exit; `version`) |
| `internal/app` | wiring: config, platform, store, events, HTTP/gRPC, gateway lease, auth registration (permissions, module roles), scan workers |
| `internal/{subnets,addresses,devices,vlans,locations,groups}` | domain services |
| `internal/ipnet` | pure CIDR/IP arithmetic that bounds allocation and scans |
| `internal/scan` | scan executor, ICMP/SNMP/TCP probes and the SNMP credentials test |
| `internal/snmpcred` | pure SNMP credential rules: validation, sealing binding, inheritance, error scrubbing |
| `internal/ipmi`, `internal/kvm` | BMC power/inventory and the KVM console proxy |
| `internal/warden` | Warden secrets client acting for the signed-in user (plus an in-memory fake) |
| `internal/bmc` | BMC access decisions: reference, BMC address, credentials, reasons (feature 024) |
| `internal/{invclient,hostreport,hostplan,hostsync}` | host sync: inventory client, report validation, pure planner, poller/reconcile/apply and admin service |
| `internal/portlink` | links reported host interfaces and addresses with a MAC to switch ports from SNMP FDB/LLDP data |
| `internal/{arpplan,arpcfg}` | ARP-based MAC linking: pure planner (filters, MAC provenance) and per-tenant settings |
| `internal/{authz,sealed,audit,stream,backup,stats,dnscfg}` | authorization, sealed owner data, audit vocabulary, event stream, tenant backup, statistics, DNS settings |
| `internal/{repo,store,memstore}` | repository, SQL bindings (RLS, goose migrations), in-memory store |
| `pkg/ipammanifest` | gateway manifest built from the OpenAPI document |
| `ui` | Vue 3 + FlyonUI federated remote on `@go-tangra/ui` |
| `api/openapi`, `sdk/api/proto` | contracts (`ipam.yaml`, `ipam.v1`) |
| `deploy` | policy, operations notes and a development key |

## Build and test

You need Go 1.26, Node 22, Docker (for the integration suite and the image), and a
GitHub token with `read:packages` to install `@go-tangra/ui` from GitHub Packages.

```bash
go build ./... && go vet ./... && go test -race ./...
(cd sdk && go vet ./... && go test -race ./...)
(cd sdk && buf lint)
make test-integration                     # -tags integration, TimescaleDB via testcontainers (needs Docker)
make lint cover vuln

cd ui
export NODE_AUTH_TOKEN=$(gh auth token)   # ui/.npmrc only references this variable
npm ci && npm run lint && npm run test:unit && npm run build
```

The unit coverage gate requires at least 80 % overall and 100 % for
`internal/{authz,sealed,ipnet,hostreport,hostplan}`. `make fuzz` runs every fuzz
target (`FUZZTIME`, default 10 s each). Generated code, SQL bindings, wiring and the
raw network probes are covered by the integration suite instead. The Playwright
specs in `ui/tests/e2e` need a running platform and operator credentials; they
skip otherwise.

## Run

The service runs in the go-tangra platform stack (`deploy/stack` in
[go-tangra](https://github.com/go-tangra/go-tangra)), next to TimescaleDB, Valkey,
the gateway, lcm and warden. The stack mounts its configuration at
`/app/deploy/container.yaml` and the development key-encryption key at
`/app/deploy/kek.dev`. `deploy/kek.dev` in this repository is a development key
only; it is excluded from the image.

```bash
ipamsvc bootstrap -config deploy/container.yaml    # apply migrations and exit
ipamsvc -config deploy/container.yaml              # serve (applies migrations)
```

## Container image

The image is `ghcr.io/go-tangra/go-tangra-ipam`, built by
`.github/workflows/ci.yaml`. It carries `ipamsvc` with the embedded UI remote.

```bash
docker buildx build --secret id=npm_token,env=NODE_AUTH_TOKEN \
  --build-arg APP_VERSION=4.0.0 -t go-tangra-ipam:dev .
docker run --rm go-tangra-ipam:dev version
```

The image runs `ipamsvc -config deploy/container.yaml` as user `app`
(uid 10001) and ships `deploy/policy.yaml`. It contains no configuration and no
key material: deployments mount their own `deploy/container.yaml` and
key-encryption key. `ipamsvc` carries the file capability `cap_net_raw+ep` so
ICMP discovery scans work without root; the container must keep `NET_RAW` in its
capability set (Docker's default; the platform stack adds it explicitly).

## Host sync

The inventory agent reports each host's interfaces (kind, speed, addresses with
prefix and flags, gateway), primary addresses, virtualization, BMC LAN
settings (no credentials), Proxmox guests and Linux update state to the
inventory module. IPAM pulls a projection of each host's latest report from
inventory over the mesh (`inventory.v1.HostReportService`, SPIFFE mTLS):

- a **poll** every `host_sync.poll_interval_seconds` (60) fetches the reports
  that changed since the tenant's watermark; a per-tenant **reconcile** (tenant
  setting, default hourly) compares digests of every host and marks devices of
  retired or deleted hosts as *no longer reported* (nothing is deleted);
- each host is applied in **one tenant transaction** holding a per-tenant
  advisory lock and `FOR SHARE` on the tenant settings, so disabling the sync
  stops every later change; every change is written as an audit row in the
  same transaction (actor `system`/`hostsync`);
- the device is matched by inventory host id, else a unique real serial, else a
  non-generic hostname; reported data wins for the reported fields only —
  description, tags, location, rack, asset tag, status, contact, BMC secret
  reference, firmware and groups are never changed; addresses are placed in the
  most specific subnet (a subnet named after the reported network is created
  with origin `host_sync` when none contains it), moved from other devices with
  the previous device audited, flagged as a conflict after repeated moves, and
  released (not deleted) when the host stops reporting them; loopback,
  link-local, temporary IPv6 and container/virtual bridge interfaces (tenant
  exclusion patterns) are not recorded;
- after SNMP scans and host-sync runs, host interface MACs are correlated with
  the switches' forwarding tables and LLDP neighbours to show the switch port
  (and VLAN) each host is connected to.

Configuration (`host_sync` section, all optional):

```yaml
host_sync:
  enabled: true                 # global kill switch (false: nothing is applied)
  inventory_service: inventory
  poll_interval_seconds: 60     # 10-3600
  workers: 2                    # tenants in parallel, 1-8
  page_size: 100                # 1-200
  pace_ms: 10                   # pause between hosts
  request_timeout_seconds: 30
  conflict_moves: 3             # moves within the window that flag a conflict, 2-100
  conflict_window_hours: 24     # 1-168
  max_macs_per_port: 16         # switch ports with more MACs are never inferred, 1-256
  link_stale_days: 14           # switch-port links not re-confirmed are cleared
```

Per tenant, administrators enable or disable the sync, set the reconcile
interval and edit the interface exclusions (`/ipam/host-sync`, permission
`hostsync:manage`); anyone with `devices:manage` can re-sync one host or all.
Until inventory >= 4.3.0 is deployed and its policy has the `ipam-hostsync` rule
(see `deploy/README.md`), the sync reports `degraded` and writes nothing.

Audit vocabulary of the sync: `device_created`, `device_updated`,
`device_not_reported`, `interface_created`, `interface_updated`,
`interface_not_reported`, `subnet_created`, `address_created`,
`address_updated`, `address_moved`, `address_released`, `address_conflict`,
`address_conflict_cleared`, `packages_updated`, `hypervisor_linked`,
`hypervisor_unlinked`, `port_linked`, `port_unlinked`, `hostsync_run`,
`hostsync_settings_updated`, `hostsync_resync_requested`, `hardware_reported`,
`hardware_updated`.

### Device hardware

Inventory agents >= 4.4.0 (feature 023, inventory SDK >= v4.2.0) add a
hardware section to the host report: BIOS, system/board/chassis, processors,
memory (every slot, error correction), physical disks and filesystems with the
disks they live on. The host sync validates it again (256 disks, 1024 memory
slots, 256 processors, 1024 filesystems, 64 disk references per filesystem,
cleaned strings, closed media/interface sets, 256 KiB profile bound; every
correction is a host-sync issue) and stores it per host-reported device in
`ipam_device_hardware` (migration 0009, RLS):

- the device page gets a **Hardware** tab (cards BIOS, System / board /
  chassis, Processors, Memory with empty slots greyed, Disks with a removable
  badge, Filesystems with usage bars) and a summary line
  (`2× Xeon Silver 4310 · 24 cores / 48 threads · 512 GiB DDR4 (16/16 slots) ·
  3 disks, 11.8 TB`); the device list gains CPU and memory columns and the
  `has_hardware=true|false` filter; a host-reported device whose agent has not
  reported hardware yet shows an explanatory empty state, manual and scanned
  devices show no tab;
- `GET /api/ipam/v1/devices/{id}/hardware` (`ipam:read`) returns the profile;
  devices carry a read-only `hardware_summary` (HTTP and gRPC). Hardware is
  reported data: it is replaced by each report, there is no write route, and a
  device create/update carrying `hardware_summary`/`hardware` is refused (400);
  device columns (serial, firmware, description, …) are never written from it;
- the first report stores it with `hardware_reported` (summary); a changed
  report is audited as one `hardware_updated` row listing the field changes
  (`bios.version`, `system.serial`, `memory.slot[<locator>]`,
  `disk[<serial or name>]`, `processor[<socket>]`, … with before/after, at most
  100 plus `changes_truncated`); filesystem usage alone is refreshed without
  an audit row; a report without hardware (older agent or inventory) leaves the
  stored hardware untouched.

Hardware therefore appears once inventory >= 4.4.0 is deployed and the host's
agent is >= 4.4.0; older inventories and agents keep working without it.

## SNMP credentials

A subnet can hold its own SNMP credentials (feature 021): SNMP v2c (community)
or SNMP v3 (user, `authNoPriv` or `authPriv`, authentication protocol MD5,
SHA-1, SHA-224/256/384/512 and password, privacy protocol DES or AES-128/192/256
and password; MD5, SHA-1 and DES are labelled weak). v3 passwords need at least
8 characters; no value may be empty or longer than 256 characters.

- **Storage**: table `ipam_subnet_snmp` (migration 0006, row-level security):
  version, level and protocols in clear, the secret values as one envelope
  blob sealed with the module KEK and bound to tenant and subnet, so a blob
  copied to another row or tenant does not open. Deleting the subnet deletes
  its credentials.
- **Write-only**: no response, event, backup, audit row or log line carries a
  community, v3 user or password; reads return only whether credentials are
  configured, their version, level and where the effective ones come from.
  Editing a subnet never touches its credentials.
- **Inheritance**: a subnet without its own credentials uses those of its
  nearest ancestor that has them (never across tenants). Subnet responses carry
  the read-only `snmp` summary (`none`, `own` or `inherited` with the source
  subnet) and `snmp_version` is the effective version.
- **Scans**: a scan with SNMP discovery resolves and opens the effective
  credentials once, when it starts, and records the SNMP phase on the job:
  `snmp_status` (`not_requested`, `no_live_hosts`, `no_credentials`,
  `credentials_unreadable`, `ran`), `snmp_source_subnet_id`, `snmp_probed`,
  `snmp_no_answer`, `snmp_rejected` and `snmp_discovered_count`.
- **Endpoints**: `GET /api/ipam/v1/subnets/{id}/snmp` (`ipam:read`),
  `PUT` set/replace and `DELETE` clear (`subnets:manage`),
  `POST /api/ipam/v1/subnets/{id}/snmp/test` (`scan:run`): probes one usable
  address inside the subnet within the SNMP timeout plus 2 seconds, at most 10
  tests per user per minute, and answers `ok` (sysName, sysDescr),
  `no_response`, `auth_failed`, `unknown_user`, `privacy_failed`,
  `no_credentials`, `credentials_unreadable` or `error`.
- **Audit**: `snmp_credentials_set`, `snmp_credentials_replaced`,
  `snmp_credentials_cleared`, `snmp_credentials_tested`, with neutral detail
  keys only (`protocol_version`, `security_level`, `previous_version`,
  `target`, `outcome`, `source_subnet_id`).
- **Backup**: exports carry the summary only; an import leaves SNMP
  unconfigured and lists the subnets to re-enter in `snmp_credentials_required`.
- **Legacy**: the never-functional warden reference `snmp_secret_ref` is no
  longer written or returned; at start ipam logs how many subnets still carry
  one so their credentials can be entered again.

## BMC credentials

Power status and actions, sensors, the SEL and KVM sessions use a Warden secret
(username + password) attached to the device (feature 024).

- **Attach**: `PUT /api/ipam/v1/devices/{id}/bmc` `{"reference": "<warden secret id>"}`
  (`devices:manage`) — ipam asks Warden (`Secrets/Get`) *as the acting user*
  whether they may read it and stores only the id; audited
  `bmc_reference_set` / `bmc_reference_changed`; `DELETE` clears it
  (`bmc_reference_cleared`). The device body cannot set or change the
  reference. The UI lists the secrets through Warden's own API
  (`/api/warden/v1/secrets/search`), never requesting a password.
- **Status**: `GET /api/ipam/v1/devices/{id}/bmc` (`ipam:read`) — the secret's
  name/username/folder as the viewer may see it in Warden, the access state
  and the BMC address: the management IP, else the address the inventory agent
  reported on the `bmc` interface (never the host's primary IP).
- **Use**: each out-of-band call (platform-admin) fetches the password with
  `Secrets/Get` + `Secrets/GetPassword`, forwarding the caller's platform token
  over the mesh, so Warden applies its own per-secret check and audit. Nothing
  is cached; a rotated password is used on the next call. The BMC is contacted
  only after Warden released the credentials.
- **Reasons**: `bmc_not_configured`, `bmc_no_address` (409),
  `bmc_secret_forbidden` (403), `bmc_secret_not_found` (409),
  `warden_unavailable` (503), `bmc_unreachable` (504), `bmc_auth_failed`,
  `bmc_error` (502, with `detail.address`); a KVM session also answers
  `bmc_2fa_required` (409) and `bmc_session_limit` (502), see
  [KVM console](#kvm-console). The Power / KVM tab explains each.
- **Audit**: power actions (`power_action`) and KVM sessions
  (`kvm_session_started`) with outcome and reason; reads go to the module log.
- **Policy**: Warden must allow `spiffe://<trust>/svc/ipam` exactly
  `/warden.v1.Secrets/Get` and `/warden.v1.Secrets/GetPassword` (rule
  `ipam-bmc-secrets` in Warden's policy); without it every call reads as
  `warden_unavailable`. The host URL of the secret may select the IPMI session
  (`lanplus://host:port` for 2.0, `lan://` for 1.5); otherwise auto on 623.
- **Backup**: references are not exported and never imported; overwriting an
  existing device keeps its reference.

### KVM console origin (feature 025)

The BMC's HTML5 console is vendor JavaScript, so it is never served on the
portal origin. The gateway's console listener (`console:` in the gateway
configuration, `https://<public host>:8444`) forwards only `/bmc/` to IPAM,
and IPAM is told that origin:

```yaml
kvm:
  token_ttl_seconds: 60      # single-use start token in the console URL
  session_seconds: 3600      # console session the token is exchanged for
  console_origin: https://portal.example.com:8444
```

- **Start**: `POST /devices/{id}/kvm-session` logs in to the BMC web UI
  (see [KVM console](#kvm-console)) and returns `console_url =
  <console_origin>/bmc/<device>/cgi/url_redirect.cgi?url_name=man_ikvm_html5_bootstrap&kvmtoken=<token>`,
  the BMC's HTML5 viewer (relative
  when `console_origin` is empty — the Power / KVM tab then shows "KVM console
  origin not configured" instead of a frame the browser would refuse).
- **Session**: the first request with the token consumes it and sets
  `freya_kvm=<session>` (`Path=/bmc/<device>/; Secure; HttpOnly;
  SameSite=Strict`, `Max-Age=session_seconds`); a replayed token is refused.
- **WebSocket**: `/bmc/<device>/__kvmws` needs the session cookie and, when
  `console_origin` is set, `Origin` equal to it.
- **BMC**: receives only IPAM's server-side BMC session (`SID` cookie and/or
  `X-Auth-Token`), never browser cookies or headers; its `Set-Cookie` and
  `X-Auth-Token` never reach the browser as headers.
- Sessions live in the IPAM process: run one IPAM instance (or sticky routing)
  for consoles.

### KVM console

`POST /devices/{id}/kvm-session` logs in to the BMC web UI server-side before
it answers, with the Warden credentials, so a refused login is explained in the
Power / KVM tab instead of inside the console frame. Supported Supermicro
login flows (tried in this order, one attempt each):

1. **Redfish session** (X12 and later, e.g. web UI 1.8.x, whose login page
   still shows the `/cgi/login.cgi` form but never posts it):
   `POST /redfish/v1/SessionService/Sessions {"UserName","Password"}` → the
   `X-Auth-Token` header and the session URI (`Location` / `Id`). A 401/403
   ends the login there (`bmc_auth_failed`), so a wrong password costs one
   failed attempt.
2. **Form login** (older firmware): `POST /cgi/login.cgi` with `name`, `pwd`,
   `check=00` → the `SID` cookie. An X11 that offers both gets both.

The proxy sets the token/cookie on every request and WebSocket to the BMC.
HTML pages the BMC serves get a small script at the top of `<head>` that
seeds `sessionStorage._x_auth` / `_sess_idx` (the BMC UI's own Redfish
session, on the isolated console origin only), keeps the page's
absolute-path calls (`/redfish/v1/...`) under `/bmc/<device>/` and routes its
WebSocket through `/bmc/<device>/__kvmws`.

One BMC session per (BMC, user) is shared by all consoles and deleted on the
BMC (`DELETE` of the Redfish session, `/cgi/logout.cgi` for a SID) when the
last console using it ends, and on shutdown — BMCs allow only a few web
sessions. A session the BMC expired (401) is replaced by a new login.

Limitations:

- **Two-factor login**: a BMC user with 2FA enabled (`Oem.Supermicro.TwoFAEnabled`)
  cannot be logged in automatically; the session is deleted again and the
  start answers `bmc_2fa_required` — open the BMC web UI directly or use a
  BMC user without 2FA for the Warden secret.
- **Session limit**: when the BMC answers `SessionLimitExceeded` the start
  answers `bmc_session_limit` — close other BMC web sessions (or wait for them
  to time out) and try again.

## ARP-based MAC linking

Agentless hosts (printers, access points, cameras, BMCs, servers without the
inventory agent) get their MAC and switch port from the network (feature 022).

- **Collection**: a scan with SNMP discovery also walks each answering
  device's `ipNetToPhysicalTable` (IPv4 and IPv6 neighbours), falling back to
  the legacy `ipNetToMediaTable`, with the subnet's effective SNMP credentials
  and read-only requests, at most 65,536 entries per device per scan (a capped
  or interrupted read counts as partial).
- **Filters**: entries are ignored and counted by reason when the MAC is
  incomplete or invalid (`invalid`), multicast or broadcast (`multicast`),
  a VRRP or HSRP virtual-router MAC (`virtual_router`), a network device's own
  interface MAC (`network_device`), answers for more than the proxy threshold
  of IPs in one scan (`proxy_arp`, default 8), comes from an excluded device
  (`excluded_device`) or the IP is outside every subnet of the tenant
  (`outside_subnets`). ARP data never crosses tenants.
- **Provenance**: every address records `mac_source` (`agent` from the host
  sync, `manual` from the address API, `arp`), and for ARP the reporting
  device (`mac_source_device_id`) and `mac_seen_at`. ARP fills an empty MAC and
  updates a MAC it learned itself; it never changes an agent or manual MAC, and
  records a disagreement in `mac_conflict` instead (cleared when they agree
  again). An IP inside a known subnet without an address record gets one
  (status active, `origin: arp`); such addresses are never deleted
  automatically. MACs that existed before migration 0008 were backfilled as
  `agent` (host-reported addresses) or `manual`. The same IP reported by
  several devices: the last device in id order wins and the disagreement
  counts as a conflict.
- **Switch ports**: the switch-port correlation links every address with a
  MAC (any source) with the same rules as reported interfaces (fewest-MAC
  port, maximum MACs per access port, uplinks and network-device MACs
  excluded, stale links cleared). Addresses carry `link` (switch, port, VLAN,
  source, last seen); an address whose MAC a reported interface carries shows
  that interface's link; switch ports list `behind_addresses`. A host
  learned on several switches (MLAG / LACP bond across a switch pair) gets
  one link per switch (fewest-MAC port on each; a tie between two ports of
  the same switch links nothing there): interfaces and addresses list them
  in `links` (primary first; `link` and the flat columns are the primary),
  and the host shows behind both switches' ports.
- **Scan result**: `arp_status` (`ran`, `disabled`, `failed`), `arp_devices`,
  `arp_partial`, `arp_entries`, `arp_applied`, `arp_created`, `arp_conflicts`
  and `arp_ignored` (reason to count).
- **Search**: `GET /api/ipam/v1/ip-addresses?mac=` takes a full or partial
  MAC in colon, dash, dot or bare notation (2-12 hex digits; otherwise 422
  with `detail.field = mac`).
- **Settings**: `GET /api/ipam/v1/arp/settings` (`ipam:read`) and `PUT`
  (`subnets:manage`): `enabled` (default on), `excluded_devices` (up to 256
  existing devices never used as ARP sources) and `proxy_threshold` (2-256).
  Stored in `ipam_arp_settings` (row-level security); a tenant that never
  saved them uses the defaults.
- **Audit**: `mac_learned`, `mac_changed`, `mac_conflict`, `address_created`
  (`origin: arp`), `port_linked`/`port_unlinked` for addresses, one `arp_run`
  summary per scan (actor system/scan) and `arp_settings_updated` (the user),
  with neutral detail keys (`address`, `mac`, `previous_mac`, `observed_mac`,
  `source_device_id`, `job_id`).

## API permissions

`ipam:read`, `subnets:manage`, `addresses:manage`, `addresses:allocate`,
`devices:manage`, `vlans:manage`, `locations:manage`, `groups:manage`,
`scan:run`, `dns:manage`, `backup:manage`, `power:control`, `kvm:access`,
`hostsync:manage`. The gateway enforces the per-route permission from the
manifest; power, IPMI and KVM additionally require the platform-admin role.

## Roles

The module registers its permissions with auth at start and every five
minutes, together with ready-made module roles that auth offers in every
tenant (locked; administrators assign them or clone them into custom roles):

| Role | Display name | Permissions |
|---|---|---|
| `administrator` | IPAM administrator | all 14, including `power:control`, `kvm:access` (the handlers still require platform-admin for those) and `hostsync:manage` |
| `operator` | IPAM operator | `ipam:read`, `addresses:allocate`, `scan:run` |
| `viewer` | IPAM viewer | `ipam:read` |

Built-in role grants (scoped to IPAM by auth): `owner` and `admin` hold every
permission; `operator` holds everything except `power:control`, `kvm:access`
and `hostsync:manage`; `member` and `auditor` hold `ipam:read`.

## Versioning

- Service releases are tagged `vX.Y.Z`. CI publishes the image as `X.Y.Z`,
  `X.Y`, `X` and `sha-<short>`. There is no `latest` tag.
- The SDK is released separately with `sdk/vX.Y.Z` tags. These tags never build an image.
- v4.0.0 rebuilds the service on the go-tangra v4 platform. The v3 line stays on
  the `v3` branch and its `v3.x` tags.
