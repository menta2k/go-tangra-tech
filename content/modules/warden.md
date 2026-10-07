# Warden

Vault-backed secrets management and controlled credential sharing.

**Architecture role**: Control plane. [See the complete component map](architecture/index.html).

**Documented source**: `d7f797813b78` · nearest local service tag `v4.5.3` · v4 major. [Repository at this revision](https://github.com/go-tangra/go-tangra-warden/tree/d7f797813b781cb22f41f2b2a2b75c270e0e660f). Tags are source metadata, not a claim of image publication or cross-module compatibility.


## Permissions and authorization

This catalogue contains **10 permissions** declared by the [module manifest](https://github.com/go-tangra/go-tangra-warden/blob/d7f797813b781cb22f41f2b2a2b75c270e0e660f/pkg/wardenmanifest/manifest.go) at the revision above. Custom-role references use `module:resource:action`; the manifest and API contract use the local `resource:action` form. The action names are distinct grants: do not assume `manage` automatically includes `read` or another action.

API permissions are combined with resource grants on secrets and folders. Owner/editor/viewer/sharer relationships, expiry and folder inheritance constrain which secrets a caller can reach. Revealing passwords is sensitive even when the permission is named read.

[How to assign and verify permissions](architecture/security.html#assign-and-verify-permissions). Module roles and built-in grant mappings are defined in the linked manifest; review those mappings before assigning a broad role.

| Qualified permission | What it allows |
| --- | --- |
| `warden:secrets:read` | Read secrets and reveal passwords the caller is granted |
| `warden:secrets:write` | Create and change secrets the caller is granted |
| `warden:secrets:delete` | Delete secrets the caller owns |
| `warden:secrets:share` | Create external shares of secrets the caller may share |
| `warden:folders:manage` | Create, move and delete folders the caller is granted |
| `warden:permissions:manage` | Grant and revoke access on resources the caller may share |
| `warden:transfer:import` | Import Bitwarden exports |
| `warden:transfer:export` | Export secrets to Bitwarden format (bulk disclosure) |
| `warden:backup:manage` | Export and import tenant backups (bulk disclosure with material) |
| `warden:stats:read` | Read statistics and the audit trail |

### warden:secrets:read

Read secrets and reveal passwords the caller is granted.

**UI actions**: `read`, `create`, `update`, `delete`, `share` on `Secret`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Secrets, Generator.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/warden/v1/secrets` | listSecrets |
| `GET` | `/api/warden/v1/secrets/search` | searchSecrets |
| `GET` | `/api/warden/v1/secrets/{id}` | getSecret |
| `GET` | `/api/warden/v1/secrets/{id}/password` | revealPassword |
| `GET` | `/api/warden/v1/secrets/{id}/versions` | listVersions |
| `GET` | `/api/warden/v1/secrets/{id}/totp` | totpCode |
| `GET` | `/api/warden/v1/access/check` | checkAccess |
| `GET` | `/api/warden/v1/access/effective` | effectivePermissions |
| `GET` | `/api/warden/v1/access/resources` | accessibleResources |
| `POST` | `/api/warden/v1/generate` | generatePassword |

**Scope and additional checks**: API permissions are combined with resource grants on secrets and folders. Owner/editor/viewer/sharer relationships, expiry and folder inheritance constrain which secrets a caller can reach. Revealing passwords is sensitive even when the permission is named read.

### warden:secrets:write

Create and change secrets the caller is granted.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/warden/v1/secrets` | createSecret |
| `PUT` | `/api/warden/v1/secrets/{id}` | updateSecret |
| `POST` | `/api/warden/v1/secrets/{id}/move` | moveSecret |
| `PUT` | `/api/warden/v1/secrets/{id}/password` | updatePassword |
| `POST` | `/api/warden/v1/secrets/{id}/versions/{version}/restore` | restoreVersion |
| `PUT` | `/api/warden/v1/secrets/{id}/totp` | setTotp |
| `DELETE` | `/api/warden/v1/secrets/{id}/totp` | removeTotp |

**Scope and additional checks**: API permissions are combined with resource grants on secrets and folders. Owner/editor/viewer/sharer relationships, expiry and folder inheritance constrain which secrets a caller can reach. Revealing passwords is sensitive even when the permission is named read.

### warden:secrets:delete

Delete secrets the caller owns.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/warden/v1/secrets/{id}/remove` | deleteSecret |

**Scope and additional checks**: API permissions are combined with resource grants on secrets and folders. Owner/editor/viewer/sharer relationships, expiry and folder inheritance constrain which secrets a caller can reach. Revealing passwords is sensitive even when the permission is named read.

### warden:secrets:share

Create external shares of secrets the caller may share.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/warden/v1/secrets/{id}/shares` | listShares |
| `POST` | `/api/warden/v1/secrets/{id}/shares` | createShare |
| `POST` | `/api/warden/v1/shares/{id}/cancel` | cancelShare |

**Scope and additional checks**: API permissions are combined with resource grants on secrets and folders. Owner/editor/viewer/sharer relationships, expiry and folder inheritance constrain which secrets a caller can reach. Revealing passwords is sensitive even when the permission is named read.

### warden:folders:manage

Create, move and delete folders the caller is granted.

**UI actions**: `manage` on `Folder`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/warden/v1/folders` | listFolders |
| `POST` | `/api/warden/v1/folders` | createFolder |
| `GET` | `/api/warden/v1/folders/tree` | folderTree |
| `GET` | `/api/warden/v1/folders/{id}` | getFolder |
| `PUT` | `/api/warden/v1/folders/{id}` | renameFolder |
| `POST` | `/api/warden/v1/folders/{id}/move` | moveFolder |
| `POST` | `/api/warden/v1/folders/{id}/remove` | deleteFolder |

**Scope and additional checks**: API permissions are combined with resource grants on secrets and folders. Owner/editor/viewer/sharer relationships, expiry and folder inheritance constrain which secrets a caller can reach. Revealing passwords is sensitive even when the permission is named read.

### warden:permissions:manage

Grant and revoke access on resources the caller may share.

**UI actions**: `manage` on `Grant`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Permissions.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/warden/v1/grants` | listGrants |
| `POST` | `/api/warden/v1/grants` | grantAccess |
| `POST` | `/api/warden/v1/grants/{id}/revoke` | revokeAccess |

**Scope and additional checks**: API permissions are combined with resource grants on secrets and folders. Owner/editor/viewer/sharer relationships, expiry and folder inheritance constrain which secrets a caller can reach. Revealing passwords is sensitive even when the permission is named read.

### warden:transfer:import

Import Bitwarden exports.

**UI actions**: `import` on `Transfer`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/warden/v1/transfer/bitwarden/validate` | validateBitwarden |
| `POST` | `/api/warden/v1/transfer/bitwarden/import` | importBitwarden |

**Scope and additional checks**: API permissions are combined with resource grants on secrets and folders. Owner/editor/viewer/sharer relationships, expiry and folder inheritance constrain which secrets a caller can reach. Revealing passwords is sensitive even when the permission is named read.

### warden:transfer:export

Export secrets to Bitwarden format (bulk disclosure).

**UI actions**: `export` on `Transfer`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/warden/v1/transfer/bitwarden/export` | exportBitwarden |

**Scope and additional checks**: API permissions are combined with resource grants on secrets and folders. Owner/editor/viewer/sharer relationships, expiry and folder inheritance constrain which secrets a caller can reach. Revealing passwords is sensitive even when the permission is named read.

### warden:backup:manage

Export and import tenant backups (bulk disclosure with material).

**UI actions**: `manage` on `Backup`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/warden/v1/backup/export` | exportBackup |
| `POST` | `/api/warden/v1/backup/import` | importBackup |

**Scope and additional checks**: API permissions are combined with resource grants on secrets and folders. Owner/editor/viewer/sharer relationships, expiry and folder inheritance constrain which secrets a caller can reach. Revealing passwords is sensitive even when the permission is named read.

### warden:stats:read

Read statistics and the audit trail.

**UI actions**: `read` on `Stats`, `WardenAudit`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/warden/v1/stats` | stats |
| `GET` | `/api/warden/v1/audit` | auditTrail |
| `GET` | `/api/warden/v1/health` | health |

**Scope and additional checks**: API permissions are combined with resource grants on secrets and folders. Owner/editor/viewer/sharer relationships, expiry and folder inheritance constrain which secrets a caller can reach. Revealing passwords is sensitive even when the permission is named read.
<div class="guide-actions"><a href="how-to/warden/docker.html">Install with Docker Compose →</a><a href="how-to/warden/native.html">Install without Docker →</a><a href="downloads/warden.zip">Download Compose bundle ↓</a></div>

## Dependencies and integration

**Required**: TimescaleDB, Valkey, Vault KV/AppRole, key-encryption key, Auth, Portal, mesh identity.

**Optional or feature-dependent**: No additional optional dependency is identified in this summary; see the detailed source reference for supported integrations.

Initialize the Vault KV mount, AppRole and policy before serving. Preserve the KEK with database backups. The gateway's configured body limits must accommodate Warden operations.

The list describes infrastructure/features, not every transitive library. Check the linked deployment reference for exact versions, enabled features and peer grants. [Framework dependencies](architecture/dependencies.html) cover the shared Go libraries.

## Runtime and operation

| Item | Reference |
| --- | --- |
| Service binary | `wardensvc` |
| Public example configuration | `deploy/dev.yaml`; adapt endpoints and paths for your environment |
| Native source build | Go `1.26.3`, toolchain `go1.26.8`, Node 22 for UI |
| Image repository | `ghcr.io/go-tangra/go-tangra-warden`; choose a published compatible version |
| Private admin default | `127.0.0.1:9490`; check actual configuration |
| Health and readiness | `/healthz` and `/readyz` on the configured admin listener |
| Web integration | Gateway registration, permission grants and federated UI |

Bootstrap initializes or validates the module's own stores; serving still needs a valid workload identity, reachable dependencies and policy. Logs, readiness, gateway registration and module-specific checks are described in the detailed references below.

## Configuration field index

The following names and types come from the public Go configuration structures. Group names identify nested types, not flat YAML paths. Required values, defaults, cross-field checks and enabled-feature behavior are explained by the module's source/operations references; never assume every listed setting is optional.

| Configuration group | YAML key | Value type |
| --- | --- | --- |
| `Config` | `db` | `DB` |
| `Config` | `valkey` | `Valkey` |
| `Config` | `vault` | `Vault` |
| `Config` | `gateway` | `Gateway` |
| `Config` | `share` | `Share` |
| `Config` | `mail` | `Mail` |
| `Config` | `limits_warden` | `Limits` |
| `Config` | `enroll` | `Enroll` |
| `DB` | `dsn` | `string` |
| `DB` | `migrate_dsn` | `string` |
| `DB` | `max_conns` | `int32` |
| `Valkey` | `addresses` | `[]string` |
| `Valkey` | `username` | `string` |
| `Valkey` | `password` | `string` |
| `Valkey` | `allow_plaintext` | `bool` |
| `Valkey` | `ca_file` | `string` |
| `Vault` | `address` | `string` |
| `Vault` | `mount` | `string` |
| `Vault` | `role_id_file` | `string` |
| `Vault` | `secret_id_file` | `string` |
| `Vault` | `role_id_secret` | `string` |
| `Vault` | `secret_id_secret` | `string` |
| `Vault` | `allow_plaintext` | `bool` |
| `Vault` | `ca_file` | `string` |
| `Enroll` | `enabled` | `bool` |
| `Enroll` | `enroll_url` | `string` |
| `Enroll` | `lcm_grpc` | `string` |
| `Enroll` | `tenant_id` | `string` |
| `Enroll` | `token_file` | `string` |
| `Enroll` | `state_file` | `string` |
| `Enroll` | `insecure` | `bool` |
| `Gateway` | `service` | `string` |
| `Gateway` | `issuer` | `string` |
| `Share` | `public_origin` | `string` |
| `Share` | `default_validity_seconds` | `int` |
| `Share` | `default_max_opens` | `int` |
| `Mail` | `transport` | `string` |
| `Mail` | `host` | `string` |
| `Mail` | `port` | `int` |
| `Mail` | `username` | `string` |
| `Mail` | `password` | `string` |
| `Mail` | `from` | `string` |
| `Mail` | `allow_plaintext` | `bool` |
| `Limits` | `transfer_max_bytes` | `int64` |
| `Limits` | `lookup_rate_per_minute` | `int` |

[Configuration structures and validation](https://github.com/go-tangra/go-tangra-warden/blob/d7f797813b781cb22f41f2b2a2b75c270e0e660f/internal/config/config.go)

## API operation index

These operations are extracted from the module's OpenAPI contract. Read the source contract for request/response schemas, permission checks and exact route bases; internal mesh endpoints must not be treated as anonymous public APIs.

| Method | Contract path | Operation |
| --- | --- | --- |
| `GET` | `/api/warden/v1/folders` | listFolders |
| `POST` | `/api/warden/v1/folders` | createFolder |
| `GET` | `/api/warden/v1/folders/tree` | folderTree |
| `GET` | `/api/warden/v1/folders/{id}` | getFolder |
| `PUT` | `/api/warden/v1/folders/{id}` | renameFolder |
| `POST` | `/api/warden/v1/folders/{id}/move` | moveFolder |
| `POST` | `/api/warden/v1/folders/{id}/remove` | deleteFolder |
| `GET` | `/api/warden/v1/secrets` | listSecrets |
| `POST` | `/api/warden/v1/secrets` | createSecret |
| `GET` | `/api/warden/v1/secrets/search` | searchSecrets |
| `GET` | `/api/warden/v1/secrets/{id}` | getSecret |
| `PUT` | `/api/warden/v1/secrets/{id}` | updateSecret |
| `POST` | `/api/warden/v1/secrets/{id}/remove` | deleteSecret |
| `POST` | `/api/warden/v1/secrets/{id}/move` | moveSecret |
| `GET` | `/api/warden/v1/secrets/{id}/password` | revealPassword |
| `PUT` | `/api/warden/v1/secrets/{id}/password` | updatePassword |
| `GET` | `/api/warden/v1/secrets/{id}/versions` | listVersions |
| `POST` | `/api/warden/v1/secrets/{id}/versions/{version}/restore` | restoreVersion |
| `GET` | `/api/warden/v1/secrets/{id}/totp` | totpCode |
| `PUT` | `/api/warden/v1/secrets/{id}/totp` | setTotp |
| `DELETE` | `/api/warden/v1/secrets/{id}/totp` | removeTotp |
| `GET` | `/api/warden/v1/grants` | listGrants |
| `POST` | `/api/warden/v1/grants` | grantAccess |
| `POST` | `/api/warden/v1/grants/{id}/revoke` | revokeAccess |
| `GET` | `/api/warden/v1/access/check` | checkAccess |
| `GET` | `/api/warden/v1/access/effective` | effectivePermissions |
| `GET` | `/api/warden/v1/access/resources` | accessibleResources |
| `POST` | `/api/warden/v1/transfer/bitwarden/validate` | validateBitwarden |
| `POST` | `/api/warden/v1/transfer/bitwarden/import` | importBitwarden |
| `POST` | `/api/warden/v1/transfer/bitwarden/export` | exportBitwarden |
| `POST` | `/api/warden/v1/backup/export` | exportBackup |
| `POST` | `/api/warden/v1/backup/import` | importBackup |
| `GET` | `/api/warden/v1/secrets/{id}/shares` | listShares |
| `POST` | `/api/warden/v1/secrets/{id}/shares` | createShare |
| `POST` | `/api/warden/v1/shares/{id}/cancel` | cancelShare |
| `GET` | `/warden/share` | sharePage |
| `POST` | `/api/warden/v1/share/open` | openShare |
| `POST` | `/api/warden/v1/generate` | generatePassword |
| `GET` | `/api/warden/v1/stats` | stats |
| `GET` | `/api/warden/v1/audit` | auditTrail |
| `GET` | `/api/warden/v1/health` | health |

[OpenAPI: api/openapi/warden.yaml](https://github.com/go-tangra/go-tangra-warden/blob/d7f797813b781cb22f41f2b2a2b75c270e0e660f/api/openapi/warden.yaml)

## Detailed source references

- [README.md](sources/warden/README.html) — captured at `d7f797813b78`.
- [docs/dependencies.md](sources/warden/docs/dependencies.html) — captured at `d7f797813b78`.
- [docs/migration-v3.md](sources/warden/docs/migration-v3.html) — captured at `d7f797813b78`.
- [docs/operations.md](sources/warden/docs/operations.html) — captured at `d7f797813b78`.
- [docs/security-model.md](sources/warden/docs/security-model.html) — captured at `d7f797813b78`.

## Limits, diagnostics and recovery

Initialize the Vault KV mount, AppRole and policy before serving. Preserve the KEK with database backups. The gateway's configured body limits must accommodate Warden operations.

Use the module's operations/deployment reference for retention, backup/restore, refusal behavior, interface examples and feature limitations. The installation guides cover common readiness, identity, registration and storage failures.

## Upstream overview: go-tangra-warden

Tenant credential vault for the
[go-tangra v4 platform](https://github.com/go-tangra/go-tangra).

Secrets (name, username, password, host, description, free-form metadata,
optional TOTP seed) live in an unlimited-depth folder tree. **Passwords and seeds
are stored only in HashiCorp Vault** (KV v2, one path per tenant and secret,
AppRole authentication); TimescaleDB holds metadata, version references and
checksums. Access is Zanzibar-style (owner / editor / viewer / sharer on folders
or secrets, granted to users, roles or the tenant, with expiry, inherited down
the tree). External e-mail shares, a password generator, Bitwarden import/export
and tenant backups complete the operator surface. Every operation is audited;
material never reaches the database, the audit trail, logs, search or backups
taken without material.

Security model: [`docs/security-model.md`](sources/warden/docs/security-model.html).
Operations: [`docs/operations.md`](sources/warden/docs/operations.html).
Dependencies: [`docs/dependencies.md`](sources/warden/docs/dependencies.html).
Design history: `specs/005-warden-secrets`.

## Place in the platform

```
go-tangra/go-tangra          platform module + @go-tangra/ui kit
        |
go-tangra-auth  <---->  go-tangra-portal (gateway)  <---->  go-tangra-warden
                              |                               ^
                         go-tangra-lcm (SVIDs)        ipam, ticket, dns (warden sdk)
```

- Built on `github.com/go-tangra/go-tangra/v4` (mTLS transports, identity,
  service policy, audit, observability).
- Verifies platform tokens and registers its permissions, module roles
  (Warden administrator, editor, viewer) and built-in role grants with the
  auth SDK (`github.com/go-tangra/go-tangra-auth/sdk/v4`); see
  [docs/operations.md](sources/warden/docs/operations.html#permissions-and-module-roles).
- Registers with the gateway through the portal SDK
  (`github.com/go-tangra/go-tangra-portal/sdk/v4`), which fronts the browser API,
  the public share route and the federated UI remote.
- Enrolls for its workload identity with lcm (`github.com/go-tangra/go-tangra-lcm/sdk/v4`).

## Modules in this repository

| Module | Path | Consumers |
|---|---|---|
| `github.com/go-tangra/go-tangra-warden/v4` | `/` | the service (`cmd/wardensvc`) and `pkg/wardenmanifest` |
| `github.com/go-tangra/go-tangra-warden/sdk/v4` | `sdk/` | other services: the `warden.v1` protobuf API (secret references resolved over mTLS) |

The service builds against the in-repo SDK through
`replace github.com/go-tangra/go-tangra-warden/sdk/v4 => ./sdk`. Consumers use the
SDK's published `sdk/vX.Y.Z` tag.

## Layout

| Path | Purpose |
|------|---------|
| `cmd/wardensvc` | service binary (serve, `bootstrap`: migrate, vault probe, health; `version`) |
| `internal/app` | wiring: config, platform, store, cache, vault, audit, HTTP/gRPC, gateway lease, permission seeding, reconciler, share sweeper |
| `internal/authz` | Zanzibar evaluation (check, effective, accessible, grants) |
| `internal/secrets`, `internal/folders` | secret and folder services (two-phase vault writes, versions, restore, search, TOTP, reconciliation) |
| `internal/share` | external e-mail shares (hashed tokens, budgets, CIDR policy, sweeper, mail through the notification module) |
| `internal/transfer` | Bitwarden validate/import/export and tenant backups |
| `internal/vault` | KV v2 client with AppRole login and token renewal, plus an in-memory fake |
| `internal/...` | generator, statistics, audit vocabulary, rate counters, repository and SQL bindings (RLS, goose migrations) |
| `pkg/wardenmanifest` | gateway manifest built from the OpenAPI document |
| `ui` | Vue 3 + FlyonUI federated remote on `@go-tangra/ui` |
| `api/openapi`, `api/schema`, `sdk/api/proto` | contracts (`warden.yaml`, Bitwarden schema, `warden.v1`) |
| `deploy` | compose stack (TimescaleDB, Valkey, Vault dev, Mailpit), dev configuration, policy, `vault-init.sh` |
| `tests/{contract,fuzz,integration,testdata}` | contract, fuzz and Docker-backed integration suites |

## Build and test

You need Go 1.26, Node 22, Docker (for integration tests and the image), and a
GitHub token with `read:packages` to install `@go-tangra/ui` from GitHub Packages.

```bash
go build ./... && go vet ./... && go test -race ./...
(cd sdk && go vet ./... && go test -race ./...)
(cd sdk && buf lint)
make test-integration                     # -tags integration, needs Docker
make lint cover fuzz redaction-scan vuln

cd ui
export NODE_AUTH_TOKEN=$(gh auth token)   # ui/.npmrc only references this variable
npm ci && npm run lint && npm run test:unit && npm run build
```

The unit coverage gate requires at least 80 % overall and 100 % for
`internal/{authz,vault,share,secrets,generator}`. Generated code, SQL bindings
and wiring are covered by the integration suite instead.

The integration harness starts real auth and gateway processes. It still builds
them from sibling checkouts (`../auth`, `../gateway`, as in the former monorepo
layout); point it at released binaries or images before running it standalone.

## Run locally

```bash
make compose-up                           # TimescaleDB :5433, Valkey :6380, Vault dev :8200, Mailpit; runs deploy/vault-init.sh
go run ./cmd/wardensvc bootstrap -config deploy/dev.yaml
go run -tags ui ./cmd/wardensvc -config deploy/dev.yaml  # after the ui build
```

The gateway must allow-list the module
(`spiffe://example.org/svc/warden=/api/warden,/warden/share,/ui;warden`) and its
edge must accept 16 MiB bodies for transfers (`limits.max_request_bytes: 16842752`).

## Container image

The image is `ghcr.io/go-tangra/go-tangra-warden`, built by `.github/workflows/ci.yaml`.
It carries `wardensvc` with the embedded UI remote.

```bash
docker buildx build --secret id=npm_token,env=NODE_AUTH_TOKEN \
  --build-arg APP_VERSION=4.0.0 -t go-tangra-warden:dev .
docker run --rm go-tangra-warden:dev version
```

The image runs `wardensvc -config deploy/dev.yaml` as user `app` (uid 10001).
Deployments mount their own configuration and the Vault AppRole credentials
(`vault.role_id_file` / `vault.secret_id_file`); `deploy/.vault` is never copied
into the image.

## Versioning

- Service releases are tagged `vX.Y.Z`. CI publishes the image as `X.Y.Z`,
  `X.Y`, `X` and `sha-<short>`. There is no `latest` tag.
- The SDK is released separately with `sdk/vX.Y.Z` tags. These tags never build an image.
- v4.0.0 rebuilds the service on the go-tangra v4 platform. The v3 line stays on
  the `v3` branch and its `v3.x` tags.
