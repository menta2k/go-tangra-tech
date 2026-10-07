# LCM

Mesh certificate authority, SVID enrollment and certificate lifecycle.

**Architecture role**: Control plane. [See the complete component map](architecture/index.html).

**Documented source**: `b4511efb2a4a` · nearest local service tag `v4.7.0` · v4 major. [Repository at this revision](https://github.com/go-tangra/go-tangra-lcm/tree/b4511efb2a4a60653b037447898f5476cca7f67a). Tags are source metadata, not a claim of image publication or cross-module compatibility.


## Permissions and authorization

This catalogue contains **14 permissions** declared by the [module manifest](https://github.com/go-tangra/go-tangra-lcm/blob/b4511efb2a4a60653b037447898f5476cca7f67a/pkg/lcmmanifest/manifest.go) at the revision above. Custom-role references use `module:resource:action`; the manifest and API contract use the local `resource:action` form. The action names are distinct grants: do not assume `manage` automatically includes `read` or another action.

Certificate permissions apply to certificates/SVIDs the caller is granted. Issuance, revocation, deployment, issuer management and secret access are separate capabilities; a read grant does not imply those operations.

[How to assign and verify permissions](architecture/security.html#assign-and-verify-permissions). Module roles and built-in grant mappings are defined in the linked manifest; review those mappings before assigning a broad role.

| Qualified permission | What it allows |
| --- | --- |
| `lcm:certificates:read` | List and read certificates/SVIDs the caller is granted |
| `lcm:certificates:issue` | Issue certificates/SVIDs for identities the caller may use |
| `lcm:certificates:manage` | Renew, deploy, update and delete certificates the caller is granted |
| `lcm:certificates:revoke` | Revoke certificates the caller is granted |
| `lcm:issuers:read` | List and read issuers (credentials redacted) |
| `lcm:issuers:manage` | Create, change and delete issuers and their CAs |
| `lcm:enrollment:enroll` | Enroll a workload for an SVID with a platform identity or enrollment token |
| `lcm:jobs:read` | List and read certificate jobs |
| `lcm:jobs:manage` | Cancel and retry certificate jobs |
| `lcm:permissions:manage` | Grant and revoke access on certificates and issuers the caller may share |
| `lcm:secrets:manage` | Create, rotate and delete tenant secrets (ACME/DNS credentials) |
| `lcm:webhooks:manage` | Create and delete outbound webhook endpoints |
| `lcm:backup:manage` | Export and import tenant backups (bulk disclosure with credentials on request) |
| `lcm:stats:read` | Read statistics, health and the audit trail |

### lcm:certificates:read

List and read certificates/SVIDs the caller is granted.

**UI actions**: `read`, `create`, `update`, `delete`, `share`, `use` on `Certificate`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Certificates.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/lcm/v1/certificates` | listCertificates |
| `GET` | `/api/lcm/v1/certificates/{id}` | getCertificate |
| `GET` | `/api/lcm/v1/certificates/{id}/details` | getCertificateDetails |
| `GET` | `/api/lcm/v1/certificates/{id}/download` | downloadCertificate |
| `GET` | `/api/lcm/v1/requests` | listRequests |
| `GET` | `/api/lcm/v1/requests/{id}` | getRequest |
| `GET` | `/api/lcm/v1/trust-bundle` | getTrustBundle |
| `GET` | `/api/lcm/v1/revocations` | listRevocations |
| `GET` | `/api/lcm/v1/crl` | getCrl |
| `GET` | `/api/lcm/v1/installed` | listInstalled |
| `GET` | `/api/lcm/v1/access/check` | checkAccess |
| `GET` | `/api/lcm/v1/access/effective` | effectivePermissions |
| `GET` | `/api/lcm/v1/access/accessible` | listAccessible |
| `GET` | `/api/lcm/v1/stream` | stream |

**Scope and additional checks**: Certificate permissions apply to certificates/SVIDs the caller is granted. Issuance, revocation, deployment, issuer management and secret access are separate capabilities; a read grant does not imply those operations.

### lcm:certificates:issue

Issue certificates/SVIDs for identities the caller may use.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/lcm/v1/certificates/issue` | issueCertificate |
| `POST` | `/api/lcm/v1/certificates/acme` | obtainAcmeCertificate |
| `POST` | `/api/lcm/v1/certificates/import` | importAcmeCertificate |
| `POST` | `/api/lcm/v1/requests` | createRequest |

**Scope and additional checks**: Certificate permissions apply to certificates/SVIDs the caller is granted. Issuance, revocation, deployment, issuer management and secret access are separate capabilities; a read grant does not imply those operations.

### lcm:certificates:manage

Renew, deploy, update and delete certificates the caller is granted.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `PUT` | `/api/lcm/v1/certificates/{id}` | updateCertificate |
| `GET` | `/api/lcm/v1/certificates/{id}/key` | downloadCertificateKey |
| `POST` | `/api/lcm/v1/certificates/{id}/renew` | renewCertificate |
| `POST` | `/api/lcm/v1/certificates/{id}/deploy` | deployCertificate |
| `POST` | `/api/lcm/v1/certificates/{id}/remove` | deleteCertificate |
| `POST` | `/api/lcm/v1/requests/{id}/approve` | approveRequest |
| `POST` | `/api/lcm/v1/requests/{id}/reject` | rejectRequest |
| `GET` | `/api/lcm/v1/deployment-targets` | listDeploymentTargets |
| `POST` | `/api/lcm/v1/deployment-targets` | createDeploymentTarget |

**Scope and additional checks**: Certificate permissions apply to certificates/SVIDs the caller is granted. Issuance, revocation, deployment, issuer management and secret access are separate capabilities; a read grant does not imply those operations.

### lcm:certificates:revoke

Revoke certificates the caller is granted.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/lcm/v1/certificates/{id}/revoke` | revokeCertificate |

**Scope and additional checks**: Certificate permissions apply to certificates/SVIDs the caller is granted. Issuance, revocation, deployment, issuer management and secret access are separate capabilities; a read grant does not imply those operations.

### lcm:issuers:read

List and read issuers (credentials redacted).

**UI actions**: `read`, `create`, `update`, `delete`, `share` on `Issuer`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Issuers.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/lcm/v1/issuers` | listIssuers |
| `GET` | `/api/lcm/v1/issuers/{id}` | getIssuer |
| `GET` | `/api/lcm/v1/dns-providers` | listDnsProviders |

**Scope and additional checks**: Certificate permissions apply to certificates/SVIDs the caller is granted. Issuance, revocation, deployment, issuer management and secret access are separate capabilities; a read grant does not imply those operations.

### lcm:issuers:manage

Create, change and delete issuers and their CAs.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/lcm/v1/issuers` | createIssuer |
| `PUT` | `/api/lcm/v1/issuers/{id}` | updateIssuer |
| `POST` | `/api/lcm/v1/issuers/{id}/remove` | deleteIssuer |

**Scope and additional checks**: Certificate permissions apply to certificates/SVIDs the caller is granted. Issuance, revocation, deployment, issuer management and secret access are separate capabilities; a read grant does not imply those operations.

### lcm:enrollment:enroll

Enroll a workload for an SVID with a platform identity or enrollment token.

**UI actions**: `enroll` on `Enrollment`. These are the manifest’s CASL presentation rules.

The imported OpenAPI operations do not declare a matching `x-freya-permission` for this grant. Use the manifest and server authorization implementation to identify its enforcement; this absence does not indicate public access.

**Scope and additional checks**: Certificate permissions apply to certificates/SVIDs the caller is granted. Issuance, revocation, deployment, issuer management and secret access are separate capabilities; a read grant does not imply those operations.

### lcm:jobs:read

List and read certificate jobs.

**UI actions**: `read`, `manage` on `CertificateJob`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Requests.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/lcm/v1/jobs` | listJobs |
| `GET` | `/api/lcm/v1/jobs/{id}` | getJob |

**Scope and additional checks**: Certificate permissions apply to certificates/SVIDs the caller is granted. Issuance, revocation, deployment, issuer management and secret access are separate capabilities; a read grant does not imply those operations.

### lcm:jobs:manage

Cancel and retry certificate jobs.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/lcm/v1/jobs/{id}/cancel` | cancelJob |
| `POST` | `/api/lcm/v1/jobs/{id}/retry` | retryJob |

**Scope and additional checks**: Certificate permissions apply to certificates/SVIDs the caller is granted. Issuance, revocation, deployment, issuer management and secret access are separate capabilities; a read grant does not imply those operations.

### lcm:permissions:manage

Grant and revoke access on certificates and issuers the caller may share.

**UI actions**: `manage` on `LcmGrant`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Permissions.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/lcm/v1/grants` | listGrants |
| `POST` | `/api/lcm/v1/grants` | grant |
| `POST` | `/api/lcm/v1/grants/{id}/revoke` | revokeGrant |

**Scope and additional checks**: Certificate permissions apply to certificates/SVIDs the caller is granted. Issuance, revocation, deployment, issuer management and secret access are separate capabilities; a read grant does not imply those operations.

### lcm:secrets:manage

Create, rotate and delete tenant secrets (ACME/DNS credentials).

**UI actions**: `manage` on `TenantSecret`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Secrets.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/lcm/v1/secrets` | listSecrets |
| `POST` | `/api/lcm/v1/secrets` | createSecret |
| `PUT` | `/api/lcm/v1/secrets/{id}` | updateSecret |
| `POST` | `/api/lcm/v1/secrets/{id}/rotate` | rotateSecret |
| `POST` | `/api/lcm/v1/secrets/{id}/remove` | deleteSecret |

**Scope and additional checks**: Certificate permissions apply to certificates/SVIDs the caller is granted. Issuance, revocation, deployment, issuer management and secret access are separate capabilities; a read grant does not imply those operations.

### lcm:webhooks:manage

Create and delete outbound webhook endpoints.

**UI actions**: `manage` on `Webhook`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/lcm/v1/webhooks` | listWebhooks |
| `POST` | `/api/lcm/v1/webhooks` | createWebhook |
| `POST` | `/api/lcm/v1/webhooks/{id}/remove` | deleteWebhook |

**Scope and additional checks**: Certificate permissions apply to certificates/SVIDs the caller is granted. Issuance, revocation, deployment, issuer management and secret access are separate capabilities; a read grant does not imply those operations.

### lcm:backup:manage

Export and import tenant backups (bulk disclosure with credentials on request).

**UI actions**: `manage` on `LcmBackup`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/lcm/v1/backup/export` | exportBackup |
| `POST` | `/api/lcm/v1/backup/import` | importBackup |

**Scope and additional checks**: Certificate permissions apply to certificates/SVIDs the caller is granted. Issuance, revocation, deployment, issuer management and secret access are separate capabilities; a read grant does not imply those operations.

### lcm:stats:read

Read statistics, health and the audit trail.

**UI actions**: `read` on `LcmStats`, `LcmAudit`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Dashboard, Audit.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/lcm/v1/stats` | stats |
| `GET` | `/api/lcm/v1/audit` | auditTrail |
| `GET` | `/api/lcm/v1/health` | health |

**Scope and additional checks**: Certificate permissions apply to certificates/SVIDs the caller is granted. Issuance, revocation, deployment, issuer management and secret access are separate capabilities; a read grant does not imply those operations.
<div class="guide-actions"><a href="how-to/lcm/docker.html">Install with Docker Compose →</a><a href="how-to/lcm/native.html">Install without Docker →</a><a href="downloads/lcm.zip">Download Compose bundle ↓</a></div>

## Dependencies and integration

**Required**: TimescaleDB, Valkey, key-encryption key, Auth, Portal.

**Optional or feature-dependent**: ACME issuer, DNS provider.

LCM bootstraps the persistent mesh root. The `bootstrap -out … -services …` mode exports initial identities; preserve the database and KEK together. Public ACME certificates and mesh SVIDs serve different purposes.

The list describes infrastructure/features, not every transitive library. Check the linked deployment reference for exact versions, enabled features and peer grants. [Framework dependencies](architecture/dependencies.html) cover the shared Go libraries.

## Runtime and operation

| Item | Reference |
| --- | --- |
| Service binary | `lcmsvc` |
| Public example configuration | `deploy/dev.yaml`; adapt endpoints and paths for your environment |
| Native source build | Go `1.26.3`, toolchain `go1.26.8`, Node 22 for UI |
| Image repository | `ghcr.io/go-tangra/go-tangra-lcm`; choose a published compatible version |
| Private admin default | `127.0.0.1:9390`; check actual configuration |
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
| `Config` | `renewal` | `Renewal` |
| `Config` | `gateway` | `Gateway` |
| `Config` | `acme` | `ACME` |
| `Config` | `dns` | `DNS` |
| `Config` | `limits_lcm` | `Limits` |
| `Config` | `task_scheduler` | `TaskScheduler` |
| `Config` | `notification` | `Notification` |
| `Config` | `enroll_listener` | `string` |
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
| `Renewal` | `interval_seconds` | `int` |
| `Renewal` | `lease_seconds` | `int` |
| `Renewal` | `workers` | `int` |
| `Renewal` | `short_lived_fraction` | `float64` |
| `Renewal` | `long_lived_days` | `int` |
| `Gateway` | `service` | `string` |
| `Gateway` | `issuer` | `string` |
| `ACME` | `allow_plaintext_dns` | `bool` |
| `DNS` | `service` | `string` |
| `TaskScheduler` | `enabled` | `bool` |
| `TaskScheduler` | `service` | `string` |
| `Notification` | `service` | `string` |
| `Limits` | `backup_max_bytes` | `int64` |
| `Limits` | `csr_max_bytes` | `int64` |
| `Limits` | `webhook_max_bytes` | `int64` |
| `Limits` | `streams_per_user` | `int` |
| `Limits` | `streams_per_tenant` | `int` |
| `Limits` | `replay_window_seconds` | `int` |

[Configuration structures and validation](https://github.com/go-tangra/go-tangra-lcm/blob/b4511efb2a4a60653b037447898f5476cca7f67a/internal/config/config.go)

## API operation index

These operations are extracted from the module's OpenAPI contract. Read the source contract for request/response schemas, permission checks and exact route bases; internal mesh endpoints must not be treated as anonymous public APIs.

| Method | Contract path | Operation |
| --- | --- | --- |
| `GET` | `/api/lcm/v1/issuers` | listIssuers |
| `POST` | `/api/lcm/v1/issuers` | createIssuer |
| `GET` | `/api/lcm/v1/issuers/{id}` | getIssuer |
| `PUT` | `/api/lcm/v1/issuers/{id}` | updateIssuer |
| `POST` | `/api/lcm/v1/issuers/{id}/remove` | deleteIssuer |
| `GET` | `/api/lcm/v1/dns-providers` | listDnsProviders |
| `GET` | `/api/lcm/v1/certificates` | listCertificates |
| `POST` | `/api/lcm/v1/certificates/issue` | issueCertificate |
| `POST` | `/api/lcm/v1/certificates/acme` | obtainAcmeCertificate |
| `POST` | `/api/lcm/v1/certificates/import` | importAcmeCertificate |
| `GET` | `/api/lcm/v1/certificates/{id}` | getCertificate |
| `PUT` | `/api/lcm/v1/certificates/{id}` | updateCertificate |
| `GET` | `/api/lcm/v1/certificates/{id}/details` | getCertificateDetails |
| `GET` | `/api/lcm/v1/certificates/{id}/download` | downloadCertificate |
| `GET` | `/api/lcm/v1/certificates/{id}/key` | downloadCertificateKey |
| `POST` | `/api/lcm/v1/certificates/{id}/renew` | renewCertificate |
| `POST` | `/api/lcm/v1/certificates/{id}/revoke` | revokeCertificate |
| `POST` | `/api/lcm/v1/certificates/{id}/deploy` | deployCertificate |
| `POST` | `/api/lcm/v1/certificates/{id}/remove` | deleteCertificate |
| `GET` | `/api/lcm/v1/requests` | listRequests |
| `POST` | `/api/lcm/v1/requests` | createRequest |
| `GET` | `/api/lcm/v1/requests/{id}` | getRequest |
| `POST` | `/api/lcm/v1/requests/{id}/approve` | approveRequest |
| `POST` | `/api/lcm/v1/requests/{id}/reject` | rejectRequest |
| `GET` | `/api/lcm/v1/jobs` | listJobs |
| `GET` | `/api/lcm/v1/jobs/{id}` | getJob |
| `POST` | `/api/lcm/v1/jobs/{id}/cancel` | cancelJob |
| `POST` | `/api/lcm/v1/jobs/{id}/retry` | retryJob |
| `POST` | `/api/lcm/v1/enroll` | enroll |
| `GET` | `/api/lcm/v1/bootstrap-bundle` | getBootstrapBundle |
| `GET` | `/api/lcm/v1/trust-bundle` | getTrustBundle |
| `GET` | `/api/lcm/v1/revocations` | listRevocations |
| `GET` | `/api/lcm/v1/crl` | getCrl |
| `GET` | `/api/lcm/v1/deployment-targets` | listDeploymentTargets |
| `POST` | `/api/lcm/v1/deployment-targets` | createDeploymentTarget |
| `GET` | `/api/lcm/v1/installed` | listInstalled |
| `GET` | `/api/lcm/v1/secrets` | listSecrets |
| `POST` | `/api/lcm/v1/secrets` | createSecret |
| `PUT` | `/api/lcm/v1/secrets/{id}` | updateSecret |
| `POST` | `/api/lcm/v1/secrets/{id}/rotate` | rotateSecret |
| `POST` | `/api/lcm/v1/secrets/{id}/remove` | deleteSecret |
| `GET` | `/api/lcm/v1/webhooks` | listWebhooks |
| `POST` | `/api/lcm/v1/webhooks` | createWebhook |
| `POST` | `/api/lcm/v1/webhooks/{id}/remove` | deleteWebhook |
| `GET` | `/api/lcm/v1/grants` | listGrants |
| `POST` | `/api/lcm/v1/grants` | grant |
| `POST` | `/api/lcm/v1/grants/{id}/revoke` | revokeGrant |
| `GET` | `/api/lcm/v1/access/check` | checkAccess |
| `GET` | `/api/lcm/v1/access/effective` | effectivePermissions |
| `GET` | `/api/lcm/v1/access/accessible` | listAccessible |
| `GET` | `/api/lcm/v1/stream` | stream |
| `POST` | `/api/lcm/v1/backup/export` | exportBackup |
| `POST` | `/api/lcm/v1/backup/import` | importBackup |
| `GET` | `/api/lcm/v1/stats` | stats |
| `GET` | `/api/lcm/v1/audit` | auditTrail |
| `GET` | `/api/lcm/v1/health` | health |

[OpenAPI: api/openapi/lcm.yaml](https://github.com/go-tangra/go-tangra-lcm/blob/b4511efb2a4a60653b037447898f5476cca7f67a/api/openapi/lcm.yaml)

## Detailed source references

- [README.md](sources/lcm/README.html) — captured at `b4511efb2a4a`.
- [docs/README.md](sources/lcm/docs/README.html) — captured at `b4511efb2a4a`.
- [docs/operations.md](sources/lcm/docs/operations.html) — captured at `b4511efb2a4a`.
- [docs/security-review.md](sources/lcm/docs/security-review.html) — captured at `b4511efb2a4a`.

## Limits, diagnostics and recovery

LCM bootstraps the persistent mesh root. The `bootstrap -out … -services …` mode exports initial identities; preserve the database and KEK together. Public ACME certificates and mesh SVIDs serve different purposes.

Use the module's operations/deployment reference for retention, backup/restore, refusal behavior, interface examples and feature limitations. The installation guides cover common readiness, identity, registration and storage failures.

## Upstream overview: go-tangra-lcm

Certificate and SVID lifecycle management service for the
[go-tangra v4 platform](https://github.com/go-tangra/go-tangra).

It is the platform's SPIFFE certificate authority. Per tenant and trust domain it
generates a self-signed CA on first use (plus optional ACME DNS-01 issuers), issues
X.509-SVIDs and certificates from CSRs or service-generated keys, enrolls workloads
with their platform identity or a short-lived enrollment token, renews before expiry,
streams issued/renewed/revoked events to browsers (SSE) and workloads (`Agent.Watch`),
and publishes revocations, a signed CRL and the trust bundle. Tenant secrets,
signed webhooks, audit, statistics and backup export/import complete the operator
surface. All key material is sealed with envelope encryption.

Overview: [`docs/README.md`](sources/lcm/docs/README.html).
Operations: [`docs/operations.md`](sources/lcm/docs/operations.html).
Security review: [`docs/security-review.md`](sources/lcm/docs/security-review.html).
Design history: `specs/007-lcm-service`.

## Place in the platform

```
go-tangra/go-tangra          platform module + @go-tangra/ui kit
        |
go-tangra-auth  <---->  go-tangra-portal (gateway)  <---->  go-tangra-lcm
                                                              ^
                                    deployer, dns, workloads (lcm sdk, lcm-agent)
```

- Built on `github.com/go-tangra/go-tangra/v4` (mTLS transports, identity,
  service policy, audit, observability).
- Verifies platform tokens and registers its permissions, module roles and
  built-in role grants with the auth SDK
  (`github.com/go-tangra/go-tangra-auth/sdk/v4`); see
  [docs/README.md](sources/lcm/docs/README.html#permissions-and-module-roles).
- Registers with the gateway through the portal SDK
  (`github.com/go-tangra/go-tangra-portal/sdk/v4`), which fronts the browser API
  and the federated UI remote.

## Modules in this repository

| Module | Path | Consumers |
|---|---|---|
| `github.com/go-tangra/go-tangra-lcm/v4` | `/` | the service (`cmd/lcmsvc`), `cmd/lcm-agent`, `cmd/lcm-devca` and `pkg/lcmmanifest` |
| `github.com/go-tangra/go-tangra-lcm/sdk/v4` | `sdk/` | other services and workloads: the `lcm.v1` protobuf API, `pkg/lcmclient` (client and agent loop), `pkg/lcmidentity`, `pkg/dnschallenge` |

The service builds against the in-repo SDK through
`replace github.com/go-tangra/go-tangra-lcm/sdk/v4 => ./sdk`. Consumers use the
SDK's published `sdk/vX.Y.Z` tag.

## Layout

| Path | Purpose |
|------|---------|
| `cmd/lcmsvc` | service binary (serve, `bootstrap`, `version`) |
| `cmd/lcm-agent` | workload daemon: enroll, write cert/key/bundle, auto-renew |
| `cmd/lcm-devca` | offline development CA and per-service SVIDs (development only) |
| `internal/app` | wiring: config, platform, stores, services, HTTP/gRPC |
| `internal/...` | CA, CSR, ACME, issuance, enrollment, renewal, revocation, streams, sealing, authz, secrets, webhooks, backup and their SQL bindings |
| `ui` | Vue 3 + FlyonUI federated remote on `@go-tangra/ui` |
| `api/openapi`, `api/schema`, `sdk/api/proto` | contracts (`lcm.yaml`, backup schema, `lcm.v1`) |
| `deploy` | compose stack, dev configuration, development KEK, policies |
| `tests/{contract,fuzz,integration,security}` | contract, fuzz, Docker-backed integration and security suites |

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

The unit coverage gate requires at least 80 % overall and 100 % for the
crypto, authorization, sealing and stream packages. Generated code, SQL bindings
and wiring are covered by the integration suite instead.

## Run locally

```bash
make compose-up                           # TimescaleDB, Valkey, Pebble (ACME), challtestsrv (DNS)
go run ./cmd/lcmsvc bootstrap -config deploy/dev.yaml
go run -tags ui ./cmd/lcmsvc -config deploy/dev.yaml    # after the ui build
```

## Container image

The image is `ghcr.io/go-tangra/go-tangra-lcm`, built by `.github/workflows/ci.yaml`.
It carries `lcmsvc` (with the embedded UI remote) and `lcm-devca`.

```bash
docker buildx build --secret id=npm_token,env=NODE_AUTH_TOKEN \
  --build-arg APP_VERSION=4.0.0 -t go-tangra-lcm:dev .
docker run --rm go-tangra-lcm:dev version
```

The image runs `lcmsvc -config deploy/dev.yaml` as user `app` (uid 10001).
Production deployments mount their own configuration and key-encryption key.

## Versioning

- Service releases are tagged `vX.Y.Z`. CI publishes the image as `X.Y.Z`,
  `X.Y`, `X` and `sha-<short>`. There is no `latest` tag.
- The SDK is released separately with `sdk/vX.Y.Z` tags. These tags never build an image.
- v4.0.0 rebuilds the service on the go-tangra v4 platform. The v3 line stays on
  the `v3` branch and its `v3.x` tags.
