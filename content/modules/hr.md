# HR

Leave requests, allowances, team calendars and signing integration.

**Architecture role**: Business modules. [See the complete component map](architecture/index.html).

**Documented source**: `d1aab9d2cde3` · nearest local service tag `v4.1.2` · v4 major. [Repository at this revision](https://github.com/go-tangra/go-tangra-hr/tree/d1aab9d2cde331d0b59527a418df249e5068ddea). Tags are source metadata, not a claim of image publication or cross-module compatibility.


## Permissions and authorization

This catalogue contains **4 permissions** declared by the [module manifest](https://github.com/go-tangra/go-tangra-hr/blob/d1aab9d2cde331d0b59527a418df249e5068ddea/pkg/hrmanifest/manifest.go) at the revision above. Custom-role references use `module:resource:action`; the manifest and API contract use the local `resource:action` form. The action names are distinct grants: do not assume `manage` automatically includes `read` or another action.

Permissions distinguish team-calendar visibility, personal requests and HR administration. Request-review workflow rules still apply: nobody reviews their own request. Signing-required requests also depend on the configured Signing workflow.

[How to assign and verify permissions](architecture/security.html#assign-and-verify-permissions). Module roles and built-in grant mappings are defined in the linked manifest; review those mappings before assigning a broad role.

| Qualified permission | What it allows |
| --- | --- |
| `hr:hr:calendar` | See the team calendar: who is absent when, with the absence type |
| `hr:hr:request` | Request leave for myself, see my requests and my balance (managers also approve for their departments) |
| `hr:hr:read` | Read every leave request, balance, allowance, absence type, department and holiday of the tenant |
| `hr:hr:manage` | Manage absence types, pools, allowances, departments and holidays, act for anyone, run carry-over and backups |

### hr:hr:calendar

See the team calendar: who is absent when, with the absence type.

**UI actions**: `read` on `HrCalendar`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Leave calendar.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/hr/v1/me` | me |
| `GET` | `/api/hr/v1/people` | listPeople |
| `GET` | `/api/hr/v1/calendar` | calendar |
| `GET` | `/api/hr/v1/absence-types` | listAbsenceTypes |
| `GET` | `/api/hr/v1/absence-types/{id}` | getAbsenceType |
| `GET` | `/api/hr/v1/allowances` | listAllowances |
| `GET` | `/api/hr/v1/allowances/{id}` | getAllowance |
| `GET` | `/api/hr/v1/balance/{user_id}` | getBalance |
| `GET` | `/api/hr/v1/requests` | listRequests |
| `GET` | `/api/hr/v1/requests/{id}` | getRequest |
| `POST` | `/api/hr/v1/requests/{id}/approve` | approveRequest |
| `POST` | `/api/hr/v1/requests/{id}/reject` | rejectRequest |
| `POST` | `/api/hr/v1/requests/{id}/revoke` | revokeRequest |
| `GET` | `/api/hr/v1/requests/{id}/signed-document` | downloadSignedDocument |
| `GET` | `/api/hr/v1/departments` | listDepartments |
| `GET` | `/api/hr/v1/holidays` | listHolidays |
| `GET` | `/api/hr/v1/stream` | streamEvents |

**Scope and additional checks**: Permissions distinguish team-calendar visibility, personal requests and HR administration. Request-review workflow rules still apply: nobody reviews their own request. Signing-required requests also depend on the configured Signing workflow.

### hr:hr:request

Request leave for myself, see my requests and my balance (managers also approve for their departments).

**UI actions**: `create`, `read` on `HrRequest`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: My leave, To review.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/hr/v1/requests` | createRequest |
| `POST` | `/api/hr/v1/requests/preview` | previewRequest |
| `PUT` | `/api/hr/v1/requests/{id}` | updateRequest |
| `DELETE` | `/api/hr/v1/requests/{id}` | deleteRequest |
| `POST` | `/api/hr/v1/requests/{id}/cancel` | cancelRequest |

**Scope and additional checks**: Permissions distinguish team-calendar visibility, personal requests and HR administration. Request-review workflow rules still apply: nobody reviews their own request. Signing-required requests also depend on the configured Signing workflow.

### hr:hr:read

Read every leave request, balance, allowance, absence type, department and holiday of the tenant.

**UI actions**: `read` on `HrRequest`, `HrAllowance`, `HrAbsenceType`, `HrDepartment`, `HrStats`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Allowances, Absence types, Departments, Holidays, HR statistics.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/hr/v1/pools` | listPools |
| `GET` | `/api/hr/v1/pools/{id}` | getPool |
| `GET` | `/api/hr/v1/stats` | stats |

**Scope and additional checks**: Permissions distinguish team-calendar visibility, personal requests and HR administration. Request-review workflow rules still apply: nobody reviews their own request. Signing-required requests also depend on the configured Signing workflow.

### hr:hr:manage

Manage absence types, pools, allowances, departments and holidays, act for anyone, run carry-over and backups.

**UI actions**: `manage` on `HrRequest`, `HrAllowance`, `HrAbsenceType`, `HrDepartment`, `HrHoliday`, `HrBackup`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/hr/v1/absence-types` | createAbsenceType |
| `PUT` | `/api/hr/v1/absence-types/{id}` | updateAbsenceType |
| `DELETE` | `/api/hr/v1/absence-types/{id}` | deleteAbsenceType |
| `GET` | `/api/hr/v1/absence-types/{id}/signing-check` | checkAbsenceTypeSigning |
| `GET` | `/api/hr/v1/signing/templates` | listSigningTemplates |
| `POST` | `/api/hr/v1/pools` | createPool |
| `PUT` | `/api/hr/v1/pools/{id}` | updatePool |
| `DELETE` | `/api/hr/v1/pools/{id}` | deletePool |
| `POST` | `/api/hr/v1/allowances` | createAllowance |
| `PUT` | `/api/hr/v1/allowances/{id}` | updateAllowance |
| `DELETE` | `/api/hr/v1/allowances/{id}` | deleteAllowance |
| `POST` | `/api/hr/v1/carry-over/preview` | previewCarryOver |
| `POST` | `/api/hr/v1/carry-over` | runCarryOver |
| `POST` | `/api/hr/v1/departments` | createDepartment |
| `PUT` | `/api/hr/v1/departments/{id}` | updateDepartment |
| `DELETE` | `/api/hr/v1/departments/{id}` | deleteDepartment |
| `PUT` | `/api/hr/v1/departments/{id}/members` | setDepartmentMembers |
| `POST` | `/api/hr/v1/holidays` | createHoliday |
| `PUT` | `/api/hr/v1/holidays/{id}` | updateHoliday |
| `DELETE` | `/api/hr/v1/holidays/{id}` | deleteHoliday |
| `POST` | `/api/hr/v1/holidays/import` | importHolidays |
| `POST` | `/api/hr/v1/backup/export` | exportBackup |
| `POST` | `/api/hr/v1/backup/import` | importBackup |

**Scope and additional checks**: Permissions distinguish team-calendar visibility, personal requests and HR administration. Request-review workflow rules still apply: nobody reviews their own request. Signing-required requests also depend on the configured Signing workflow.
<div class="guide-actions"><a href="how-to/hr/docker.html">Install with Docker Compose →</a><a href="how-to/hr/native.html">Install without Docker →</a><a href="downloads/hr.zip">Download Compose bundle ↓</a></div>

## Dependencies and integration

**Required**: TimescaleDB, Valkey, Auth, Portal, mesh identity.

**Optional or feature-dependent**: Signing, Scheduler, Notification.

The image is `go-tangra-hr` although the local checkout is `hr-service-v4`. Signing-required absence types depend on compatible Signing templates, event consumers and reconciliation; configure Notification and Scheduler where used.

The list describes infrastructure/features, not every transitive library. Check the linked deployment reference for exact versions, enabled features and peer grants. [Framework dependencies](architecture/dependencies.html) cover the shared Go libraries.

## Runtime and operation

| Item | Reference |
| --- | --- |
| Service binary | `hrsvc` |
| Public example configuration | `deploy/container.yaml`; adapt endpoints and paths for your environment |
| Native source build | Go `1.26.3`, toolchain `go1.26.8`, Node 22 for UI |
| Image repository | `ghcr.io/go-tangra/go-tangra-hr`; choose a published compatible version |
| Private admin default | `127.0.0.1:9870`; check actual configuration |
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
| `Config` | `auth` | `Service` |
| `Config` | `notification` | `Service` |
| `Config` | `signing` | `Service` |
| `Config` | `task_scheduler` | `TaskScheduler` |
| `Config` | `links` | `Links` |
| `Config` | `limits_hr` | `Limits` |
| `Config` | `consumer` | `Consumer` |
| `Config` | `reconcile` | `Reconcile` |
| `Config` | `outbox` | `Outbox` |
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
| `Service` | `service` | `string` |
| `TaskScheduler` | `enabled` | `bool` |
| `TaskScheduler` | `service` | `string` |
| `Links` | `portal_base_url` | `string` |
| `Limits` | `max_page_size` | `int` |
| `Limits` | `max_calendar_days` | `int` |
| `Limits` | `max_request_days` | `int` |
| `Limits` | `max_import_bytes` | `int64` |
| `Limits` | `max_import_lines` | `int` |
| `Limits` | `max_backup_bytes` | `int64` |
| `Limits` | `max_department_depth` | `int` |
| `Consumer` | `enabled` | `bool` |
| `Consumer` | `block_ms` | `int` |
| `Consumer` | `batch` | `int` |
| `Consumer` | `tenants_refresh_seconds` | `int` |
| `Reconcile` | `older_than_minutes` | `int` |
| `Outbox` | `interval_ms` | `int` |
| `Outbox` | `batch` | `int` |
| `Outbox` | `max_attempts` | `int` |

[Configuration structures and validation](https://github.com/go-tangra/go-tangra-hr/blob/d1aab9d2cde331d0b59527a418df249e5068ddea/internal/config/config.go)

## API operation index

These operations are extracted from the module's OpenAPI contract. Read the source contract for request/response schemas, permission checks and exact route bases; internal mesh endpoints must not be treated as anonymous public APIs.

| Method | Contract path | Operation |
| --- | --- | --- |
| `GET` | `/api/hr/v1/health` | health |
| `GET` | `/api/hr/v1/me` | me |
| `GET` | `/api/hr/v1/people` | listPeople |
| `GET` | `/api/hr/v1/calendar` | calendar |
| `GET` | `/api/hr/v1/absence-types` | listAbsenceTypes |
| `POST` | `/api/hr/v1/absence-types` | createAbsenceType |
| `GET` | `/api/hr/v1/absence-types/{id}` | getAbsenceType |
| `PUT` | `/api/hr/v1/absence-types/{id}` | updateAbsenceType |
| `DELETE` | `/api/hr/v1/absence-types/{id}` | deleteAbsenceType |
| `GET` | `/api/hr/v1/absence-types/{id}/signing-check` | checkAbsenceTypeSigning |
| `GET` | `/api/hr/v1/signing/templates` | listSigningTemplates |
| `GET` | `/api/hr/v1/pools` | listPools |
| `POST` | `/api/hr/v1/pools` | createPool |
| `GET` | `/api/hr/v1/pools/{id}` | getPool |
| `PUT` | `/api/hr/v1/pools/{id}` | updatePool |
| `DELETE` | `/api/hr/v1/pools/{id}` | deletePool |
| `GET` | `/api/hr/v1/allowances` | listAllowances |
| `POST` | `/api/hr/v1/allowances` | createAllowance |
| `GET` | `/api/hr/v1/allowances/{id}` | getAllowance |
| `PUT` | `/api/hr/v1/allowances/{id}` | updateAllowance |
| `DELETE` | `/api/hr/v1/allowances/{id}` | deleteAllowance |
| `GET` | `/api/hr/v1/balance/{user_id}` | getBalance |
| `POST` | `/api/hr/v1/carry-over/preview` | previewCarryOver |
| `POST` | `/api/hr/v1/carry-over` | runCarryOver |
| `GET` | `/api/hr/v1/requests` | listRequests |
| `POST` | `/api/hr/v1/requests` | createRequest |
| `POST` | `/api/hr/v1/requests/preview` | previewRequest |
| `GET` | `/api/hr/v1/requests/{id}` | getRequest |
| `PUT` | `/api/hr/v1/requests/{id}` | updateRequest |
| `DELETE` | `/api/hr/v1/requests/{id}` | deleteRequest |
| `POST` | `/api/hr/v1/requests/{id}/approve` | approveRequest |
| `POST` | `/api/hr/v1/requests/{id}/reject` | rejectRequest |
| `POST` | `/api/hr/v1/requests/{id}/revoke` | revokeRequest |
| `POST` | `/api/hr/v1/requests/{id}/cancel` | cancelRequest |
| `GET` | `/api/hr/v1/requests/{id}/signed-document` | downloadSignedDocument |
| `GET` | `/api/hr/v1/departments` | listDepartments |
| `POST` | `/api/hr/v1/departments` | createDepartment |
| `PUT` | `/api/hr/v1/departments/{id}` | updateDepartment |
| `DELETE` | `/api/hr/v1/departments/{id}` | deleteDepartment |
| `PUT` | `/api/hr/v1/departments/{id}/members` | setDepartmentMembers |
| `GET` | `/api/hr/v1/holidays` | listHolidays |
| `POST` | `/api/hr/v1/holidays` | createHoliday |
| `PUT` | `/api/hr/v1/holidays/{id}` | updateHoliday |
| `DELETE` | `/api/hr/v1/holidays/{id}` | deleteHoliday |
| `POST` | `/api/hr/v1/holidays/import` | importHolidays |
| `GET` | `/api/hr/v1/stats` | stats |
| `GET` | `/api/hr/v1/stream` | streamEvents |
| `POST` | `/api/hr/v1/backup/export` | exportBackup |
| `POST` | `/api/hr/v1/backup/import` | importBackup |

[OpenAPI: api/openapi/hr.yaml](https://github.com/go-tangra/go-tangra-hr/blob/d1aab9d2cde331d0b59527a418df249e5068ddea/api/openapi/hr.yaml)

## Detailed source references

- [README.md](sources/hr/README.html) — captured at `d1aab9d2cde3`.
- [deploy/README.md](sources/hr/deploy/README.html) — captured at `d1aab9d2cde3`.

## Limits, diagnostics and recovery

The image is `go-tangra-hr` although the local checkout is `hr-service-v4`. Signing-required absence types depend on compatible Signing templates, event consumers and reconciliation; configure Notification and Scheduler where used.

Use the module's operations/deployment reference for retention, backup/restore, refusal behavior, interface examples and feature limitations. The installation guides cover common readiness, identity, registration and storage failures.

## Upstream overview: go-tangra-hr (v4)

Leave management module of the go-tangra v4 platform (feature 028), the v4
successor of the v3 hr-service: absence types and pools, yearly allowances
with year-end carry-over, leave requests approved by the requester's manager,
departments, public holidays and a team calendar. Absence types can require a
signed leave form: approval then starts a submission in the signing module
and the request is approved only when everyone has signed.

- **Absence types and pools** — colour, icon, whether days are deducted and
  whether approval is needed, a shared pool of days, a carry-over cap, and for
  signing-required types a signing template with party and field mappings
  (validated against the template in the signing module).
- **Allowances** — days per person, year and type or pool; the balance shows
  total, carried over, used, pending and remaining. Carry-over moves unused
  days (up to the cap) into the next year; it can be previewed, is idempotent
  and also runs as the tenant task `hr:carry-over`.
- **Requests** — whole and half days, weekends and holidays not counted,
  overlaps refused, days charged per calendar year (a request across New
  Year uses both years' allowances). Requests go to the manager of the
  requester's department (the parent department's manager for managers, HR
  administrators when there is none); nobody reviews their own request.
  Approve, reject and revoke (days refunded) with notes and e-mails.
- **Signing** — for signing-required types, approval starts a submission
  through the signing module API (idempotent, source `hr`) and the request
  waits in `awaiting_signing`. Completion approves and charges the days;
  declined, cancelled or expired submissions put the request back to pending
  with the outcome shown. Outcomes arrive on the platform event stream (cursor
  persisted per tenant) and a platform task reconciles anything missed.
- **Calendar, statistics, backup** — week/two-week/month team calendar with
  holidays, live updates over SSE, statistics, tenant export and import.

## Layout

```
cmd/hrsvc                 binary (serve | bootstrap | version)
api/openapi               browser API contract (OpenAPI 3.1)
internal/                 config, authz, audit, apperr, leavedays, routing, charges,
                          store, repo (+repodb, memstore, repotest), catalog, people,
                          departments, allowances, requests, signingmap, signing,
                          events, consumer, outbox, tasks, backup, stream, httpapi, app
pkg/hrmanifest            gateway manifest, permissions, module roles, abilities, nav
ui/                       federated UI remote (Vue 3, @go-tangra/ui)
deploy/                   policy.yaml, container.yaml (stack-shaped example), README.md
specs/028-hr-v4           specification, plan, research, data model, contracts, tasks
```

## Development

```bash
unset GOROOT; export GOWORK=off
make test                 # unit + contract tests (race)
make cover                # ≥ 80 % overall; 100 % authz, routing, leavedays, charges, signingmap
make lint vuln            # vet, staticcheck, gosec; govulncheck
make fuzz                 # every fuzz target for FUZZTIME
sg docker -c 'make test-integration'   # TimescaleDB via testcontainers
(cd ui && npm ci && npm run lint && npx vitest run)
make build                # bin/hrsvc (no UI); make build-ui embeds the remote
```

Permissions: `hr:calendar` (see the team calendar), `hr:request` (own
requests; managers review their departments' requests — relationship checks
in code), `hr:read` (all HR data of the tenant), `hr:manage` (configure types,
allowances, departments, holidays; review any request; backup). Module roles
HR administrator / viewer / employee / calendar viewer; tenant owners and
admins get the administrator role, operators and members the employee role,
auditors the viewer role. Deployment: see [deploy/README.md](sources/hr/deploy/README.html).
Security: see [SECURITY.md](https://github.com/go-tangra/go-tangra-hr/blob/d1aab9d2cde331d0b59527a418df249e5068ddea/SECURITY.md).
