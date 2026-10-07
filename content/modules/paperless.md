# Paperless

Documents, object storage, text extraction, full-text search and sharing.

**Architecture role**: Business modules. [See the complete component map](architecture/index.html).

**Documented source**: `aaed98b1fe39` · nearest local service tag `v4.4.3` · v4 major. [Repository at this revision](https://github.com/go-tangra/go-tangra-paperless/tree/aaed98b1fe399cf0019014e8edf4ac3cde4a1ae0). Tags are source metadata, not a claim of image publication or cross-module compatibility.


## Permissions and authorization

This catalogue contains **9 permissions** declared by the [module manifest](https://github.com/go-tangra/go-tangra-paperless/blob/aaed98b1fe399cf0019014e8edf4ac3cde4a1ae0/pkg/paperlessmanifest/manifest.go) at the revision above. Custom-role references use `module:resource:action`; the manifest and API contract use the local `resource:action` form. The action names are distinct grants: do not assume `manage` automatically includes `read` or another action.

The module additionally checks Zanzibar grants on each document or category. API roles alone do not give access to every document. Sharing viewer/sharer access requires share access; granting/revoking editor or owner requires owner control. A revoke affects grants on the named resource.

[How to assign and verify permissions](architecture/security.html#assign-and-verify-permissions). Module roles and built-in grant mappings are defined in the linked manifest; review those mappings before assigning a broad role.

| Qualified permission | What it allows |
| --- | --- |
| `paperless:documents:read` | List, read and download documents |
| `paperless:documents:write` | Upload, update and move documents |
| `paperless:documents:delete` | Delete documents |
| `paperless:categories:read` | Browse the category tree |
| `paperless:categories:manage` | Create, change, move and delete categories |
| `paperless:permissions:manage` | Grant and revoke access to documents and categories |
| `paperless:search:read` | Full-text search documents |
| `paperless:stats:read` | Read document statistics |
| `paperless:backup:manage` | Export and import tenant documents and permissions |

### paperless:documents:read

List, read and download documents.

**UI actions**: `read`, `create`, `update`, `delete` on `PaperlessDocument`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Documents.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/paperless/v1/documents` | listDocuments |
| `GET` | `/api/paperless/v1/documents/{id}` | getDocument |
| `GET` | `/api/paperless/v1/documents/{id}/download` | downloadDocument |
| `GET` | `/api/paperless/v1/documents/{id}/download-url` | getDownloadUrl |
| `POST` | `/api/paperless/v1/permissions/check` | checkAccess |
| `GET` | `/api/paperless/v1/permissions/effective` | getEffectivePermissions |
| `GET` | `/api/paperless/v1/stream` | streamEvents |

**Scope and additional checks**: The module additionally checks Zanzibar grants on each document or category. API roles alone do not give access to every document. Sharing viewer/sharer access requires share access; granting/revoking editor or owner requires owner control. A revoke affects grants on the named resource.

### paperless:documents:write

Upload, update and move documents.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/paperless/v1/documents` | uploadDocument |
| `PUT` | `/api/paperless/v1/documents/{id}` | updateDocument |
| `POST` | `/api/paperless/v1/documents/{id}/move` | moveDocument |

**Scope and additional checks**: The module additionally checks Zanzibar grants on each document or category. API roles alone do not give access to every document. Sharing viewer/sharer access requires share access; granting/revoking editor or owner requires owner control. A revoke affects grants on the named resource.

### paperless:documents:delete

Delete documents.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/paperless/v1/documents/{id}/remove` | deleteDocument |
| `POST` | `/api/paperless/v1/documents/batch-delete` | batchDeleteDocuments |

**Scope and additional checks**: The module additionally checks Zanzibar grants on each document or category. API roles alone do not give access to every document. Sharing viewer/sharer access requires share access; granting/revoking editor or owner requires owner control. A revoke affects grants on the named resource.

### paperless:categories:read

Browse the category tree.

**UI actions**: `read`, `create`, `update`, `delete` on `PaperlessCategory`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Categories.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/paperless/v1/categories` | listCategories |
| `GET` | `/api/paperless/v1/categories/tree` | getCategoryTree |
| `GET` | `/api/paperless/v1/categories/{id}` | getCategory |

**Scope and additional checks**: The module additionally checks Zanzibar grants on each document or category. API roles alone do not give access to every document. Sharing viewer/sharer access requires share access; granting/revoking editor or owner requires owner control. A revoke affects grants on the named resource.

### paperless:categories:manage

Create, change, move and delete categories.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/paperless/v1/categories` | createCategory |
| `PUT` | `/api/paperless/v1/categories/{id}` | updateCategory |
| `POST` | `/api/paperless/v1/categories/{id}/remove` | deleteCategory |
| `POST` | `/api/paperless/v1/categories/{id}/move` | moveCategory |

**Scope and additional checks**: The module additionally checks Zanzibar grants on each document or category. API roles alone do not give access to every document. Sharing viewer/sharer access requires share access; granting/revoking editor or owner requires owner control. A revoke affects grants on the named resource.

### paperless:permissions:manage

Grant and revoke access to documents and categories.

**UI actions**: `manage` on `PaperlessPermission`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/paperless/v1/permissions/grant` | grantAccess |
| `POST` | `/api/paperless/v1/permissions/revoke` | revokeAccess |
| `GET` | `/api/paperless/v1/permissions` | listPermissions |

**Scope and additional checks**: The module additionally checks Zanzibar grants on each document or category. API roles alone do not give access to every document. Sharing viewer/sharer access requires share access; granting/revoking editor or owner requires owner control. A revoke affects grants on the named resource.

### paperless:search:read

Full-text search documents.

**UI actions**: `read` on `PaperlessSearch`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Search.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/paperless/v1/documents/search` | searchDocuments |

**Scope and additional checks**: The module additionally checks Zanzibar grants on each document or category. API roles alone do not give access to every document. Sharing viewer/sharer access requires share access; granting/revoking editor or owner requires owner control. A revoke affects grants on the named resource.

### paperless:stats:read

Read document statistics.

**UI actions**: `read` on `PaperlessStats`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Dashboard.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/paperless/v1/statistics` | getStatistics |
| `GET` | `/api/paperless/v1/statistics/tenant` | getTenantStatistics |

**Scope and additional checks**: The module additionally checks Zanzibar grants on each document or category. API roles alone do not give access to every document. Sharing viewer/sharer access requires share access; granting/revoking editor or owner requires owner control. A revoke affects grants on the named resource.

### paperless:backup:manage

Export and import tenant documents and permissions.

**UI actions**: `manage` on `PaperlessBackup`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/paperless/v1/backup/export` | exportBackup |
| `POST` | `/api/paperless/v1/backup/import` | importBackup |

**Scope and additional checks**: The module additionally checks Zanzibar grants on each document or category. API roles alone do not give access to every document. Sharing viewer/sharer access requires share access; granting/revoking editor or owner requires owner control. A revoke affects grants on the named resource.
<div class="guide-actions"><a href="how-to/paperless/docker.html">Install with Docker Compose →</a><a href="how-to/paperless/native.html">Install without Docker →</a><a href="downloads/paperless.zip">Download Compose bundle ↓</a></div>

## Dependencies and integration

**Required**: TimescaleDB, Valkey, S3-compatible storage, Auth, Portal, mesh identity.

**Optional or feature-dependent**: OpenFGA sharing, Tika, Gotenberg.

Configure S3-compatible object storage and extraction providers. Database exports do not include every blob. Review sharing/OpenFGA configuration and extractor connectivity before validating document search.

The list describes infrastructure/features, not every transitive library. Check the linked deployment reference for exact versions, enabled features and peer grants. [Framework dependencies](architecture/dependencies.html) cover the shared Go libraries.

## Runtime and operation

| Item | Reference |
| --- | --- |
| Service binary | `paperlesssvc` |
| Public example configuration | `deploy/dev.yaml`; adapt endpoints and paths for your environment |
| Native source build | Go `1.26.3`, toolchain `go1.26.8`, Node 22 for UI |
| Image repository | `ghcr.io/go-tangra/go-tangra-paperless`; choose a published compatible version |
| Private admin default | `127.0.0.1:9790`; check actual configuration |
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
| `Config` | `extract` | `Extract` |
| `Config` | `uploads` | `Uploads` |
| `Config` | `jobs` | `Jobs` |
| `Config` | `events` | `Events` |
| `Config` | `gateway` | `Gateway` |
| `Config` | `enroll` | `Enroll` |
| `Config` | `limits_paperless` | `Limits` |
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
| `Extract` | `tika_url` | `string` |
| `Extract` | `gotenberg_url` | `string` |
| `Extract` | `timeout_seconds` | `int` |
| `Extract` | `max_bytes` | `int64` |
| `Uploads` | `max_size_bytes` | `int64` |
| `Uploads` | `allowed_mime` | `[]string` |
| `Jobs` | `workers` | `int` |
| `Jobs` | `interval_seconds` | `int` |
| `Jobs` | `lease_seconds` | `int` |
| `Jobs` | `max_retries` | `int` |
| `Jobs` | `retry_delay_seconds` | `int` |
| `Jobs` | `backoff_multiplier` | `float64` |
| `Jobs` | `job_timeout_seconds` | `int` |
| `Jobs` | `cleanup_days` | `int` |
| `Events` | `enabled` | `bool` |
| `Gateway` | `service` | `string` |
| `Gateway` | `issuer` | `string` |
| `Enroll` | `enabled` | `bool` |
| `Enroll` | `enroll_url` | `string` |
| `Enroll` | `lcm_grpc` | `string` |
| `Enroll` | `tenant_id` | `string` |
| `Enroll` | `token_file` | `string` |
| `Enroll` | `state_file` | `string` |
| `Enroll` | `insecure` | `bool` |
| `Limits` | `backup_max_bytes` | `int64` |
| `Limits` | `search_max_len` | `int` |

[Configuration structures and validation](https://github.com/go-tangra/go-tangra-paperless/blob/aaed98b1fe399cf0019014e8edf4ac3cde4a1ae0/internal/config/config.go)

## API operation index

These operations are extracted from the module's OpenAPI contract. Read the source contract for request/response schemas, permission checks and exact route bases; internal mesh endpoints must not be treated as anonymous public APIs.

| Method | Contract path | Operation |
| --- | --- | --- |
| `POST` | `/api/paperless/v1/documents` | uploadDocument |
| `GET` | `/api/paperless/v1/documents` | listDocuments |
| `GET` | `/api/paperless/v1/documents/{id}` | getDocument |
| `PUT` | `/api/paperless/v1/documents/{id}` | updateDocument |
| `POST` | `/api/paperless/v1/documents/{id}/remove` | deleteDocument |
| `POST` | `/api/paperless/v1/documents/{id}/move` | moveDocument |
| `GET` | `/api/paperless/v1/documents/{id}/download` | downloadDocument |
| `GET` | `/api/paperless/v1/documents/{id}/download-url` | getDownloadUrl |
| `POST` | `/api/paperless/v1/documents/search` | searchDocuments |
| `POST` | `/api/paperless/v1/documents/batch-delete` | batchDeleteDocuments |
| `POST` | `/api/paperless/v1/categories` | createCategory |
| `GET` | `/api/paperless/v1/categories` | listCategories |
| `GET` | `/api/paperless/v1/categories/tree` | getCategoryTree |
| `GET` | `/api/paperless/v1/categories/{id}` | getCategory |
| `PUT` | `/api/paperless/v1/categories/{id}` | updateCategory |
| `POST` | `/api/paperless/v1/categories/{id}/remove` | deleteCategory |
| `POST` | `/api/paperless/v1/categories/{id}/move` | moveCategory |
| `POST` | `/api/paperless/v1/permissions/grant` | grantAccess |
| `POST` | `/api/paperless/v1/permissions/revoke` | revokeAccess |
| `GET` | `/api/paperless/v1/permissions` | listPermissions |
| `POST` | `/api/paperless/v1/permissions/check` | checkAccess |
| `GET` | `/api/paperless/v1/permissions/effective` | getEffectivePermissions |
| `GET` | `/api/paperless/v1/statistics` | getStatistics |
| `GET` | `/api/paperless/v1/statistics/tenant` | getTenantStatistics |
| `POST` | `/api/paperless/v1/backup/export` | exportBackup |
| `POST` | `/api/paperless/v1/backup/import` | importBackup |
| `GET` | `/api/paperless/v1/stream` | streamEvents |

[OpenAPI: api/openapi/paperless.yaml](https://github.com/go-tangra/go-tangra-paperless/blob/aaed98b1fe399cf0019014e8edf4ac3cde4a1ae0/api/openapi/paperless.yaml)

## Detailed source references

- [README.md](sources/paperless/README.html) — captured at `aaed98b1fe39`.
- [deploy/README.md](sources/paperless/deploy/README.html) — captured at `aaed98b1fe39`.

## Limits, diagnostics and recovery

Configure S3-compatible object storage and extraction providers. Database exports do not include every blob. Review sharing/OpenFGA configuration and extractor connectivity before validating document search.

Use the module's operations/deployment reference for retention, backup/restore, refusal behavior, interface examples and feature limitations. The installation guides cover common readiness, identity, registration and storage failures.

## Upstream overview: go-tangra-paperless

Tenant document management service for the
[go-tangra v4 platform](https://github.com/go-tangra/go-tangra).

It stores **documents** (metadata in TimescaleDB, bytes in S3-compatible object
storage such as RustFS or MinIO), organises them into a **category hierarchy**,
extracts their text asynchronously through **Apache Tika** (optionally converting
with **Gotenberg**), and makes them **full-text searchable**. Access is
Zanzibar-style (owner / editor / viewer / sharer, to users, roles or the tenant,
with expiry), inherited down the category tree. Object-store credentials are
sealed at rest (AES-256-GCM envelope) and never returned; extracted content
never reaches logs or the audit trail. Processing progress is published live on
the platform event bus, so the UI updates without polling.

Operations: [`deploy/README.md`](sources/paperless/deploy/README.html).
Design history: `specs/009-paperless-service`.

## Place in the platform

```
go-tangra/go-tangra          platform module + @go-tangra/ui kit
        |
go-tangra-auth  <---->  go-tangra-portal (gateway)  <---->  go-tangra-lcm
                                  |
                        go-tangra-paperless  ---->  object storage (S3), Tika, Gotenberg
```

- Built on `github.com/go-tangra/go-tangra/v4` (mTLS transports, identity,
  service policy, audit, observability).
- Verifies platform tokens, resolves people and checks permissions through the
  auth SDK (`github.com/go-tangra/go-tangra-auth/sdk/v4`).
- Registers with the gateway through the portal SDK
  (`github.com/go-tangra/go-tangra-portal/sdk/v4`), which fronts the browser API
  (`/api/paperless`) and the federated UI remote.
- Enrolls for its SVID with lcm over the network
  (`github.com/go-tangra/go-tangra-lcm/sdk/v4`), as the platform stack does.

The repository holds two Go modules: the service,
`github.com/go-tangra/go-tangra-paperless/v4`, and the client SDK in `sdk/`,
`github.com/go-tangra/go-tangra-paperless/sdk/v4` (the `paperless.v1` protos and
`pkg/paperlessclient`). Other services call paperless over the mesh through the
SDK (not proxied by the gateway); the service requires the SDK through a
`replace ... => ./sdk`, and the SDK is released by hand with `sdk/vX.Y.Z` tags.

### Client SDK

```go
import "github.com/go-tangra/go-tangra-paperless/sdk/v4/pkg/paperlessclient"

conn, _ := app.Client(ctx, "paperless")                 // SPIFFE mTLS
pc := paperlessclient.New(conn)
catID, _ := pc.EnsureCategory(ctx, tenantID, []string{"Assets", "AT-000123"})
doc, _ := pc.CreateDocument(ctx, tenantID, paperlessclient.CreateInput{
    CategoryID: catID, Name: "Warranty", FileName: "w.pdf", MimeType: "application/pdf", Content: b})
hits, _ := pc.Search(ctx, tenantID, "warranty", 20)
data, name, mime, _ := pc.DownloadDocument(ctx, tenantID, doc.ID)
_ = pc.DeleteDocument(ctx, tenantID, doc.ID, true)
```

Every method takes the tenant explicitly and returns plain Go types; gRPC
`NotFound` / `PermissionDenied` / `Unavailable` map to `ErrNotFound` /
`ErrForbidden` / `ErrUnavailable`. `EnsureCategory` is idempotent and safe for
concurrent callers. A calling service is identified by its SPIFFE id: it becomes
owner of the folders and documents it creates, finds them with `Search`, and may
create root folders and read the folder tree; it gets no collection access to
documents (tenant admins see everything). Each call carries 33 MiB message-size
bounds (`WithMaxMessageBytes` overrides), matching the server default. The caller
must also be allowed by `deploy/policy.yaml` (e.g. the `asset-documents` rule).

## Layout

| Path | What |
|------|------|
| `api/openapi/paperless.yaml` | browser API contract (served under `/api/paperless`) |
| `sdk/api/proto/paperless/v1/` | document, category, permission and statistics gRPC services (SDK module) |
| `internal/config` | configuration + validation (secure defaults, named opt-outs) |
| `internal/store`, `internal/repo` | TimescaleDB schema (RLS), repositories; `internal/memstore` is the in-memory test double |
| `internal/blob` | S3-compatible object storage (minio-go), presigned downloads |
| `internal/extract` | Tika text extraction and Gotenberg conversion clients |
| `internal/jobs` | distributed extraction worker pool (single-winner lease, retry with backoff) |
| `internal/sealed` | envelope encryption of object-store credentials (KEK -> DEK) |
| `internal/authz`, `internal/permissions` | Zanzibar grants and category-tree inheritance |
| `internal/documents`, `internal/categories`, `internal/search` | documents, folders, full-text search |
| `internal/events`, `internal/stream` | processing events on the platform bus, live stream |
| `internal/backup`, `internal/stats`, `internal/audit` | backup export/import, statistics, audit |
| `internal/httpapi`, `internal/grpcapi` | browser and service APIs |
| `internal/app`, `cmd/paperlesssvc` | wiring and the service binary (serve, `bootstrap`, `version`) |
| `pkg/paperlessmanifest` | gateway manifest, module roles and built-in role grants |
| `sdk/pkg/paperlessclient` | typed Go client other services use (SDK module) |
| `deploy` | service policy and operations notes |
| `ui/` | Vue 3 + FlyonUI federated remote on `@go-tangra/ui` |

## Build and test

You need Go 1.26, Node 22, Docker (for the integration suite and the image), and a
GitHub token with `read:packages` to install `@go-tangra/ui` from GitHub Packages.

```bash
go build ./... && go vet ./... && go test -race ./...
(cd sdk && go vet ./... && go test -race ./... && buf lint)   # client SDK module
make test-integration                     # -tags integration, TimescaleDB via testcontainers (needs Docker)
make lint cover vuln

cd ui
export NODE_AUTH_TOKEN=$(gh auth token)   # ui/.npmrc only references this variable
npm ci && npm run lint && npm run test:unit && npm run build
```

The unit coverage gate requires at least 80 % overall and 100 % for the
authorization and sealing packages. Generated code, SQL bindings and wiring are
covered by the integration suite instead. The Playwright specs in `ui/tests/e2e`
need a running platform and operator credentials; they skip otherwise.

## Run

The service runs in the go-tangra platform stack (`deploy/stack` in
[go-tangra](https://github.com/go-tangra/go-tangra)), next to TimescaleDB, Valkey,
RustFS, Tika and Gotenberg. The stack mounts its configuration at
`/app/deploy/container.yaml` and the development key-encryption key at
`/app/deploy/kek.dev`. `deploy/kek.dev` in this repository is a development key
only; it is excluded from the image.

```bash
paperlesssvc bootstrap -config deploy/container.yaml    # apply migrations and exit
paperlesssvc -config deploy/container.yaml              # serve (applies migrations)
```

See `specs/009-paperless-service/quickstart.md` for the end-to-end walkthrough.

## Container image

The image is `ghcr.io/go-tangra/go-tangra-paperless`, built by
`.github/workflows/ci.yaml`. It carries `paperlesssvc` with the embedded UI remote.

```bash
docker buildx build --secret id=npm_token,env=NODE_AUTH_TOKEN \
  --build-arg APP_VERSION=4.0.0 -t go-tangra-paperless:dev .
docker run --rm go-tangra-paperless:dev version
```

The image runs `paperlesssvc -config deploy/container.yaml` as user `app`
(uid 10001). It contains no configuration and no key material: deployments mount
their own `deploy/container.yaml` and key-encryption key. Tika, Gotenberg and the
object store are separate services the configuration points at
(`extract.tika_url`, `extract.gotenberg_url`, `object_store.endpoint`); the
bucket is created on start when missing.

## API permissions

`documents:read/write/delete`, `categories:read/manage`, `search:read`,
`permissions:manage`, `backup:manage`, `stats:read`. The gateway enforces the
per-route permission from the manifest; the module then enforces the Zanzibar
grant on the document or category.

Sharing: holders of `permissions:manage` get a **Share access** button on a
document (document drawer) and on a category (selected-category card), which
opens the kit permission drawer (users, roles or everyone in the tenant, with
optional expiry). Grants on a category apply to everything inside it. Viewer and
sharer grants need share access to the resource; granting or revoking editor or
owner needs full (owner) control, so a sharer cannot promote anyone or remove an
owner. A revoke only reaches grants on the resource it names.

The module registers its permissions, its module roles and the built-in role
grants (`pkg/paperlessmanifest.Grants`, scoped to paperless by auth) with auth
at start and every five minutes (`pkg/paperlessmanifest.Registration`). Module
roles are provided in every tenant; administrators assign them or clone them
into custom roles:

| Role | Display name | Permissions |
|---|---|---|
| `administrator` | Paperless administrator | all paperless permissions |
| `editor` | Paperless editor | `documents:read`, `documents:write`, `categories:read`, `search:read` |
| `viewer` | Paperless viewer | `documents:read`, `categories:read`, `search:read` |

A module role grants the API permission only; access to an individual
document or category still needs its Zanzibar grant.

## Versioning

- Releases are tagged `vX.Y.Z`. CI publishes the image as `X.Y.Z`, `X.Y`, `X`
  and `sha-<short>`. There is no `latest` tag.
- v4.0.0 rebuilds the service on the go-tangra v4 platform. The v3 line stays on
  the `v3` branch and its `v3.x` tags.
