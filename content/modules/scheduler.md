# Scheduler

Typed tenant and platform jobs, cron scheduling, retries and history.

**Architecture role**: Platform services. [See the complete component map](architecture/index.html).

**Documented source**: `b8746bfeea0a` · nearest local service tag `v4.1.2` · v4 major. [Repository at this revision](https://github.com/go-tangra/go-tangra-scheduler/tree/b8746bfeea0a54b6b3d0b937ea9d557148323b9e). Tags are source metadata, not a claim of image publication or cross-module compatibility.


## Permissions and authorization

This catalogue contains **5 permissions** declared by the [module manifest](https://github.com/go-tangra/go-tangra-scheduler/blob/b8746bfeea0a54b6b3d0b937ea9d557148323b9e/pkg/schedulermanifest/manifest.go) at the revision above. Custom-role references use `module:resource:action`; the manifest and API contract use the local `resource:action` form. The action names are distinct grants: do not assume `manage` automatically includes `read` or another action.

Module permissions gate actions within the authenticated tenant. The endpoint still enforces its resource and workflow checks; a UI ability describes presentation and does not replace server authorization.

[How to assign and verify permissions](architecture/security.html#assign-and-verify-permissions). Module roles and built-in grant mappings are defined in the linked manifest; review those mappings before assigning a broad role.

| Qualified permission | What it allows |
| --- | --- |
| `scheduler:scheduler:read` | List task types, tasks, execution history and the overview, preview cron schedules and follow the live stream |
| `scheduler:tasks:manage` | Create and edit scheduled tasks, enable or disable them, and retire a removed module's task types (platform administrators) |
| `scheduler:tasks:delete` | Delete scheduled tasks |
| `scheduler:tasks:control` | Start, stop, restart, run now, run again and cancel tasks, including bulk actions |
| `scheduler:backup:manage` | Export and import scheduler tasks and history |

### scheduler:scheduler:read

List task types, tasks, execution history and the overview, preview cron schedules and follow the live stream.

**UI actions**: `read` on `SchedulerTask`, `SchedulerExecution`, `SchedulerOverview`, `SchedulerTaskType`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Scheduler, Dashboard.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/scheduler/v1/task-types` | listTaskTypes |
| `GET` | `/api/scheduler/v1/cron/preview` | previewCron |
| `GET` | `/api/scheduler/v1/tasks` | listTasks |
| `GET` | `/api/scheduler/v1/tasks/{id}` | getTask |
| `GET` | `/api/scheduler/v1/executions` | listExecutions |
| `GET` | `/api/scheduler/v1/executions/{id}` | getExecution |
| `GET` | `/api/scheduler/v1/overview` | overview |
| `GET` | `/api/scheduler/v1/stream` | streamEvents |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### scheduler:tasks:manage

Create and edit scheduled tasks, enable or disable them, and retire a removed module's task types (platform administrators).

**UI actions**: `create`, `update` on `SchedulerTask`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/scheduler/v1/modules/{module}/unregister` | retireModule |
| `POST` | `/api/scheduler/v1/tasks` | createTask |
| `PUT` | `/api/scheduler/v1/tasks/{id}` | updateTask |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### scheduler:tasks:delete

Delete scheduled tasks.

**UI actions**: `delete` on `SchedulerTask`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `DELETE` | `/api/scheduler/v1/tasks/{id}` | deleteTask |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### scheduler:tasks:control

Start, stop, restart, run now, run again and cancel tasks, including bulk actions.

**UI actions**: `control` on `SchedulerTask`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/scheduler/v1/tasks/{id}/start` | startTask |
| `POST` | `/api/scheduler/v1/tasks/{id}/stop` | stopTask |
| `POST` | `/api/scheduler/v1/tasks/{id}/restart` | restartTask |
| `POST` | `/api/scheduler/v1/tasks/{id}/run` | runTask |
| `POST` | `/api/scheduler/v1/tasks/{id}/cancel` | cancelTask |
| `POST` | `/api/scheduler/v1/tasks/bulk/{action}` | bulkControl |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### scheduler:backup:manage

Export and import scheduler tasks and history.

**UI actions**: `manage` on `SchedulerBackup`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/scheduler/v1/backup/export` | exportBackup |
| `POST` | `/api/scheduler/v1/backup/import` | importBackup |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.
<div class="guide-actions"><a href="how-to/scheduler/docker.html">Install with Docker Compose →</a><a href="how-to/scheduler/native.html">Install without Docker →</a><a href="downloads/scheduler.zip">Download Compose bundle ↓</a></div>

## Dependencies and integration

**Required**: TimescaleDB, Valkey, Auth, Portal, mesh identity.

**Optional or feature-dependent**: task-executing modules.

This module is absent from the recorded base platform Compose file. Create its `scheduler_app` role with LOGIN and NOBYPASSRLS before migrations; migrations grant to that existing role. No KEK is required. Configure both task-registration and executor policies.

The list describes infrastructure/features, not every transitive library. Check the linked deployment reference for exact versions, enabled features and peer grants. [Framework dependencies](architecture/dependencies.html) cover the shared Go libraries.

## Runtime and operation

| Item | Reference |
| --- | --- |
| Service binary | `schedulersvc` |
| Public example configuration | `deploy/container.yaml`; adapt endpoints and paths for your environment |
| Native source build | Go `1.26.3`, toolchain `go1.26.8`, Node 22 for UI |
| Image repository | `ghcr.io/go-tangra/go-tangra-scheduler`; choose a published compatible version |
| Private admin default | `127.0.0.1:9800`; check actual configuration |
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
| `Config` | `engine` | `Engine` |
| `Config` | `limits_scheduler` | `Limits` |
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
| `Engine` | `tick_ms` | `int` |
| `Engine` | `workers` | `int` |
| `Engine` | `batch` | `int` |
| `Engine` | `misfire_grace_seconds` | `int` |
| `Engine` | `lease_grace_seconds` | `int` |
| `Engine` | `retention_days` | `int` |
| `Engine` | `retention_interval_minutes` | `int` |
| `Engine` | `instance_id` | `string` |
| `Limits` | `max_payload_bytes` | `int` |
| `Limits` | `max_result_bytes` | `int` |
| `Limits` | `max_timeout_seconds` | `int` |
| `Limits` | `min_interval_seconds` | `int` |
| `Limits` | `max_page_size` | `int` |
| `Limits` | `max_backup_bytes` | `int64` |
| `Limits` | `max_tasks_per_tenant` | `int` |

[Configuration structures and validation](https://github.com/go-tangra/go-tangra-scheduler/blob/b8746bfeea0a54b6b3d0b937ea9d557148323b9e/internal/config/config.go)

## API operation index

These operations are extracted from the module's OpenAPI contract. Read the source contract for request/response schemas, permission checks and exact route bases; internal mesh endpoints must not be treated as anonymous public APIs.

| Method | Contract path | Operation |
| --- | --- | --- |
| `GET` | `/api/scheduler/v1/health` | health |
| `GET` | `/api/scheduler/v1/task-types` | listTaskTypes |
| `POST` | `/api/scheduler/v1/modules/{module}/unregister` | retireModule |
| `GET` | `/api/scheduler/v1/cron/preview` | previewCron |
| `GET` | `/api/scheduler/v1/tasks` | listTasks |
| `POST` | `/api/scheduler/v1/tasks` | createTask |
| `GET` | `/api/scheduler/v1/tasks/{id}` | getTask |
| `PUT` | `/api/scheduler/v1/tasks/{id}` | updateTask |
| `DELETE` | `/api/scheduler/v1/tasks/{id}` | deleteTask |
| `POST` | `/api/scheduler/v1/tasks/{id}/start` | startTask |
| `POST` | `/api/scheduler/v1/tasks/{id}/stop` | stopTask |
| `POST` | `/api/scheduler/v1/tasks/{id}/restart` | restartTask |
| `POST` | `/api/scheduler/v1/tasks/{id}/run` | runTask |
| `POST` | `/api/scheduler/v1/tasks/{id}/cancel` | cancelTask |
| `POST` | `/api/scheduler/v1/tasks/bulk/{action}` | bulkControl |
| `GET` | `/api/scheduler/v1/executions` | listExecutions |
| `GET` | `/api/scheduler/v1/executions/{id}` | getExecution |
| `GET` | `/api/scheduler/v1/overview` | overview |
| `GET` | `/api/scheduler/v1/stream` | streamEvents |
| `POST` | `/api/scheduler/v1/backup/export` | exportBackup |
| `POST` | `/api/scheduler/v1/backup/import` | importBackup |

[OpenAPI: api/openapi/scheduler.yaml](https://github.com/go-tangra/go-tangra-scheduler/blob/b8746bfeea0a54b6b3d0b937ea9d557148323b9e/api/openapi/scheduler.yaml)

## Detailed source references

- [README.md](sources/scheduler/README.html) — captured at `b8746bfeea0a`.
- [deploy/README.md](sources/scheduler/deploy/README.html) — captured at `b8746bfeea0a`.

## Limits, diagnostics and recovery

This module is absent from the recorded base platform Compose file. Create its `scheduler_app` role with LOGIN and NOBYPASSRLS before migrations; migrations grant to that existing role. No KEK is required. Configure both task-registration and executor policies.

Use the module's operations/deployment reference for retention, backup/restore, refusal behavior, interface examples and feature limitations. The installation guides cover common readiness, identity, registration and storage failures.

## Upstream overview: go-tangra-scheduler (v4)

Central, UI-driven job scheduler of the go-tangra v4 platform (feature 026).
It decides **when** work runs and asks the module that owns the work to run
it over the SPIFFE mTLS mesh.

- **Task types** are registered by modules (`scheduler.v1.Registration`). The
  owner is the caller's verified SPIFFE identity; every name is
  `<module>:<action>`. Types carry a JSON Schema for their payload, a suggested
  cron expression, a default retry count and a scope (tenant or platform).
- **Tasks** belong to a tenant (platform-scoped types: platform administrators
  only). Kinds: `periodic` (5-field cron with an IANA time zone, DST-safe),
  `delayed` (once, at a time or after a delay) and `wait_result` (once, now;
  the UI follows the run live). Payloads are validated against the type's
  schema at save time and again before every run.
- **Execution** calls `scheduler.v1.TaskExecutor/ExecuteTask` on the owning
  module with the task timeout. Retryable failures back off 30 s × 2^(n-1)
  (capped at 10 min); permanent failures stop. Every attempt is recorded with
  status, message and result; tasks show their last run and next run.
- **Exactly once across replicas**: PostgreSQL row locks (`SKIP LOCKED`),
  leases with fencing and a unique occurrence index. Missed occurrences during
  downtime are counted, with at most one catch-up run when the task allows it.
- **Control**: start/stop/restart periodic tasks, run now / run again, cancel
  one-shot tasks, bulk actions scoped to the caller.
- **Overview, metrics, audit, backup**: US6 overview; OTel metrics on the
  admin listener; closed-vocabulary audit that never records payload values;
  export/import of tasks, history and types.

## Layout

```
cmd/schedulersvc          binary (serve | bootstrap | version)
api/openapi               browser API contract (OpenAPI 3.1)
sdk/                      nested module …/sdk/v4: scheduler.v1 proto, taskexec, schedulerclient
internal/                 config, authz, audit, cron, payload, registry, tasks, engine,
                          dispatch, backup, metrics, events, stream, store, repo, httpapi, grpcapi, app
pkg/schedulermanifest     gateway manifest, permissions, module roles, abilities, nav
ui/                       federated UI remote (Vue 3, @go-tangra/ui)
deploy/                   policy.yaml, container.yaml (stack-shaped example), README.md
specs/026-scheduler-v4    specification, plan, research, data model, contracts, tasks
```

## Development

```bash
unset GOROOT; export GOWORK=off
make test                 # unit + contract tests (race)
make cover                # ≥ 80 % overall; 100 % authz, cron, payload, registry
make lint vuln            # vet, staticcheck, gosec; govulncheck (service + sdk)
sg docker -c 'make test-integration'   # TimescaleDB via testcontainers
(cd sdk && buf lint && go test -race ./...)
make build                # bin/schedulersvc (no UI); make build-ui embeds the remote
```

Permissions: `scheduler:read`, `tasks:manage`, `tasks:delete`,
`tasks:control`, `backup:manage`; module roles Scheduler administrator /
operator / viewer. Deployment: see [deploy/README.md](sources/scheduler/deploy/README.html).
Security: see [SECURITY.md](https://github.com/go-tangra/go-tangra-scheduler/blob/b8746bfeea0a54b6b3d0b937ea9d557148323b9e/SECURITY.md).
