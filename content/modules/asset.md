# Asset

IT asset lifecycle, consumables, licenses, insurance and depreciation.

**Architecture role**: Business modules. [See the complete component map](architecture/index.html).

**Documented source**: `ff6055e17e18` · nearest local service tag `v4.4.3` · v4 major. [Repository at this revision](https://github.com/go-tangra/go-tangra-asset/tree/ff6055e17e18f941a945c8cc8d1e1bf2ee44afa7). Tags are source metadata, not a claim of image publication or cross-module compatibility.


## Permissions and authorization

This catalogue contains **13 permissions** declared by the [module manifest](https://github.com/go-tangra/go-tangra-asset/blob/ff6055e17e18f941a945c8cc8d1e1bf2ee44afa7/pkg/assetmanifest/manifest.go) at the revision above. Custom-role references use `module:resource:action`; the manifest and API contract use the local `resource:action` form. The action names are distinct grants: do not assume `manage` automatically includes `read` or another action.

Module permissions gate actions within the authenticated tenant. The endpoint still enforces its resource and workflow checks; a UI ability describes presentation and does not replace server authorization.

[How to assign and verify permissions](architecture/security.html#assign-and-verify-permissions). Module roles and built-in grant mappings are defined in the linked manifest; review those mappings before assigning a broad role.

| Qualified permission | What it allows |
| --- | --- |
| `asset:assets:read` | List and read assets, org records, documents, users and the live stream |
| `asset:assets:manage` | Create, update and delete assets |
| `asset:assets:assign` | Assign and unassign assets to users |
| `asset:categories:manage` | Manage the category tree |
| `asset:suppliers:manage` | Manage suppliers |
| `asset:locations:manage` | Manage the location tree |
| `asset:consumables:manage` | Manage consumables (stock) |
| `asset:licenses:manage` | Manage software licenses |
| `asset:insurance:manage` | Manage insurance policies and asset coverage |
| `asset:documents:manage` | Upload and delete photos and documents |
| `asset:inventory:sync` | Preview and execute inventory synchronisation |
| `asset:stats:read` | Read the asset dashboard statistics |
| `asset:backup:manage` | Export and import tenant asset data |

### asset:assets:read

List and read assets, org records, documents, users and the live stream.

**UI actions**: `read` on `Asset`, `AssetCategory`, `AssetSupplier`, `AssetLocation`, `AssetConsumable`, `AssetLicense`, `AssetInsurance`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Assets, Categories, Suppliers, Locations, Consumables, Licenses, Insurance, Document search.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/asset/v1/assets` | listAssets |
| `GET` | `/api/asset/v1/assets/{id}` | getAsset |
| `GET` | `/api/asset/v1/assets/{id}/assignments` | listAssetAssignments |
| `GET` | `/api/asset/v1/assets/{id}/photo` | getAssetPhoto |
| `GET` | `/api/asset/v1/documents/search` | searchDocuments |
| `GET` | `/api/asset/v1/assets/{id}/documents` | listAssetDocuments |
| `GET` | `/api/asset/v1/assets/{id}/documents/{doc_id}/download` | downloadAssetDocument |
| `GET` | `/api/asset/v1/categories` | listCategories |
| `GET` | `/api/asset/v1/categories/tree` | getCategoryTree |
| `GET` | `/api/asset/v1/categories/{id}` | getCategory |
| `GET` | `/api/asset/v1/suppliers` | listSuppliers |
| `GET` | `/api/asset/v1/suppliers/{id}` | getSupplier |
| `GET` | `/api/asset/v1/locations` | listLocations |
| `GET` | `/api/asset/v1/locations/tree` | getLocationTree |
| `GET` | `/api/asset/v1/locations/{id}` | getLocation |
| `GET` | `/api/asset/v1/consumables` | listConsumables |
| `GET` | `/api/asset/v1/consumables/{id}` | getConsumable |
| `GET` | `/api/asset/v1/consumables/{id}/documents` | listConsumableDocuments |
| `GET` | `/api/asset/v1/consumables/{id}/documents/{doc_id}/download` | downloadConsumableDocument |
| `GET` | `/api/asset/v1/licenses` | listLicenses |
| `GET` | `/api/asset/v1/licenses/{id}` | getLicense |
| `GET` | `/api/asset/v1/licenses/{id}/documents` | listLicenseDocuments |
| `GET` | `/api/asset/v1/licenses/{id}/documents/{doc_id}/download` | downloadLicenseDocument |
| `GET` | `/api/asset/v1/insurance-policies` | listInsurancePolicies |
| `GET` | `/api/asset/v1/insurance-policies/{id}` | getInsurancePolicy |
| `GET` | `/api/asset/v1/insurance-policies/{id}/assets` | listPolicyAssets |
| `GET` | `/api/asset/v1/users` | listUsers |
| `GET` | `/api/asset/v1/stream` | streamEvents |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### asset:assets:manage

Create, update and delete assets.

**UI actions**: `create`, `update`, `delete` on `Asset`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/asset/v1/assets` | createAsset |
| `PUT` | `/api/asset/v1/assets/{id}` | updateAsset |
| `DELETE` | `/api/asset/v1/assets/{id}` | deleteAsset |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### asset:assets:assign

Assign and unassign assets to users.

**UI actions**: `assign` on `Asset`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/asset/v1/assets/{id}/assign` | assignAsset |
| `POST` | `/api/asset/v1/assets/{id}/unassign` | unassignAsset |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### asset:categories:manage

Manage the category tree.

**UI actions**: `manage` on `AssetCategory`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/asset/v1/categories` | createCategory |
| `PUT` | `/api/asset/v1/categories/{id}` | updateCategory |
| `DELETE` | `/api/asset/v1/categories/{id}` | deleteCategory |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### asset:suppliers:manage

Manage suppliers.

**UI actions**: `manage` on `AssetSupplier`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/asset/v1/suppliers` | createSupplier |
| `PUT` | `/api/asset/v1/suppliers/{id}` | updateSupplier |
| `DELETE` | `/api/asset/v1/suppliers/{id}` | deleteSupplier |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### asset:locations:manage

Manage the location tree.

**UI actions**: `manage` on `AssetLocation`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/asset/v1/locations` | createLocation |
| `PUT` | `/api/asset/v1/locations/{id}` | updateLocation |
| `DELETE` | `/api/asset/v1/locations/{id}` | deleteLocation |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### asset:consumables:manage

Manage consumables (stock).

**UI actions**: `manage` on `AssetConsumable`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/asset/v1/consumables` | createConsumable |
| `PUT` | `/api/asset/v1/consumables/{id}` | updateConsumable |
| `DELETE` | `/api/asset/v1/consumables/{id}` | deleteConsumable |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### asset:licenses:manage

Manage software licenses.

**UI actions**: `manage` on `AssetLicense`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/asset/v1/licenses` | createLicense |
| `PUT` | `/api/asset/v1/licenses/{id}` | updateLicense |
| `DELETE` | `/api/asset/v1/licenses/{id}` | deleteLicense |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### asset:insurance:manage

Manage insurance policies and asset coverage.

**UI actions**: `manage` on `AssetInsurance`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/asset/v1/insurance-policies` | createInsurancePolicy |
| `PUT` | `/api/asset/v1/insurance-policies/{id}` | updateInsurancePolicy |
| `DELETE` | `/api/asset/v1/insurance-policies/{id}` | deleteInsurancePolicy |
| `POST` | `/api/asset/v1/insurance-policies/{id}/assets` | addAssetToPolicy |
| `DELETE` | `/api/asset/v1/insurance-policies/{id}/assets/{asset_id}` | removeAssetFromPolicy |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### asset:documents:manage

Upload and delete photos and documents.

**UI actions**: `manage` on `AssetDocument`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/asset/v1/assets/{id}/photo` | uploadAssetPhoto |
| `DELETE` | `/api/asset/v1/assets/{id}/photo` | deleteAssetPhoto |
| `POST` | `/api/asset/v1/assets/{id}/documents` | uploadAssetDocument |
| `DELETE` | `/api/asset/v1/assets/{id}/documents/{doc_id}` | deleteAssetDocument |
| `POST` | `/api/asset/v1/consumables/{id}/documents` | uploadConsumableDocument |
| `DELETE` | `/api/asset/v1/consumables/{id}/documents/{doc_id}` | deleteConsumableDocument |
| `POST` | `/api/asset/v1/licenses/{id}/documents` | uploadLicenseDocument |
| `DELETE` | `/api/asset/v1/licenses/{id}/documents/{doc_id}` | deleteLicenseDocument |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### asset:inventory:sync

Preview and execute inventory synchronisation.

**UI actions**: `sync` on `AssetInventory`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Inventory Sync.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/asset/v1/assets/inventory-sync/preview` | inventorySyncPreview |
| `GET` | `/api/asset/v1/assets/inventory-sync/settings` | getInventorySyncSettings |
| `PUT` | `/api/asset/v1/assets/inventory-sync/settings` | putInventorySyncSettings |
| `POST` | `/api/asset/v1/assets/inventory-sync/execute` | inventorySyncExecute |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### asset:stats:read

Read the asset dashboard statistics.

**UI actions**: `read` on `AssetStats`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Dashboard.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/asset/v1/stats` | getDashboardStats |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### asset:backup:manage

Export and import tenant asset data.

**UI actions**: `manage` on `AssetBackup`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/asset/v1/backup/export` | exportBackup |
| `POST` | `/api/asset/v1/backup/import` | importBackup |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.
<div class="guide-actions"><a href="how-to/asset/docker.html">Install with Docker Compose →</a><a href="how-to/asset/native.html">Install without Docker →</a><a href="downloads/asset.zip">Download Compose bundle ↓</a></div>

## Dependencies and integration

**Required**: TimescaleDB, Valkey, S3-compatible storage, key-encryption key, Auth, Portal, mesh identity.

**Optional or feature-dependent**: Inventory, Paperless, Scheduler.

Configure object storage for photos. Paperless is enabled by default in the documented integration; disable it explicitly if unused. Inventory sync and scheduled sync need reciprocal module policy and consumer grants.

The list describes infrastructure/features, not every transitive library. Check the linked deployment reference for exact versions, enabled features and peer grants. [Framework dependencies](architecture/dependencies.html) cover the shared Go libraries.

## Runtime and operation

| Item | Reference |
| --- | --- |
| Service binary | `assetsvc` |
| Public example configuration | `deploy/dev.yaml`; adapt endpoints and paths for your environment |
| Native source build | Go `1.26.3`, toolchain `go1.26.8`, Node 22 for UI |
| Image repository | `ghcr.io/go-tangra/go-tangra-asset`; choose a published compatible version |
| Private admin default | `127.0.0.1:9830`; check actual configuration |
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
| `Config` | `object_store` | `ObjectStore` |
| `Config` | `inventory` | `Inventory` |
| `Config` | `scheduler` | `Scheduler` |
| `Config` | `task_scheduler` | `TaskScheduler` |
| `Config` | `paperless` | `Paperless` |
| `Config` | `uploads` | `Uploads` |
| `Config` | `events` | `Events` |
| `Config` | `gateway` | `Gateway` |
| `Config` | `mesh_enroll` | `MeshEnroll` |
| `Config` | `limits_asset` | `Limits` |
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
| `ObjectStore` | `endpoint` | `string` |
| `ObjectStore` | `bucket` | `string` |
| `ObjectStore` | `region` | `string` |
| `ObjectStore` | `use_ssl` | `bool` |
| `ObjectStore` | `access_key` | `string` |
| `ObjectStore` | `secret_key` | `string` |
| `ObjectStore` | `presign_ttl_seconds` | `int` |
| `Inventory` | `service` | `string` |
| `Scheduler` | `interval_seconds` | `int` |
| `Scheduler` | `warranty_soon_days` | `int` |
| `Scheduler` | `license_soon_days` | `int` |
| `Scheduler` | `insurance_soon_days` | `int` |
| `Paperless` | `enabled` | `bool` |
| `Paperless` | `service` | `string` |
| `TaskScheduler` | `enabled` | `bool` |
| `TaskScheduler` | `service` | `string` |
| `Uploads` | `max_size_bytes` | `int64` |
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

[Configuration structures and validation](https://github.com/go-tangra/go-tangra-asset/blob/ff6055e17e18f941a945c8cc8d1e1bf2ee44afa7/internal/config/config.go)

## API operation index

These operations are extracted from the module's OpenAPI contract. Read the source contract for request/response schemas, permission checks and exact route bases; internal mesh endpoints must not be treated as anonymous public APIs.

| Method | Contract path | Operation |
| --- | --- | --- |
| `GET` | `/api/asset/v1/assets` | listAssets |
| `POST` | `/api/asset/v1/assets` | createAsset |
| `POST` | `/api/asset/v1/assets/inventory-sync/preview` | inventorySyncPreview |
| `GET` | `/api/asset/v1/assets/inventory-sync/settings` | getInventorySyncSettings |
| `PUT` | `/api/asset/v1/assets/inventory-sync/settings` | putInventorySyncSettings |
| `POST` | `/api/asset/v1/assets/inventory-sync/execute` | inventorySyncExecute |
| `GET` | `/api/asset/v1/assets/{id}` | getAsset |
| `PUT` | `/api/asset/v1/assets/{id}` | updateAsset |
| `DELETE` | `/api/asset/v1/assets/{id}` | deleteAsset |
| `POST` | `/api/asset/v1/assets/{id}/assign` | assignAsset |
| `POST` | `/api/asset/v1/assets/{id}/unassign` | unassignAsset |
| `GET` | `/api/asset/v1/assets/{id}/assignments` | listAssetAssignments |
| `GET` | `/api/asset/v1/assets/{id}/photo` | getAssetPhoto |
| `POST` | `/api/asset/v1/assets/{id}/photo` | uploadAssetPhoto |
| `DELETE` | `/api/asset/v1/assets/{id}/photo` | deleteAssetPhoto |
| `GET` | `/api/asset/v1/documents/search` | searchDocuments |
| `GET` | `/api/asset/v1/assets/{id}/documents` | listAssetDocuments |
| `POST` | `/api/asset/v1/assets/{id}/documents` | uploadAssetDocument |
| `DELETE` | `/api/asset/v1/assets/{id}/documents/{doc_id}` | deleteAssetDocument |
| `GET` | `/api/asset/v1/assets/{id}/documents/{doc_id}/download` | downloadAssetDocument |
| `GET` | `/api/asset/v1/categories` | listCategories |
| `POST` | `/api/asset/v1/categories` | createCategory |
| `GET` | `/api/asset/v1/categories/tree` | getCategoryTree |
| `GET` | `/api/asset/v1/categories/{id}` | getCategory |
| `PUT` | `/api/asset/v1/categories/{id}` | updateCategory |
| `DELETE` | `/api/asset/v1/categories/{id}` | deleteCategory |
| `GET` | `/api/asset/v1/suppliers` | listSuppliers |
| `POST` | `/api/asset/v1/suppliers` | createSupplier |
| `GET` | `/api/asset/v1/suppliers/{id}` | getSupplier |
| `PUT` | `/api/asset/v1/suppliers/{id}` | updateSupplier |
| `DELETE` | `/api/asset/v1/suppliers/{id}` | deleteSupplier |
| `GET` | `/api/asset/v1/locations` | listLocations |
| `POST` | `/api/asset/v1/locations` | createLocation |
| `GET` | `/api/asset/v1/locations/tree` | getLocationTree |
| `GET` | `/api/asset/v1/locations/{id}` | getLocation |
| `PUT` | `/api/asset/v1/locations/{id}` | updateLocation |
| `DELETE` | `/api/asset/v1/locations/{id}` | deleteLocation |
| `GET` | `/api/asset/v1/consumables` | listConsumables |
| `POST` | `/api/asset/v1/consumables` | createConsumable |
| `GET` | `/api/asset/v1/consumables/{id}` | getConsumable |
| `PUT` | `/api/asset/v1/consumables/{id}` | updateConsumable |
| `DELETE` | `/api/asset/v1/consumables/{id}` | deleteConsumable |
| `GET` | `/api/asset/v1/consumables/{id}/documents` | listConsumableDocuments |
| `POST` | `/api/asset/v1/consumables/{id}/documents` | uploadConsumableDocument |
| `DELETE` | `/api/asset/v1/consumables/{id}/documents/{doc_id}` | deleteConsumableDocument |
| `GET` | `/api/asset/v1/consumables/{id}/documents/{doc_id}/download` | downloadConsumableDocument |
| `GET` | `/api/asset/v1/licenses` | listLicenses |
| `POST` | `/api/asset/v1/licenses` | createLicense |
| `GET` | `/api/asset/v1/licenses/{id}` | getLicense |
| `PUT` | `/api/asset/v1/licenses/{id}` | updateLicense |
| `DELETE` | `/api/asset/v1/licenses/{id}` | deleteLicense |
| `GET` | `/api/asset/v1/licenses/{id}/documents` | listLicenseDocuments |
| `POST` | `/api/asset/v1/licenses/{id}/documents` | uploadLicenseDocument |
| `DELETE` | `/api/asset/v1/licenses/{id}/documents/{doc_id}` | deleteLicenseDocument |
| `GET` | `/api/asset/v1/licenses/{id}/documents/{doc_id}/download` | downloadLicenseDocument |
| `GET` | `/api/asset/v1/insurance-policies` | listInsurancePolicies |
| `POST` | `/api/asset/v1/insurance-policies` | createInsurancePolicy |
| `GET` | `/api/asset/v1/insurance-policies/{id}` | getInsurancePolicy |
| `PUT` | `/api/asset/v1/insurance-policies/{id}` | updateInsurancePolicy |
| `DELETE` | `/api/asset/v1/insurance-policies/{id}` | deleteInsurancePolicy |
| `GET` | `/api/asset/v1/insurance-policies/{id}/assets` | listPolicyAssets |
| `POST` | `/api/asset/v1/insurance-policies/{id}/assets` | addAssetToPolicy |
| `DELETE` | `/api/asset/v1/insurance-policies/{id}/assets/{asset_id}` | removeAssetFromPolicy |
| `GET` | `/api/asset/v1/users` | listUsers |
| `GET` | `/api/asset/v1/health` | health |
| `GET` | `/api/asset/v1/stats` | getDashboardStats |
| `POST` | `/api/asset/v1/backup/export` | exportBackup |
| `POST` | `/api/asset/v1/backup/import` | importBackup |
| `GET` | `/api/asset/v1/stream` | streamEvents |

[OpenAPI: api/openapi/asset.yaml](https://github.com/go-tangra/go-tangra-asset/blob/ff6055e17e18f941a945c8cc8d1e1bf2ee44afa7/api/openapi/asset.yaml)

## Detailed source references

- [README.md](sources/asset/README.html) — captured at `ff6055e17e18`.
- [deploy/README.md](sources/asset/deploy/README.html) — captured at `ff6055e17e18`.

## Limits, diagnostics and recovery

Configure object storage for photos. Paperless is enabled by default in the documented integration; disable it explicitly if unused. Inventory sync and scheduled sync need reciprocal module policy and consumer grants.

Use the module's operations/deployment reference for retention, backup/restore, refusal behavior, interface examples and feature limitations. The installation guides cover common readiness, identity, registration and storage failures.

## Upstream overview: go-tangra-asset

Tenant IT asset management (ITAM) service for the
[go-tangra v4 platform](https://github.com/go-tangra/go-tangra).

It tracks **assets** with an assign/unassign lifecycle to platform users,
**photos and documents** (metadata in TimescaleDB, bytes in S3-compatible object
storage such as RustFS or MinIO), **categories** and **locations** (trees),
**suppliers**, **consumables** (stock), **licenses**, **insurance policies** with
per-asset coverage, and server-side **depreciation** (double-declining balance).
A lifecycle scheduler raises warranty, license, insurance and low-stock events on
the platform event bus. **Inventory sync** diffs the hosts reported by the
inventory service against the assets and creates or updates them. Supplier and
location contact data is sealed at rest (AES-256-GCM envelope) and returned in
clear only to tenant admins.

Operations: [`deploy/README.md`](sources/asset/deploy/README.html).
Design history: `specs/012-asset-service`.

## Place in the platform

```
go-tangra/go-tangra          platform module + @go-tangra/ui kit
        |
go-tangra-auth  <---->  go-tangra-portal (gateway)  <---->  go-tangra-lcm
                                  |
                          go-tangra-asset  ---->  object storage (S3)
                                  |
                                  +---- mTLS ---->  go-tangra-inventory (host list)
```

- Built on `github.com/go-tangra/go-tangra/v4` (mTLS transports, identity,
  service policy, audit, observability).
- Verifies platform tokens, resolves people and checks permissions through the
  auth SDK (`github.com/go-tangra/go-tangra-auth/sdk/v4`).
- Registers with the gateway through the portal SDK
  (`github.com/go-tangra/go-tangra-portal/sdk/v4`), which fronts the browser API
  (`/api/asset`) and the federated UI remote.
- Enrolls for its SVID with lcm over the network
  (`github.com/go-tangra/go-tangra-lcm/sdk/v4`), as the platform stack does.
- Reads hosts from inventory over the SPIFFE mTLS mesh through the inventory SDK
  (`github.com/go-tangra/go-tangra-inventory/sdk/v4`). The inventory policy must
  allow `svc/asset` on `InventoryHostService/ListHosts`.

The repository holds one Go module, `github.com/go-tangra/go-tangra-asset/v4`.
Other services call it through `pkg/assetclient` and the `asset.v1` protos
(not proxied by the gateway).

## Layout

| Path | What |
|------|------|
| `api/openapi/asset.yaml` | browser API contract (served under `/api/asset`) |
| `api/proto/asset/v1/` | asset gRPC services |
| `internal/config` | configuration + validation (secure defaults, named opt-outs) |
| `internal/store`, `internal/repo` | TimescaleDB schema (RLS), repositories; `internal/memstore` is the in-memory test double |
| `internal/blob` | S3-compatible object storage (minio-go), presigned downloads |
| `internal/sealed` | envelope encryption of contact PII (KEK -> DEK) |
| `internal/authz` | per-route permission checks |
| `internal/assets`, `internal/categories`, `internal/locations`, `internal/suppliers` | assets and their reference data |
| `internal/consumables`, `internal/licenses`, `internal/insurance`, `internal/documents` | stock, licenses, insurance coverage, documents |
| `internal/deprec` | pure depreciation library |
| `internal/invclient`, `internal/invsync` | inventory client adapter and the sync preview/execute |
| `internal/scheduler`, `internal/events`, `internal/stream` | lifecycle sweeps, events on the platform bus, live stream |
| `internal/backup`, `internal/stats`, `internal/audit`, `internal/userdir` | backup export/import, statistics, audit, user lookups |
| `internal/httpapi`, `internal/grpcapi` | browser and service APIs |
| `internal/app`, `cmd/assetsvc` | wiring and the service binary (serve, `bootstrap`, `version`) |
| `pkg/assetmanifest` | gateway manifest, module roles and built-in role grants |
| `pkg/assetclient` | Go client other services use |
| `deploy` | service policy and operations notes |
| `ui/` | Vue 3 + FlyonUI federated remote on `@go-tangra/ui` |

## Build and test

You need Go 1.26, Node 22, Docker (for the integration suite and the image), and a
GitHub token with `read:packages` to install `@go-tangra/ui` from GitHub Packages.

```bash
go build ./... && go vet ./... && go test -race ./...
buf lint
make test-integration                     # -tags integration, TimescaleDB + Valkey via testcontainers (needs Docker)
make lint cover vuln

cd ui
export NODE_AUTH_TOKEN=$(gh auth token)   # ui/.npmrc only references this variable
npm ci && npm run lint && npm run test:unit && npm run build
```

The unit coverage gate requires at least 80 % overall and 100 % for the
authorization, sealing and depreciation packages. Generated code, SQL bindings and
wiring are covered by the integration suite instead. The Playwright specs in
`ui/tests/e2e` need a running platform and operator credentials; they skip
otherwise.

## Run

The service runs in the go-tangra platform stack (`deploy/stack` in
[go-tangra](https://github.com/go-tangra/go-tangra)), next to TimescaleDB, Valkey,
RustFS and the inventory service. The stack mounts its configuration at
`/app/deploy/container.yaml` and the development key-encryption key at
`/app/deploy/kek.dev`. `deploy/kek.dev` in this repository is a development key
only; it is excluded from the image.

```bash
assetsvc bootstrap -config deploy/container.yaml    # apply migrations and exit
assetsvc -config deploy/container.yaml              # serve (applies migrations)
```

See `specs/012-asset-service/quickstart.md` for the end-to-end walkthrough.

## Container image

The image is `ghcr.io/go-tangra/go-tangra-asset`, built by
`.github/workflows/ci.yaml`. It carries `assetsvc` with the embedded UI remote.

```bash
docker buildx build --secret id=npm_token,env=NODE_AUTH_TOKEN \
  --build-arg APP_VERSION=4.0.0 -t go-tangra-asset:dev .
docker run --rm go-tangra-asset:dev version
```

The image runs `assetsvc -config deploy/container.yaml` as user `app`
(uid 10001). It contains no configuration and no key material: deployments mount
their own `deploy/container.yaml` and key-encryption key. The object store and
inventory are separate services the configuration points at
(`object_store.endpoint`, `discovery.static.inventory`); the bucket is created on
start when missing.

## API permissions

`assets:read/manage/assign`, `categories:manage`, `suppliers:manage`,
`locations:manage`, `consumables:manage`, `licenses:manage`, `insurance:manage`,
`documents:manage`, `inventory:sync`, `stats:read`, `backup:manage`. The gateway
enforces the per-route permission from the manifest; the module checks it again.

The module registers its permissions, its module roles and the built-in role
grants (`pkg/assetmanifest.Grants`, scoped to asset by auth) with auth at start
and every five minutes (`pkg/assetmanifest.Registration`). Module roles are
provided in every tenant; administrators assign them or clone them into custom
roles:

| Role | Display name | Permissions |
|---|---|---|
| `administrator` | Assets administrator | all asset permissions |
| `editor` | Assets editor | `assets:read`, `assets:manage`, `assets:assign`, `stats:read` |
| `viewer` | Assets viewer | `assets:read`, `stats:read` |

## Versioning

- Releases are tagged `vX.Y.Z`. CI publishes the image as `X.Y.Z`, `X.Y`, `X`
  and `sha-<short>`. There is no `latest` tag.
- v4.0.0 rebuilds the service on the go-tangra v4 platform. The v3 line stays on
  the `v3` branch and its `v3.x` tags.
