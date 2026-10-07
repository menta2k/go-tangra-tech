# Signing

PDF templates, signing submissions, personal and qualified signatures.

**Architecture role**: Business modules. [See the complete component map](architecture/index.html).

**Documented source**: `041fcb91357f` · nearest local service tag `v4.2.2` · v4 major. [Repository at this revision](https://github.com/go-tangra/go-tangra-signing/tree/041fcb91357fc68d5d736a2bc16450a1199254dd). Tags are source metadata, not a claim of image publication or cross-module compatibility.


## Permissions and authorization

This catalogue contains **7 permissions** declared by the [module manifest](https://github.com/go-tangra/go-tangra-signing/blob/041fcb91357fc68d5d736a2bc16450a1199254dd/pkg/signingmanifest/manifest.go) at the revision above. Custom-role references use `module:resource:action`; the manifest and API contract use the local `resource:action` form. The action names are distinct grants: do not assume `manage` automatically includes `read` or another action.

Module permissions gate actions within the authenticated tenant. The endpoint still enforces its resource and workflow checks; a UI ability describes presentation and does not replace server authorization.

[How to assign and verify permissions](architecture/security.html#assign-and-verify-permissions). Module roles and built-in grant mappings are defined in the linked manifest; review those mappings before assigning a broad role.

| Qualified permission | What it allows |
| --- | --- |
| `signing:signing:sign` | Sign or decline documents assigned to me, see my inbox and manage my own signing certificate |
| `signing:signing:read` | View templates, folders and every submission of the tenant, and verify signed documents |
| `signing:templates:manage` | Create, edit, clone, archive and delete templates and folders, and use the field builder |
| `signing:submissions:create` | Send documents for signature and manage the submissions I sent |
| `signing:submissions:manage` | Cancel, resend, replace signers of and delete any submission of the tenant |
| `signing:certificates:manage` | Manage the tenant signing CA and certificates, revoke certificates and sign documents with administrator certificates |
| `signing:backup:manage` | Export and import the tenant's signing data |

### signing:signing:sign

Sign or decline documents assigned to me, see my inbox and manage my own signing certificate.

**UI actions**: `sign` on `SigningDocument`, `SigningCertificate`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: To sign, My certificate.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/signing/v1/submissions` | listSubmissions |
| `GET` | `/api/signing/v1/submissions/{id}` | getSubmission |
| `DELETE` | `/api/signing/v1/submissions/{id}` | deleteSubmission |
| `POST` | `/api/signing/v1/submissions/{id}/send` | sendSubmission |
| `POST` | `/api/signing/v1/submissions/{id}/cancel` | cancelSubmission |
| `PUT` | `/api/signing/v1/submissions/{id}/signers/{sid}` | replaceSigner |
| `POST` | `/api/signing/v1/submissions/{id}/signers/{sid}/resend` | resendInvitation |
| `GET` | `/api/signing/v1/submissions/{id}/events` | listSubmissionEvents |
| `GET` | `/api/signing/v1/submissions/{id}/document` | downloadSubmissionDocument |
| `GET` | `/api/signing/v1/submissions/{id}/audit-trail` | downloadAuditTrail |
| `GET` | `/api/signing/v1/submissions/{id}/package` | downloadPackage |
| `GET` | `/api/signing/v1/inbox` | inbox |
| `GET` | `/api/signing/v1/signing/{signer_id}` | getSession |
| `GET` | `/api/signing/v1/signing/{signer_id}/document` | downloadSessionDocument |
| `POST` | `/api/signing/v1/signing/{signer_id}/open` | openSession |
| `POST` | `/api/signing/v1/signing/{signer_id}/sign` | sign |
| `POST` | `/api/signing/v1/signing/{signer_id}/decline` | decline |
| `POST` | `/api/signing/v1/signing/{signer_id}/qes/prepare` | prepareQES |
| `POST` | `/api/signing/v1/signing/{signer_id}/qes/complete` | completeQES |
| `GET` | `/api/signing/v1/me/certificate` | getMyCertificate |
| `POST` | `/api/signing/v1/me/certificate` | setupMyCertificate |
| `POST` | `/api/signing/v1/me/certificate/pin` | changeMyPin |
| `POST` | `/api/signing/v1/me/certificate/renew` | renewMyCertificate |
| `POST` | `/api/signing/v1/me/certificate/revoke` | revokeMyCertificate |
| `GET` | `/api/signing/v1/stream` | streamEvents |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### signing:signing:read

View templates, folders and every submission of the tenant, and verify signed documents.

**UI actions**: `read` on `SigningTemplate`, `SigningSubmission`, `SigningVerification`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Templates, Verify.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/signing/v1/folders` | listFolders |
| `GET` | `/api/signing/v1/templates` | listTemplates |
| `GET` | `/api/signing/v1/templates/{id}` | getTemplate |
| `GET` | `/api/signing/v1/templates/{id}/pdf` | downloadTemplatePdf |
| `GET` | `/api/signing/v1/ca/crl` | downloadCRL |
| `POST` | `/api/signing/v1/verify` | verifyDocument |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### signing:templates:manage

Create, edit, clone, archive and delete templates and folders, and use the field builder.

**UI actions**: `create`, `update`, `delete` on `SigningTemplate`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/signing/v1/folders` | createFolder |
| `PATCH` | `/api/signing/v1/folders/{id}` | updateFolder |
| `DELETE` | `/api/signing/v1/folders/{id}` | deleteFolder |
| `POST` | `/api/signing/v1/templates` | createTemplate |
| `PATCH` | `/api/signing/v1/templates/{id}` | updateTemplate |
| `DELETE` | `/api/signing/v1/templates/{id}` | deleteTemplate |
| `PUT` | `/api/signing/v1/templates/{id}/fields` | saveTemplateFields |
| `POST` | `/api/signing/v1/templates/{id}/clone` | cloneTemplate |
| `POST` | `/api/signing/v1/templates/{id}/detect-fields` | detectTemplateFields |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### signing:submissions:create

Send documents for signature and manage the submissions I sent.

**UI actions**: `create` on `SigningSubmission`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Submissions.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/signing/v1/submissions` | createSubmission |
| `GET` | `/api/signing/v1/users` | listMembers |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### signing:submissions:manage

Cancel, resend, replace signers of and delete any submission of the tenant.

**UI actions**: `manage` on `SigningSubmission`. These are the manifest’s CASL presentation rules.

The imported OpenAPI operations do not declare a matching `x-freya-permission` for this grant. Use the manifest and server authorization implementation to identify its enforcement; this absence does not indicate public access.

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### signing:certificates:manage

Manage the tenant signing CA and certificates, revoke certificates and sign documents with administrator certificates.

**UI actions**: `manage` on `SigningCertificate`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Certificates.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/signing/v1/certificates` | listCertificates |
| `POST` | `/api/signing/v1/certificates` | createAdminCertificate |
| `GET` | `/api/signing/v1/certificates/{id}` | getCertificate |
| `POST` | `/api/signing/v1/certificates/{id}/revoke` | revokeCertificate |
| `POST` | `/api/signing/v1/documents/sign` | signDocument |
| `GET` | `/api/signing/v1/documents/{id}` | downloadSignedDocument |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### signing:backup:manage

Export and import the tenant's signing data.

**UI actions**: `manage` on `SigningBackup`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/signing/v1/backup/export` | exportBackup |
| `POST` | `/api/signing/v1/backup/import` | importBackup |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.
<div class="guide-actions"><a href="how-to/signing/docker.html">Install with Docker Compose →</a><a href="how-to/signing/native.html">Install without Docker →</a><a href="downloads/signing.zip">Download Compose bundle ↓</a></div>

## Dependencies and integration

**Required**: TimescaleDB, Valkey, S3-compatible storage, key-encryption key, Auth, Portal, mesh identity.

**Optional or feature-dependent**: Scheduler, Notification, Warden, B-Trust BISS.

Configure S3 storage, KEK and the tenant signing CA lifecycle. Expiry/reminder tasks depend on Scheduler integration; a source build alone does not enable them. Qualified signatures require the user's B-Trust BISS/card environment.

The list describes infrastructure/features, not every transitive library. Check the linked deployment reference for exact versions, enabled features and peer grants. [Framework dependencies](architecture/dependencies.html) cover the shared Go libraries.

## Runtime and operation

| Item | Reference |
| --- | --- |
| Service binary | `signingsvc` |
| Public example configuration | `deploy/container.yaml`; adapt endpoints and paths for your environment |
| Native source build | Go `1.26.3`, toolchain `go1.26.8`, Node 22 for UI |
| Image repository | `ghcr.io/go-tangra/go-tangra-signing`; choose a published compatible version |
| Private admin default | `127.0.0.1:9860`; check actual configuration |
| Health and readiness | `/healthz` and `/readyz` on the configured admin listener |
| Web integration | Gateway registration, permission grants and federated UI |

Bootstrap initializes or validates the module's own stores; serving still needs a valid workload identity, reachable dependencies and policy. Logs, readiness, gateway registration and module-specific checks are described in the detailed references below.

## Configuration field index

The following names and types come from the public Go configuration structures. Group names identify nested types, not flat YAML paths. Required values, defaults, cross-field checks and enabled-feature behavior are explained by the module's source/operations references; never assume every listed setting is optional.

| Configuration group | YAML key | Value type |
| --- | --- | --- |
| `Config` | `db` | `DB` |
| `Config` | `valkey` | `Valkey` |
| `Config` | `gateway` | `Gateway` |
| `Config` | `mesh_enroll` | `MeshEnroll` |
| `Config` | `events` | `Events` |
| `Config` | `platform_tenant_id` | `string` |
| `Config` | `kek` | `KEK` |
| `Config` | `object_store` | `ObjectStore` |
| `Config` | `auth` | `Service` |
| `Config` | `notification` | `Service` |
| `Config` | `warden` | `Service` |
| `Config` | `task_scheduler` | `TaskScheduler` |
| `Config` | `links` | `Links` |
| `Config` | `limits_signing` | `Limits` |
| `Config` | `signing` | `Signing` |
| `Config` | `verify` | `Verify` |
| `Config` | `qes` | `QES` |
| `DB` | `dsn` | `string` |
| `DB` | `migrate_dsn` | `string` |
| `DB` | `max_conns` | `int32` |
| `Valkey` | `addresses` | `[]string` |
| `Valkey` | `username` | `string` |
| `Valkey` | `password` | `string` |
| `Valkey` | `allow_plaintext` | `bool` |
| `Valkey` | `ca_file` | `string` |
| `Gateway` | `service` | `string` |
| `Gateway` | `issuer` | `string` |
| `MeshEnroll` | `enabled` | `bool` |
| `MeshEnroll` | `enroll_url` | `string` |
| `MeshEnroll` | `lcm_grpc` | `string` |
| `MeshEnroll` | `tenant_id` | `string` |
| `MeshEnroll` | `token_file` | `string` |
| `MeshEnroll` | `state_file` | `string` |
| `MeshEnroll` | `insecure` | `bool` |
| `Events` | `enabled` | `bool` |
| `KEK` | `source` | `string` |
| `KEK` | `path` | `string` |
| `KEK` | `env` | `string` |
| `ObjectStore` | `endpoint` | `string` |
| `ObjectStore` | `bucket` | `string` |
| `ObjectStore` | `region` | `string` |
| `ObjectStore` | `use_ssl` | `bool` |
| `ObjectStore` | `access_key` | `string` |
| `ObjectStore` | `secret_key` | `string` |
| `Service` | `service` | `string` |
| `TaskScheduler` | `enabled` | `bool` |
| `TaskScheduler` | `service` | `string` |
| `Links` | `portal_base_url` | `string` |
| `Limits` | `max_pdf_bytes` | `int64` |
| `Limits` | `max_pdf_pages` | `int` |
| `Limits` | `max_fields` | `int` |
| `Limits` | `max_signers` | `int` |
| `Limits` | `max_image_bytes` | `int64` |
| `Limits` | `max_field_upload_bytes` | `int64` |
| `Limits` | `parse_timeout_seconds` | `int` |
| `Limits` | `max_page_size` | `int` |
| `Limits` | `max_backup_bytes` | `int64` |
| `Limits` | `signings_per_minute` | `int` |
| `Limits` | `qes_preparation_minutes` | `int` |
| `Signing` | `ca_validity_years` | `int` |
| `Signing` | `ca_renew_before_years` | `int` |
| `Signing` | `cert_validity_years` | `int` |
| `Signing` | `crl_validity_days` | `int` |
| `Signing` | `pin_min` | `int` |
| `Signing` | `pin_max` | `int` |
| `Signing` | `pin_iterations` | `int` |
| `Signing` | `lock_attempts` | `int` |
| `Signing` | `lock_minutes` | `int` |
| `Signing` | `audit_job_max_attempts` | `int` |
| `Signing` | `audit_job_interval_ms` | `int` |
| `Verify` | `extra_roots_file` | `string` |
| `Verify` | `use_system_roots` | `bool` |
| `QES` | `origin_cert_file` | `string` |
| `QES` | `origin_key_file` | `string` |

[Configuration structures and validation](https://github.com/go-tangra/go-tangra-signing/blob/041fcb91357fc68d5d736a2bc16450a1199254dd/internal/config/config.go)

## API operation index

These operations are extracted from the module's OpenAPI contract. Read the source contract for request/response schemas, permission checks and exact route bases; internal mesh endpoints must not be treated as anonymous public APIs.

| Method | Contract path | Operation |
| --- | --- | --- |
| `GET` | `/api/signing/v1/health` | health |
| `GET` | `/api/signing/v1/folders` | listFolders |
| `POST` | `/api/signing/v1/folders` | createFolder |
| `PATCH` | `/api/signing/v1/folders/{id}` | updateFolder |
| `DELETE` | `/api/signing/v1/folders/{id}` | deleteFolder |
| `GET` | `/api/signing/v1/templates` | listTemplates |
| `POST` | `/api/signing/v1/templates` | createTemplate |
| `GET` | `/api/signing/v1/templates/{id}` | getTemplate |
| `PATCH` | `/api/signing/v1/templates/{id}` | updateTemplate |
| `DELETE` | `/api/signing/v1/templates/{id}` | deleteTemplate |
| `PUT` | `/api/signing/v1/templates/{id}/fields` | saveTemplateFields |
| `POST` | `/api/signing/v1/templates/{id}/clone` | cloneTemplate |
| `GET` | `/api/signing/v1/templates/{id}/pdf` | downloadTemplatePdf |
| `POST` | `/api/signing/v1/templates/{id}/detect-fields` | detectTemplateFields |
| `GET` | `/api/signing/v1/submissions` | listSubmissions |
| `POST` | `/api/signing/v1/submissions` | createSubmission |
| `GET` | `/api/signing/v1/submissions/{id}` | getSubmission |
| `DELETE` | `/api/signing/v1/submissions/{id}` | deleteSubmission |
| `POST` | `/api/signing/v1/submissions/{id}/send` | sendSubmission |
| `POST` | `/api/signing/v1/submissions/{id}/cancel` | cancelSubmission |
| `PUT` | `/api/signing/v1/submissions/{id}/signers/{sid}` | replaceSigner |
| `POST` | `/api/signing/v1/submissions/{id}/signers/{sid}/resend` | resendInvitation |
| `GET` | `/api/signing/v1/submissions/{id}/events` | listSubmissionEvents |
| `GET` | `/api/signing/v1/submissions/{id}/document` | downloadSubmissionDocument |
| `GET` | `/api/signing/v1/submissions/{id}/audit-trail` | downloadAuditTrail |
| `GET` | `/api/signing/v1/submissions/{id}/package` | downloadPackage |
| `GET` | `/api/signing/v1/inbox` | inbox |
| `GET` | `/api/signing/v1/signing/{signer_id}` | getSession |
| `GET` | `/api/signing/v1/signing/{signer_id}/document` | downloadSessionDocument |
| `POST` | `/api/signing/v1/signing/{signer_id}/open` | openSession |
| `POST` | `/api/signing/v1/signing/{signer_id}/sign` | sign |
| `POST` | `/api/signing/v1/signing/{signer_id}/decline` | decline |
| `POST` | `/api/signing/v1/signing/{signer_id}/qes/prepare` | prepareQES |
| `POST` | `/api/signing/v1/signing/{signer_id}/qes/complete` | completeQES |
| `GET` | `/api/signing/v1/me/certificate` | getMyCertificate |
| `POST` | `/api/signing/v1/me/certificate` | setupMyCertificate |
| `POST` | `/api/signing/v1/me/certificate/pin` | changeMyPin |
| `POST` | `/api/signing/v1/me/certificate/renew` | renewMyCertificate |
| `POST` | `/api/signing/v1/me/certificate/revoke` | revokeMyCertificate |
| `GET` | `/api/signing/v1/certificates` | listCertificates |
| `POST` | `/api/signing/v1/certificates` | createAdminCertificate |
| `GET` | `/api/signing/v1/certificates/{id}` | getCertificate |
| `POST` | `/api/signing/v1/certificates/{id}/revoke` | revokeCertificate |
| `GET` | `/api/signing/v1/ca/crl` | downloadCRL |
| `POST` | `/api/signing/v1/documents/sign` | signDocument |
| `GET` | `/api/signing/v1/documents/{id}` | downloadSignedDocument |
| `POST` | `/api/signing/v1/verify` | verifyDocument |
| `GET` | `/api/signing/v1/stream` | streamEvents |
| `GET` | `/api/signing/v1/users` | listMembers |
| `POST` | `/api/signing/v1/backup/export` | exportBackup |
| `POST` | `/api/signing/v1/backup/import` | importBackup |

[OpenAPI: api/openapi/signing.yaml](https://github.com/go-tangra/go-tangra-signing/blob/041fcb91357fc68d5d736a2bc16450a1199254dd/api/openapi/signing.yaml)

## Detailed source references

- [README.md](sources/signing/README.html) — captured at `041fcb91357f`.
- [deploy/README.md](sources/signing/deploy/README.html) — captured at `041fcb91357f`.

## Limits, diagnostics and recovery

Configure S3 storage, KEK and the tenant signing CA lifecycle. Expiry/reminder tasks depend on Scheduler integration; a source build alone does not enable them. Qualified signatures require the user's B-Trust BISS/card environment.

Use the module's operations/deployment reference for retention, backup/restore, refusal behavior, interface examples and feature limitations. The installation guides cover common readiness, identity, registration and storage failures.

## Upstream overview: go-tangra-signing (v4)

Document signing module of the go-tangra v4 platform (feature 027), the v4
successor of the v3 DocuSeal-style signing service: PDF templates with a
field builder, submissions signed by platform users in order or in parallel,
personal PIN-protected signing certificates issued by a per-tenant signing
CA, qualified signatures with a smart card through B-Trust BISS, and an
audit trail for every completed document.

- **Templates** — upload a PDF (bounded parsing), place fields in the
  builder (text, number, date, checkbox, select, radio, cells, image, file,
  signature, initials, stamp) per party, detect placeholders, folders and
  tags, conditions (show/require) and number formulas.
- **Submissions** — one active member per party, sequential or parallel, a
  frozen copy of the fields and the PDF, prefills, expiry and reminders
  (scheduler task types), cancel/resend/replace/delete by the sender, live
  "To sign" inbox, e-mails through the notification module.
- **Signing** — the signer sees only their own fields; values are stamped as
  an incremental update and a PAdES signature (signer certificate + tenant
  CA) is applied with the visible appearance on the first signature field, so
  every earlier signature stays valid. Parallel signers are serialised by a
  row lock. A wrong PIN signs nothing and counts towards a lockout.
- **Qualified signatures** — prepare/complete through BISS on the signer's
  computer; the card signature is verified against the prepared digest and the
  stored chain before it is spliced in.
- **Certificates** — per-tenant CA (sealed with the module KEK, renewed before
  expiry), personal certificates (PIN-encrypted keys), administrator
  certificates, revocation and CRLs, administrator document signing with an
  optional RFC 3161 time-stamp (credentials in Warden).
- **Verification, audit trail, backup** — verify any PDF against the tenant
  CAs and configured qualified roots; an audit-trail PDF certified with the
  tenant system certificate for every completed submission; tenant export and
  import with key handling that never exposes keys.

## Layout

```
cmd/signingsvc            binary (serve | bootstrap | version)
api/openapi               browser API contract (OpenAPI 3.1)
internal/                 config, authz, audit, sealed, blob, store, repo (+repodb, memstore),
                          pdf/{limits,detect,render,incr,overlay,sign,verify,audittrail,fonts},
                          pincrypto, pki, certs, contacts, templates, submissions, signing,
                          qes, rules, fieldvalues, documents, jobs, tasks, backup, mail,
                          warden, events, stream, metrics, httpapi, app
pkg/signingmanifest       gateway manifest, permissions, module roles, abilities, nav
ui/                       federated UI remote (Vue 3, @go-tangra/ui, pdf.js)
tests/integration         whole-service suites on TimescaleDB (isolation, leaks, concurrency)
deploy/                   policy.yaml, container.yaml (stack-shaped example), README.md
specs/027-signing-v4      specification, plan, research, data model, contracts, tasks
```

## Development

```bash
unset GOROOT; export GOWORK=off
make test                 # unit + contract tests (race)
make cover                # ≥ 80 % overall; 100 % authz, pincrypto, rules, qes, pdf/limits
make lint vuln            # vet, staticcheck, gosec; govulncheck
make fuzz                 # every fuzz target for FUZZTIME
sg docker -c 'make test-integration'   # TimescaleDB via testcontainers
(cd ui && npm ci && npm run lint && npx vitest run)
make build                # bin/signingsvc (no UI); make build-ui embeds the remote
```

Permissions: `signing:sign` (every tenant member; relationship checks in
code), `signing:read`, `templates:manage`, `submissions:create`,
`submissions:manage`, `certificates:manage`, `backup:manage`; module roles
Signing administrator / operator / sender / viewer. Deployment: see
[deploy/README.md](sources/signing/deploy/README.html). Security: see [SECURITY.md](https://github.com/go-tangra/go-tangra-signing/blob/041fcb91357fc68d5d736a2bc16450a1199254dd/SECURITY.md).
