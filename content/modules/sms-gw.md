# SMS Gateway

Hermes SMS API, carrier receipts, callbacks and tenant management.

**Architecture role**: Communications. [See the complete component map](architecture/index.html).

**Documented source**: `80b17c822eb8` · nearest local service tag `v4.0.0` · v4 major. [Repository at this revision](https://github.com/go-tangra/go-tangra-sms-gw/tree/80b17c822eb8b47b91645b06c4ca637517af42ac). Tags are source metadata, not a claim of image publication or cross-module compatibility.


## Permissions and authorization

This catalogue contains **11 permissions** declared by the [module manifest](https://github.com/go-tangra/go-tangra-sms-gw/blob/80b17c822eb8b47b91645b06c4ca637517af42ac/pkg/smsgwmanifest/manifest.go) at the revision above. Custom-role references use `module:resource:action`; the manifest and API contract use the local `resource:action` form. The action names are distinct grants: do not assume `manage` automatically includes `read` or another action.

Provider read operations redact credentials. dashboard:read exposes deployment-wide monitoring totals across all tenants; grant it only to users who should see that scope. Public Hermes clients authenticate separately from browser module permissions.

[How to assign and verify permissions](architecture/security.html#assign-and-verify-permissions). Module roles and built-in grant mappings are defined in the linked manifest; review those mappings before assigning a broad role.

| Qualified permission | What it allows |
| --- | --- |
| `sms-gw:providers:read` | List and read SMS providers and provider types (credentials redacted) |
| `sms-gw:providers:manage` | Create, change and delete SMS providers and their credentials |
| `sms-gw:templates:read` | List, read and preview SMS templates |
| `sms-gw:templates:manage` | Create, change and delete SMS templates |
| `sms-gw:clients:read` | List and read Hermes API clients (no passwords or secrets) |
| `sms-gw:clients:manage` | Create, change and delete Hermes API clients and reset their passwords |
| `sms-gw:blocks:read` | List and read recipient blocks |
| `sms-gw:blocks:manage` | Create, change and delete recipient blocks |
| `sms-gw:messages:read` | Search messages and read their details and delivery receipts |
| `sms-gw:messages:send` | Send SMS messages from the portal |
| `sms-gw:dashboard:read` | Read the monitoring dashboard: deployment-wide metric totals across all tenants (no records or identifiers) |

### sms-gw:providers:read

List and read SMS providers and provider types (credentials redacted).

**UI actions**: `read` on `SmsProvider`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: SMS providers.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/sms-gw/v1/providers` | listProviders |
| `GET` | `/api/sms-gw/v1/providers/{provider_id}` | getProvider |
| `GET` | `/api/sms-gw/v1/provider-types` | listProviderTypes |

**Scope and additional checks**: Provider read operations redact credentials. dashboard:read exposes deployment-wide monitoring totals across all tenants; grant it only to users who should see that scope. Public Hermes clients authenticate separately from browser module permissions.

### sms-gw:providers:manage

Create, change and delete SMS providers and their credentials.

**UI actions**: `create`, `update`, `delete` on `SmsProvider`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/sms-gw/v1/providers` | createProvider |
| `PATCH` | `/api/sms-gw/v1/providers/{provider_id}` | updateProvider |
| `DELETE` | `/api/sms-gw/v1/providers/{provider_id}` | deleteProvider |

**Scope and additional checks**: Provider read operations redact credentials. dashboard:read exposes deployment-wide monitoring totals across all tenants; grant it only to users who should see that scope. Public Hermes clients authenticate separately from browser module permissions.

### sms-gw:templates:read

List, read and preview SMS templates.

**UI actions**: `read` on `SmsTemplate`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: SMS templates.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/sms-gw/v1/templates` | listTemplates |
| `GET` | `/api/sms-gw/v1/templates/{template_id}` | getTemplate |
| `POST` | `/api/sms-gw/v1/templates/{template_id}/preview` | previewTemplate |

**Scope and additional checks**: Provider read operations redact credentials. dashboard:read exposes deployment-wide monitoring totals across all tenants; grant it only to users who should see that scope. Public Hermes clients authenticate separately from browser module permissions.

### sms-gw:templates:manage

Create, change and delete SMS templates.

**UI actions**: `create`, `update`, `delete` on `SmsTemplate`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/sms-gw/v1/templates` | createTemplate |
| `PATCH` | `/api/sms-gw/v1/templates/{template_id}` | updateTemplate |
| `DELETE` | `/api/sms-gw/v1/templates/{template_id}` | deleteTemplate |

**Scope and additional checks**: Provider read operations redact credentials. dashboard:read exposes deployment-wide monitoring totals across all tenants; grant it only to users who should see that scope. Public Hermes clients authenticate separately from browser module permissions.

### sms-gw:clients:read

List and read Hermes API clients (no passwords or secrets).

**UI actions**: `read` on `SmsApiClient`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: SMS API clients.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/sms-gw/v1/api-clients` | listAPIClients |
| `GET` | `/api/sms-gw/v1/api-clients/{client_id}` | getAPIClient |

**Scope and additional checks**: Provider read operations redact credentials. dashboard:read exposes deployment-wide monitoring totals across all tenants; grant it only to users who should see that scope. Public Hermes clients authenticate separately from browser module permissions.

### sms-gw:clients:manage

Create, change and delete Hermes API clients and reset their passwords.

**UI actions**: `create`, `update`, `delete` on `SmsApiClient`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/sms-gw/v1/api-clients` | createAPIClient |
| `PATCH` | `/api/sms-gw/v1/api-clients/{client_id}` | updateAPIClient |
| `DELETE` | `/api/sms-gw/v1/api-clients/{client_id}` | deleteAPIClient |
| `POST` | `/api/sms-gw/v1/api-clients/{client_id}/reset-password` | resetAPIClientPassword |

**Scope and additional checks**: Provider read operations redact credentials. dashboard:read exposes deployment-wide monitoring totals across all tenants; grant it only to users who should see that scope. Public Hermes clients authenticate separately from browser module permissions.

### sms-gw:blocks:read

List and read recipient blocks.

**UI actions**: `read` on `SmsBlock`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: SMS blocks.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/sms-gw/v1/blocks` | listBlocks |
| `GET` | `/api/sms-gw/v1/blocks/{block_id}` | getBlock |

**Scope and additional checks**: Provider read operations redact credentials. dashboard:read exposes deployment-wide monitoring totals across all tenants; grant it only to users who should see that scope. Public Hermes clients authenticate separately from browser module permissions.

### sms-gw:blocks:manage

Create, change and delete recipient blocks.

**UI actions**: `create`, `update`, `delete` on `SmsBlock`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/sms-gw/v1/blocks` | createBlock |
| `PATCH` | `/api/sms-gw/v1/blocks/{block_id}` | updateBlock |
| `DELETE` | `/api/sms-gw/v1/blocks/{block_id}` | deleteBlock |

**Scope and additional checks**: Provider read operations redact credentials. dashboard:read exposes deployment-wide monitoring totals across all tenants; grant it only to users who should see that scope. Public Hermes clients authenticate separately from browser module permissions.

### sms-gw:messages:read

Search messages and read their details and delivery receipts.

**UI actions**: `read` on `SmsMessage`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: SMS messages.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/sms-gw/v1/messages` | listMessages |
| `GET` | `/api/sms-gw/v1/messages/{message_id}` | getMessage |
| `GET` | `/api/sms-gw/v1/messages/{message_id}/dlrs` | listMessageReceipts |

**Scope and additional checks**: Provider read operations redact credentials. dashboard:read exposes deployment-wide monitoring totals across all tenants; grant it only to users who should see that scope. Public Hermes clients authenticate separately from browser module permissions.

### sms-gw:messages:send

Send SMS messages from the portal.

**UI actions**: `send` on `SmsMessage`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/sms-gw/v1/messages` | sendMessage |

**Scope and additional checks**: Provider read operations redact credentials. dashboard:read exposes deployment-wide monitoring totals across all tenants; grant it only to users who should see that scope. Public Hermes clients authenticate separately from browser module permissions.

### sms-gw:dashboard:read

Read the monitoring dashboard: deployment-wide metric totals across all tenants (no records or identifiers).

**UI actions**: `read` on `SmsDashboard`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: SMS dashboard.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/sms-gw/v1/dashboard/instant` | dashboardInstant |
| `POST` | `/api/sms-gw/v1/dashboard/range` | dashboardRange |

**Scope and additional checks**: Provider read operations redact credentials. dashboard:read exposes deployment-wide monitoring totals across all tenants; grant it only to users who should see that scope. Public Hermes clients authenticate separately from browser module permissions.
<div class="guide-actions"><a href="how-to/sms-gw/docker.html">Install with Docker Compose →</a><a href="how-to/sms-gw/native.html">Install without Docker →</a><a href="downloads/sms-gw.zip">Download Compose bundle ↓</a></div>

## Dependencies and integration

**Required**: PostgreSQL, key-encryption key, Hermes JWT secret, Auth, Portal, mesh identity.

**Optional or feature-dependent**: carrier provider, ACME, Prometheus.

This module is absent from the base platform stack. Its own Compose manifest supplies development PostgreSQL/carrier/callback fixtures and an optional service profile, not the whole control plane. Supply separate KEK and Hermes JWT secrets. Public Hermes TLS and mesh identity are independent.

The list describes infrastructure/features, not every transitive library. Check the linked deployment reference for exact versions, enabled features and peer grants. [Framework dependencies](architecture/dependencies.html) cover the shared Go libraries.

## Runtime and operation

| Item | Reference |
| --- | --- |
| Service binary | `smsgwsvc` |
| Public example configuration | `deploy/container.yaml`; adapt endpoints and paths for your environment |
| Native source build | Go `1.26.3`, toolchain `go1.26.8`, Node 22 for UI |
| Image repository | `ghcr.io/go-tangra/go-tangra-sms-gw`; choose a published compatible version |
| Private admin default | `127.0.0.1:9593`; check actual configuration |
| Health and readiness | `/healthz` and `/readyz` on the configured admin listener |
| Web integration | Gateway registration, permission grants and federated UI |

Bootstrap initializes or validates the module's own stores; serving still needs a valid workload identity, reachable dependencies and policy. Logs, readiness, gateway registration and module-specific checks are described in the detailed references below.

## Configuration field index

The following names and types come from the public Go configuration structures. Group names identify nested types, not flat YAML paths. Required values, defaults, cross-field checks and enabled-feature behavior are explained by the module's source/operations references; never assume every listed setting is optional.

| Configuration group | YAML key | Value type |
| --- | --- | --- |
| `Config` | `db` | `DB` |
| `Config` | `kek` | `KEK` |
| `Config` | `gateway` | `Gateway` |
| `Config` | `enroll` | `Enroll` |
| `Config` | `public` | `Public` |
| `Config` | `public_auth` | `PublicAuth` |
| `Config` | `acme` | `ACME` |
| `Config` | `rate_limits` | `RateLimits` |
| `Config` | `recipients` | `Recipients` |
| `Config` | `webhook` | `Webhook` |
| `Config` | `retention` | `Retention` |
| `Config` | `monitoring` | `Monitoring` |
| `Config` | `query` | `Query` |
| `DB` | `dsn` | `string` |
| `DB` | `migrate_dsn` | `string` |
| `DB` | `max_conns` | `int32` |
| `KEK` | `source` | `string` |
| `KEK` | `path` | `string` |
| `KEK` | `env` | `string` |
| `Gateway` | `service` | `string` |
| `Gateway` | `issuer` | `string` |
| `Gateway` | `auth_service` | `string` |
| `Enroll` | `enabled` | `bool` |
| `Enroll` | `enroll_url` | `string` |
| `Enroll` | `lcm_grpc` | `string` |
| `Enroll` | `tenant_id` | `string` |
| `Enroll` | `token_file` | `string` |
| `Enroll` | `state_file` | `string` |
| `Enroll` | `insecure` | `bool` |
| `Public` | `http_addr` | `string` |
| `Public` | `https_addr` | `string` |
| `Public` | `tls_cert_file` | `string` |
| `Public` | `tls_key_file` | `string` |
| `Public` | `trusted_proxies` | `[]string` |
| `Public` | `max_body_bytes` | `int64` |
| `PublicAuth` | `jwt_secret` | `SecretRef` |
| `PublicAuth` | `access_ttl_seconds` | `int` |
| `PublicAuth` | `refresh_ttl_seconds` | `int` |
| `ACME` | `enabled` | `bool` |
| `ACME` | `domains` | `[]string` |
| `ACME` | `email` | `string` |
| `ACME` | `directory_url` | `string` |
| `ACME` | `directory_ca_bundle` | `string` |
| `ACME` | `cache_dir` | `string` |
| `ACME` | `accept_tos` | `bool` |
| `ACME` | `renew_before` | `time.Duration` |
| `ACME` | `challenge` | `string` |
| `ACME` | `http_addr` | `string` |
| `ACME` | `prefetch` | `bool` |
| `ACME` | `eab_kid` | `string` |
| `ACME` | `eab_hmac_key` | `SecretRef` |
| `ACME` | `allow_insecure_directory` | `bool` |
| `RateLimits` | `login_per_minute` | `float64` |
| `RateLimits` | `login_burst` | `int` |
| `RateLimits` | `send_per_minute` | `float64` |
| `RateLimits` | `send_burst` | `int` |
| `RateLimits` | `dlr_per_minute` | `float64` |
| `RateLimits` | `dlr_burst` | `int` |
| `Recipients` | `min_digits` | `int` |
| `Recipients` | `allowed_prefixes` | `[]string` |
| `Recipients` | `blocked_prefixes` | `[]string` |
| `Webhook` | `allow_http` | `bool` |
| `Webhook` | `allow_private` | `bool` |
| `Webhook` | `queue_size` | `int` |
| `Webhook` | `workers` | `int` |
| `Retention` | `interval` | `time.Duration` |
| `Monitoring` | `prometheus_url` | `string` |
| `Query` | `default_page_size` | `int` |
| `Query` | `max_page_size` | `int` |
| `SecretRef` | `file` | `string` |
| `SecretRef` | `env` | `string` |

[Configuration structures and validation](https://github.com/go-tangra/go-tangra-sms-gw/blob/80b17c822eb8b47b91645b06c4ca637517af42ac/internal/config/config.go)

## API operation index

These operations are extracted from the module's OpenAPI contract. Read the source contract for request/response schemas, permission checks and exact route bases; internal mesh endpoints must not be treated as anonymous public APIs.

| Method | Contract path | Operation |
| --- | --- | --- |
| `GET` | `/api/sms-gw/v1/providers` | listProviders |
| `POST` | `/api/sms-gw/v1/providers` | createProvider |
| `GET` | `/api/sms-gw/v1/providers/{provider_id}` | getProvider |
| `PATCH` | `/api/sms-gw/v1/providers/{provider_id}` | updateProvider |
| `DELETE` | `/api/sms-gw/v1/providers/{provider_id}` | deleteProvider |
| `GET` | `/api/sms-gw/v1/provider-types` | listProviderTypes |
| `GET` | `/api/sms-gw/v1/templates` | listTemplates |
| `POST` | `/api/sms-gw/v1/templates` | createTemplate |
| `GET` | `/api/sms-gw/v1/templates/{template_id}` | getTemplate |
| `PATCH` | `/api/sms-gw/v1/templates/{template_id}` | updateTemplate |
| `DELETE` | `/api/sms-gw/v1/templates/{template_id}` | deleteTemplate |
| `POST` | `/api/sms-gw/v1/templates/{template_id}/preview` | previewTemplate |
| `GET` | `/api/sms-gw/v1/api-clients` | listAPIClients |
| `POST` | `/api/sms-gw/v1/api-clients` | createAPIClient |
| `GET` | `/api/sms-gw/v1/api-clients/{client_id}` | getAPIClient |
| `PATCH` | `/api/sms-gw/v1/api-clients/{client_id}` | updateAPIClient |
| `DELETE` | `/api/sms-gw/v1/api-clients/{client_id}` | deleteAPIClient |
| `POST` | `/api/sms-gw/v1/api-clients/{client_id}/reset-password` | resetAPIClientPassword |
| `GET` | `/api/sms-gw/v1/blocks` | listBlocks |
| `POST` | `/api/sms-gw/v1/blocks` | createBlock |
| `GET` | `/api/sms-gw/v1/blocks/{block_id}` | getBlock |
| `PATCH` | `/api/sms-gw/v1/blocks/{block_id}` | updateBlock |
| `DELETE` | `/api/sms-gw/v1/blocks/{block_id}` | deleteBlock |
| `GET` | `/api/sms-gw/v1/messages` | listMessages |
| `POST` | `/api/sms-gw/v1/messages` | sendMessage |
| `GET` | `/api/sms-gw/v1/messages/{message_id}` | getMessage |
| `GET` | `/api/sms-gw/v1/messages/{message_id}/dlrs` | listMessageReceipts |
| `POST` | `/api/sms-gw/v1/dashboard/instant` | dashboardInstant |
| `POST` | `/api/sms-gw/v1/dashboard/range` | dashboardRange |

[OpenAPI: api/openapi/sms-gw.yaml](https://github.com/go-tangra/go-tangra-sms-gw/blob/80b17c822eb8b47b91645b06c4ca637517af42ac/api/openapi/sms-gw.yaml)

## Detailed source references

- [README.md](sources/sms-gw/README.html) — captured at `80b17c822eb8`.
- [docs/compatibility.md](sources/sms-gw/docs/compatibility.html) — captured at `80b17c822eb8`.
- [docs/dependencies.md](sources/sms-gw/docs/dependencies.html) — captured at `80b17c822eb8`.
- [docs/migration.md](sources/sms-gw/docs/migration.html) — captured at `80b17c822eb8`.
- [docs/operations.md](sources/sms-gw/docs/operations.html) — captured at `80b17c822eb8`.
- [docs/validation.md](sources/sms-gw/docs/validation.html) — captured at `80b17c822eb8`.

## Limits, diagnostics and recovery

This module is absent from the base platform stack. Its own Compose manifest supplies development PostgreSQL/carrier/callback fixtures and an optional service profile, not the whole control plane. Supply separate KEK and Hermes JWT secrets. Public Hermes TLS and mesh identity are independent.

Use the module's operations/deployment reference for retention, backup/restore, refusal behavior, interface examples and feature limitations. The installation guides cover common readiness, identity, registration and storage failures.

## Upstream overview: Tangra SMS Gateway V4

The `sms-gw` module of the go-tangra V4 platform: the legacy Hermes public SMS API (login, send, read, receipt polling) on its own listener, carrier receipt ingestion with signed client callbacks, and a tenant-scoped management API with a federated portal UI. It replaces the v3 gateway at `../go-tangra-sms-gw` (read-only source of behavior).

Module `github.com/go-tangra/go-tangra-sms-gw/v4`, image `ghcr.io/go-tangra/go-tangra-sms-gw`. Specification and contracts: `specs/001-sms-gateway-v4/`. Decisions: `docs/compatibility.md` (preserved and intentionally changed behavior), `docs/operations.md`, `docs/migration.md`, `docs/dependencies.md`; evidence: `docs/validation.md`.

## Layout

| Path | Contents |
|---|---|
| `cmd/smsgwsvc` | the service (`smsgwsvc -config …`, `smsgwsvc bootstrap`, `smsgwsvc version`) |
| `cmd/smsgw-migrate` | read-only legacy snapshot import (`-dry-run`, `-apply`) |
| `internal/publicapi`, `internal/hermes`, `internal/auth`, `internal/sms`, `internal/render`, `internal/provider` | Hermes public listener, client tokens, send pipeline, templates, Voicecom carrier |
| `internal/dlr`, `internal/webhook` | receipt ingestion and client callbacks |
| `internal/httpapi`, `internal/authz`, `internal/metrics` | management API, operator authorization, dashboard |
| `internal/repo`, `internal/store`, `internal/sealed` | PostgreSQL (row-level security per tenant), migrations, sealed secrets |
| `internal/acme`, `internal/housekeeper`, `internal/migrate` | public HTTPS, retention, legacy import |
| `pkg/smsgwmanifest` | gateway manifest and auth registration (permissions, roles, nav, abilities) |
| `api/openapi/sms-gw.yaml` | management API contract (embedded; gateway routes are derived from it) |
| `ui/` | Vue federated remote `sms-gw`, embedded with `-tags ui` |
| `deploy/` | development configuration, local compose (PostgreSQL, mock carrier, callback receiver, pebble) |
| `tests/contract`, `tests/integration` | legacy replay, management, delivery, operations and platform acceptance |

## Setup

Requirements: Go 1.26 (toolchain 1.26.8; unset a stale `GOROOT`), Node 22, Docker (testcontainers and compose). `GOWORK=off`: dependencies are the published go-tangra V4 modules pinned in `go.mod`.

```sh
go mod download
cd ui && NODE_AUTH_TOKEN=$(gh auth token) npm ci   # read:packages for @go-tangra/* on npm.pkg.github.com
```

Development secrets are generated locally and gitignored (`deploy/kek.dev`, 32 random bytes; `deploy/jwt.dev.key`, at least 32 bytes; the mesh SVID under `../../.dev/ca/`). No token, key, certificate or legacy data belongs in source control.

## Build and test

```sh
make generate          # UI API types from api/openapi/sms-gw.yaml
make lint              # go vet + UI eslint/vue-tsc/no-legacy check
make test              # go test -race ./...
make test-ui           # vitest
make test-integration  # PostgreSQL and pebble via docker; skips without docker (SMSGW_TEST_REQUIRE_DOCKER=1 fails instead)
make build             # go build ./...
make build-ui-embedded # UI build + go build -tags ui
NODE_AUTH_TOKEN=$(gh auth token) make image
```

The image (distroless, nonroot) holds `smsgwsvc` (UI embedded, version from `APP_VERSION`) and `smsgw-migrate`, owns the `/state` and `/acme` mount points and contains no key material; configuration, secrets and identity are mounted (`deploy/container.yaml`). CI is `.github/workflows/ci.yaml`: vet/race/build, manifest parity, the PostgreSQL integration suite, UI lint/unit/build and the image (pushed to GHCR on `v4` pushes and `v*` tags; no `latest`). The portal e2e (`ui/tests/e2e`, Playwright) runs against a platform stack with a signed-in operator.

## Run locally

```sh
make compose-up                                              # PostgreSQL :5437, mock carrier :9916, callback receiver :9917
go run ./cmd/smsgwsvc bootstrap -config deploy/dev.yaml      # idempotent migrations and the smsgw_app role; creates no accounts
go run -tags ui ./cmd/smsgwsvc -config deploy/dev.yaml
```

Listeners: public Hermes `127.0.0.1:9901` (optional HTTPS `:9902`), mesh mTLS HTTP `:9984` and gRPC `:9983` (reached only through the gateway), admin `:9593` (`/healthz`, `/readyz`, `/metrics`). On the platform the module needs a gateway allow-list entry for `/api/sms-gw` and a mesh identity (file SVID or lcm enrollment).

## Configuration

YAML (`-config`); secrets are file or environment references. Legacy environment variables (`HTTP_PUBLIC_BIND`, `SMS_GW_TLS_*`, `SMS_GW_JWT_SECRET`, `SMS_GW_*_RPM`, `SMS_GW_PROMETHEUS_URL`, …) override their keys; see `docs/operations.md`.

| Key | Meaning |
|---|---|
| `service_name`, `trust_domain`, `identity`, `enroll` | mesh identity: file SVID or lcm enrollment (state under `/state`) |
| `server`, `admin`, `discovery`, `gateway` | mesh listeners, admin listener, gateway/auth services and portal issuer |
| `db.dsn`, `db.migrate_dsn` | application role (RLS enforced) and migration role |
| `kek` | key-encryption key for sealed provider credentials and callback secrets |
| `public`, `public_auth` | Hermes listener, trusted proxies, body limit; client JWT secret and token lifetimes |
| `acme` | optional automatic public HTTPS (`cache_dir`, domains, directory) |
| `rate_limits`, `recipients` | login/send/receipt token buckets; recipient digit and prefix policy |
| `webhook` | client callback queue and workers; `allow_http`/`allow_private` are development only |
| `retention.interval` | retention sweep (per-provider `retention_days`, 0 keeps forever) |
| `monitoring.prometheus_url` | dashboard source; empty means "not configured" |
| `query` | Hermes list page sizes |

## APIs

- Public Hermes API (legacy wire contract, `specs/001-sms-gateway-v4/contracts/public-api.md`): `POST /hermes/v1/login`, `/refresh_token`, `/logout`, `GET /hermes/v1/me`, `POST|GET /hermes/v1/sms` (and `/v1/sms`), `GET /hermes/v1/sms/{id}`, `GET /hermes/v1/sms/dlr/{id}`, carrier receipts `GET /dlr` and `/hermes/v1/sms/dlr` (always `200 "DLR_OK"`), `/health`. API clients use their own credentials and are bound to one tenant.
- Management API (`api/openapi/sms-gw.yaml`, `/api/sms-gw/v1`, 29 operations): providers and provider types, templates and preview, API clients and password reset, blocks, messages with manual send and receipts, dashboard. Reached only through the gateway with the operator's platform token; every operation is checked again in the module and scoped to the token's tenant. Secrets are write-only.

## Permissions and roles

Registered with auth at startup and every five minutes (`pkg/smsgwmanifest`).

| Permission | Allows | administrator | sender | viewer | monitoring |
|---|---|:-:|:-:|:-:|:-:|
| `providers:read` | list/read providers and types (credentials redacted) | yes | yes | yes | |
| `providers:manage` | create/change/delete providers and credentials | yes | | | |
| `templates:read` | list/read/preview templates | yes | yes | yes | |
| `templates:manage` | create/change/delete templates | yes | | | |
| `clients:read` | list/read API clients | yes | | | |
| `clients:manage` | create/change/delete API clients, reset passwords | yes | | | |
| `blocks:read` | list/read recipient blocks | yes | | | |
| `blocks:manage` | create/change/delete blocks | yes | | | |
| `messages:read` | search messages, read details and receipts | yes | yes | yes | |
| `messages:send` | manual send from the portal | yes | yes | | |
| `dashboard:read` | monitoring dashboard: **deployment-wide totals across all tenants** | yes | | | yes |

Built-in grants: owner and admin hold every permission; member gets nothing. The dashboard's metrics carry no tenant label, so `dashboard:read` is deliberately not part of viewer and its navigation entry shows only with it: grant the monitoring role only to people allowed to see deployment-wide volumes. Legacy `platform:admin`/`sms:admin` strings and identity headers have no effect.

## Migration

`cmd/smsgw-migrate` imports a read-only legacy snapshot into one explicit tenant (dry-run, apply, repeatable, reconciled); IDs and password hashes are kept. Procedure, token continuity, cutover and rollback: `docs/migration.md`.
