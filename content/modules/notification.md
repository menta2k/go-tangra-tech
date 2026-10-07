# Notification

Central SMTP notifications, inbox messages and delivery management.

**Architecture role**: Platform services. [See the complete component map](architecture/index.html).

**Documented source**: `84f73a432d9b` · nearest local service tag `v4.8.3` · v4 major. [Repository at this revision](https://github.com/go-tangra/go-tangra-notification/tree/84f73a432d9bd0e493524a972d253067dd5a812d). Tags are source metadata, not a claim of image publication or cross-module compatibility.


## Permissions and authorization

This catalogue contains **13 permissions** declared by the [module manifest](https://github.com/go-tangra/go-tangra-notification/blob/84f73a432d9bd0e493524a972d253067dd5a812d/pkg/notificationmanifest/manifest.go) at the revision above. Custom-role references use `module:resource:action`; the manifest and API contract use the local `resource:action` form. The action names are distinct grants: do not assume `manage` automatically includes `read` or another action.

Channel and template resource grants still apply on top of module roles; sending requires the relevant use access. The administrator module role excludes events:publish, which is a module capability; owner/admin built-in grants retain it. Reading channel settings returns redacted settings.

[How to assign and verify permissions](architecture/security.html#assign-and-verify-permissions). Module roles and built-in grant mappings are defined in the linked manifest; review those mappings before assigning a broad role.

| Qualified permission | What it allows |
| --- | --- |
| `notification:channels:read` | List and read notification channels the caller is granted (settings redacted) |
| `notification:channels:manage` | Create, change, test and delete channels the caller is granted |
| `notification:templates:read` | List, read and preview templates the caller is granted |
| `notification:templates:manage` | Create, change and delete templates the caller is granted |
| `notification:notifications:send` | Send notifications through templates and channels the caller may use |
| `notification:notifications:read` | Read the notification log (own sends without stats:read) |
| `notification:messages:read` | List message categories and messages |
| `notification:messages:manage` | Create, send, revoke and archive internal messages; manage categories |
| `notification:inbox:read` | Read and manage the caller's own inbox and live stream |
| `notification:events:publish` | Publish live events to users of the tenant (modules) |
| `notification:permissions:manage` | Grant and revoke access on channels and templates the caller may share |
| `notification:backup:manage` | Export and import tenant backups (bulk disclosure with credentials on request) |
| `notification:stats:read` | Read statistics, health and the audit trail |

### notification:channels:read

List and read notification channels the caller is granted (settings redacted).

**UI actions**: `read`, `create`, `update`, `delete`, `share`, `use` on `Channel`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Channels.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/notification/v1/channels` | listChannels |
| `GET` | `/api/notification/v1/channels/{id}` | getChannel |
| `GET` | `/api/notification/v1/access/check` | checkAccess |
| `GET` | `/api/notification/v1/access/effective` | effectivePermissions |

**Scope and additional checks**: Channel and template resource grants still apply on top of module roles; sending requires the relevant use access. The administrator module role excludes events:publish, which is a module capability; owner/admin built-in grants retain it. Reading channel settings returns redacted settings.

### notification:channels:manage

Create, change, test and delete channels the caller is granted.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/notification/v1/channels` | createChannel |
| `PUT` | `/api/notification/v1/channels/{id}` | updateChannel |
| `POST` | `/api/notification/v1/channels/{id}/remove` | deleteChannel |
| `POST` | `/api/notification/v1/channels/{id}/test` | testChannel |

**Scope and additional checks**: Channel and template resource grants still apply on top of module roles; sending requires the relevant use access. The administrator module role excludes events:publish, which is a module capability; owner/admin built-in grants retain it. Reading channel settings returns redacted settings.

### notification:templates:read

List, read and preview templates the caller is granted.

**UI actions**: `read`, `create`, `update`, `delete`, `share`, `use` on `Template`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Templates.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/notification/v1/templates` | listTemplates |
| `GET` | `/api/notification/v1/templates/{id}` | getTemplate |
| `POST` | `/api/notification/v1/templates/preview` | previewTemplate |

**Scope and additional checks**: Channel and template resource grants still apply on top of module roles; sending requires the relevant use access. The administrator module role excludes events:publish, which is a module capability; owner/admin built-in grants retain it. Reading channel settings returns redacted settings.

### notification:templates:manage

Create, change and delete templates the caller is granted.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/notification/v1/templates` | createTemplate |
| `PUT` | `/api/notification/v1/templates/{id}` | updateTemplate |
| `POST` | `/api/notification/v1/templates/{id}/remove` | deleteTemplate |
| `POST` | `/api/notification/v1/templates/{id}/restore` | restoreTemplate |

**Scope and additional checks**: Channel and template resource grants still apply on top of module roles; sending requires the relevant use access. The administrator module role excludes events:publish, which is a module capability; owner/admin built-in grants retain it. Reading channel settings returns redacted settings.

### notification:notifications:send

Send notifications through templates and channels the caller may use.

**UI actions**: `send` on `Notification`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/notification/v1/notifications/send` | sendNotification |

**Scope and additional checks**: Channel and template resource grants still apply on top of module roles; sending requires the relevant use access. The administrator module role excludes events:publish, which is a module capability; owner/admin built-in grants retain it. Reading channel settings returns redacted settings.

### notification:notifications:read

Read the notification log (own sends without stats:read).

**UI actions**: `read` on `NotificationLog`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Log.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/notification/v1/notifications` | listNotifications |
| `GET` | `/api/notification/v1/notifications/{id}` | getNotification |

**Scope and additional checks**: Channel and template resource grants still apply on top of module roles; sending requires the relevant use access. The administrator module role excludes events:publish, which is a module capability; owner/admin built-in grants retain it. Reading channel settings returns redacted settings.

### notification:messages:read

List message categories and messages.

**Navigation gated by this permission**: Messages.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/notification/v1/categories` | listCategories |
| `GET` | `/api/notification/v1/messages` | listMessages |
| `GET` | `/api/notification/v1/messages/{id}` | getMessage |

**Scope and additional checks**: Channel and template resource grants still apply on top of module roles; sending requires the relevant use access. The administrator module role excludes events:publish, which is a module capability; owner/admin built-in grants retain it. Reading channel settings returns redacted settings.

### notification:messages:manage

Create, send, revoke and archive internal messages; manage categories.

**UI actions**: `manage` on `Message`, `MessageCategory`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Categories.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/notification/v1/categories` | createCategory |
| `PUT` | `/api/notification/v1/categories/{id}` | updateCategory |
| `POST` | `/api/notification/v1/categories/{id}/remove` | deleteCategory |
| `POST` | `/api/notification/v1/messages` | createMessage |
| `PUT` | `/api/notification/v1/messages/{id}` | updateMessage |
| `POST` | `/api/notification/v1/messages/{id}/send` | sendMessage |
| `POST` | `/api/notification/v1/messages/{id}/cancel` | cancelSchedule |
| `POST` | `/api/notification/v1/messages/{id}/revoke` | revokeMessage |
| `POST` | `/api/notification/v1/messages/{id}/archive` | archiveMessage |
| `POST` | `/api/notification/v1/messages/{id}/remove` | deleteMessage |
| `GET` | `/api/notification/v1/messages/{id}/recipients` | listMessageRecipients |

**Scope and additional checks**: Channel and template resource grants still apply on top of module roles; sending requires the relevant use access. The administrator module role excludes events:publish, which is a module capability; owner/admin built-in grants retain it. Reading channel settings returns redacted settings.

### notification:inbox:read

Read and manage the caller's own inbox and live stream.

**UI actions**: `read` on `Inbox`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Inbox.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/notification/v1/inbox` | listInbox |
| `GET` | `/api/notification/v1/inbox/unread` | unreadCount |
| `GET` | `/api/notification/v1/inbox/{id}` | readInboxEntry |
| `POST` | `/api/notification/v1/inbox/status` | markInbox |
| `POST` | `/api/notification/v1/inbox/remove` | deleteFromInbox |
| `GET` | `/api/notification/v1/stream` | stream |

**Scope and additional checks**: Channel and template resource grants still apply on top of module roles; sending requires the relevant use access. The administrator module role excludes events:publish, which is a module capability; owner/admin built-in grants retain it. Reading channel settings returns redacted settings.

### notification:events:publish

Publish live events to users of the tenant (modules).

The imported OpenAPI operations do not declare a matching `x-freya-permission` for this grant. Use the manifest and server authorization implementation to identify its enforcement; this absence does not indicate public access.

**Scope and additional checks**: Channel and template resource grants still apply on top of module roles; sending requires the relevant use access. The administrator module role excludes events:publish, which is a module capability; owner/admin built-in grants retain it. Reading channel settings returns redacted settings.

### notification:permissions:manage

Grant and revoke access on channels and templates the caller may share.

**UI actions**: `manage` on `NotificationGrant`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Permissions.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/notification/v1/grants` | listGrants |
| `POST` | `/api/notification/v1/grants` | grant |
| `POST` | `/api/notification/v1/grants/{id}/revoke` | revoke |

**Scope and additional checks**: Channel and template resource grants still apply on top of module roles; sending requires the relevant use access. The administrator module role excludes events:publish, which is a module capability; owner/admin built-in grants retain it. Reading channel settings returns redacted settings.

### notification:backup:manage

Export and import tenant backups (bulk disclosure with credentials on request).

**UI actions**: `manage` on `NotificationBackup`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/notification/v1/backup/export` | exportBackup |
| `POST` | `/api/notification/v1/backup/import` | importBackup |

**Scope and additional checks**: Channel and template resource grants still apply on top of module roles; sending requires the relevant use access. The administrator module role excludes events:publish, which is a module capability; owner/admin built-in grants retain it. Reading channel settings returns redacted settings.

### notification:stats:read

Read statistics, health and the audit trail.

**UI actions**: `read` on `NotificationStats`, `NotificationAudit`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/notification/v1/stats` | stats |
| `GET` | `/api/notification/v1/audit` | auditTrail |
| `GET` | `/api/notification/v1/health` | health |

**Scope and additional checks**: Channel and template resource grants still apply on top of module roles; sending requires the relevant use access. The administrator module role excludes events:publish, which is a module capability; owner/admin built-in grants retain it. Reading channel settings returns redacted settings.
<div class="guide-actions"><a href="how-to/notification/docker.html">Install with Docker Compose →</a><a href="how-to/notification/native.html">Install without Docker →</a><a href="downloads/notification.zip">Download Compose bundle ↓</a></div>

## Dependencies and integration

**Required**: TimescaleDB, Valkey, key-encryption key, Auth, Portal, mesh identity.

**Optional or feature-dependent**: SMTP delivery provider, Scheduler.

SMTP is the implemented delivery provider in this source snapshot. Do not treat future channel types as available providers. Configure and test the SMTP channel before expecting delivery.

The list describes infrastructure/features, not every transitive library. Check the linked deployment reference for exact versions, enabled features and peer grants. [Framework dependencies](architecture/dependencies.html) cover the shared Go libraries.

## Runtime and operation

| Item | Reference |
| --- | --- |
| Service binary | `notificationsvc` |
| Public example configuration | `deploy/dev.yaml`; adapt endpoints and paths for your environment |
| Native source build | Go `1.26.3`, toolchain `go1.26.8`, Node 22 for UI |
| Image repository | `ghcr.io/go-tangra/go-tangra-notification`; choose a published compatible version |
| Private admin default | `127.0.0.1:9590`; check actual configuration |
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
| `Config` | `smtp` | `SMTP` |
| `Config` | `scheduler` | `Scheduler` |
| `Config` | `task_scheduler` | `TaskScheduler` |
| `Config` | `gateway` | `Gateway` |
| `Config` | `enroll` | `Enroll` |
| `Config` | `limits_notification` | `Limits` |
| `Config` | `platform_email` | `*PlatformEmail` |
| `Config` | `platform_tenant_id` | `string` |
| `PlatformEmail` | `host` | `string` |
| `PlatformEmail` | `port` | `int` |
| `PlatformEmail` | `tls` | `string` |
| `PlatformEmail` | `username` | `string` |
| `PlatformEmail` | `password` | `string` |
| `PlatformEmail` | `password_file` | `string` |
| `PlatformEmail` | `from` | `string` |
| `PlatformEmail` | `reply_to` | `string` |
| `PlatformEmail` | `allow_plaintext` | `bool` |
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
| `SMTP` | `allow_plaintext` | `bool` |
| `SMTP` | `dial_timeout_seconds` | `int` |
| `Scheduler` | `interval_seconds` | `int` |
| `Scheduler` | `lease_seconds` | `int` |
| `TaskScheduler` | `enabled` | `bool` |
| `TaskScheduler` | `service` | `string` |
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
| `Limits` | `send_per_tenant_per_minute` | `int` |
| `Limits` | `send_per_sender_per_minute` | `int` |
| `Limits` | `streams_per_user` | `int` |
| `Limits` | `streams_per_tenant` | `int` |
| `Limits` | `replay_window_seconds` | `int` |
| `Limits` | `system_send_per_minute` | `int` |

[Configuration structures and validation](https://github.com/go-tangra/go-tangra-notification/blob/84f73a432d9bd0e493524a972d253067dd5a812d/internal/config/config.go)

## API operation index

These operations are extracted from the module's OpenAPI contract. Read the source contract for request/response schemas, permission checks and exact route bases; internal mesh endpoints must not be treated as anonymous public APIs.

| Method | Contract path | Operation |
| --- | --- | --- |
| `GET` | `/api/notification/v1/channels` | listChannels |
| `POST` | `/api/notification/v1/channels` | createChannel |
| `GET` | `/api/notification/v1/channels/{id}` | getChannel |
| `PUT` | `/api/notification/v1/channels/{id}` | updateChannel |
| `POST` | `/api/notification/v1/channels/{id}/remove` | deleteChannel |
| `POST` | `/api/notification/v1/channels/{id}/test` | testChannel |
| `GET` | `/api/notification/v1/templates` | listTemplates |
| `POST` | `/api/notification/v1/templates` | createTemplate |
| `GET` | `/api/notification/v1/templates/{id}` | getTemplate |
| `PUT` | `/api/notification/v1/templates/{id}` | updateTemplate |
| `POST` | `/api/notification/v1/templates/{id}/remove` | deleteTemplate |
| `POST` | `/api/notification/v1/templates/{id}/restore` | restoreTemplate |
| `POST` | `/api/notification/v1/templates/preview` | previewTemplate |
| `POST` | `/api/notification/v1/notifications/send` | sendNotification |
| `GET` | `/api/notification/v1/notifications` | listNotifications |
| `GET` | `/api/notification/v1/notifications/{id}` | getNotification |
| `GET` | `/api/notification/v1/grants` | listGrants |
| `POST` | `/api/notification/v1/grants` | grant |
| `POST` | `/api/notification/v1/grants/{id}/revoke` | revoke |
| `GET` | `/api/notification/v1/access/check` | checkAccess |
| `GET` | `/api/notification/v1/access/effective` | effectivePermissions |
| `GET` | `/api/notification/v1/categories` | listCategories |
| `POST` | `/api/notification/v1/categories` | createCategory |
| `PUT` | `/api/notification/v1/categories/{id}` | updateCategory |
| `POST` | `/api/notification/v1/categories/{id}/remove` | deleteCategory |
| `GET` | `/api/notification/v1/messages` | listMessages |
| `POST` | `/api/notification/v1/messages` | createMessage |
| `GET` | `/api/notification/v1/messages/{id}` | getMessage |
| `PUT` | `/api/notification/v1/messages/{id}` | updateMessage |
| `POST` | `/api/notification/v1/messages/{id}/send` | sendMessage |
| `POST` | `/api/notification/v1/messages/{id}/cancel` | cancelSchedule |
| `POST` | `/api/notification/v1/messages/{id}/revoke` | revokeMessage |
| `POST` | `/api/notification/v1/messages/{id}/archive` | archiveMessage |
| `POST` | `/api/notification/v1/messages/{id}/remove` | deleteMessage |
| `GET` | `/api/notification/v1/messages/{id}/recipients` | listMessageRecipients |
| `GET` | `/api/notification/v1/inbox` | listInbox |
| `GET` | `/api/notification/v1/inbox/unread` | unreadCount |
| `GET` | `/api/notification/v1/inbox/{id}` | readInboxEntry |
| `POST` | `/api/notification/v1/inbox/status` | markInbox |
| `POST` | `/api/notification/v1/inbox/remove` | deleteFromInbox |
| `GET` | `/api/notification/v1/stream` | stream |
| `POST` | `/api/notification/v1/backup/export` | exportBackup |
| `POST` | `/api/notification/v1/backup/import` | importBackup |
| `GET` | `/api/notification/v1/stats` | stats |
| `GET` | `/api/notification/v1/audit` | auditTrail |
| `GET` | `/api/notification/v1/health` | health |

[OpenAPI: api/openapi/notification.yaml](https://github.com/go-tangra/go-tangra-notification/blob/84f73a432d9bd0e493524a972d253067dd5a812d/api/openapi/notification.yaml)

## Detailed source references

- [README.md](sources/notification/README.html) — captured at `84f73a432d9b`.
- [docs/dependencies.md](sources/notification/docs/dependencies.html) — captured at `84f73a432d9b`.
- [docs/operations.md](sources/notification/docs/operations.html) — captured at `84f73a432d9b`.
- [docs/security-model.md](sources/notification/docs/security-model.html) — captured at `84f73a432d9b`.

## Limits, diagnostics and recovery

SMTP is the implemented delivery provider in this source snapshot. Do not treat future channel types as available providers. Configure and test the SMTP channel before expecting delivery.

Use the module's operations/deployment reference for retention, backup/restore, refusal behavior, interface examples and feature limitations. The installation guides cover common readiness, identity, registration and storage failures.

## Upstream overview: go-tangra-notification

Tenant notification and messaging service for the
[go-tangra v4 platform](https://github.com/go-tangra/go-tangra).

It delivers **outbound notifications** through configurable channels (email over
SMTP is fully implemented; sms/slack/sse are declared for later providers)
using Go-template subjects and bodies, and **internal messages** (an in-app
inbox with categories, scheduling, revoke and a live server-sent-events
stream). Channel credentials are encrypted at rest (AES-256-GCM envelope) and
never returned in full; access to channels and templates is Zanzibar-style
(owner / editor / viewer / sharer, to users, roles or the tenant, with
expiry). Every operation is audited; credentials and message bodies never
reach logs, the audit trail or a credential-free backup.

It is also the platform's **central outbound email path**: the relay is
configured once (`platform_email`), and auth, warden and lcm send their
invitation, recovery, share-link and certificate-expiry mail through
`notification.v1.Notifier/Send` by system template key (`auth.invite`,
`warden.share`, `lcm.certificates_expiring`, ...), with the links redacted in
the delivery log (feature 017). For the scheduler module it executes the
scheduled task `notification:send-test-email` (feature 026, config
`task_scheduler`). Services depend on the small
`github.com/go-tangra/go-tangra-notification/sdk/v4` module (proto +
`pkg/notifyclient`), not on this service module.

Security model: [`docs/security-model.md`](sources/notification/docs/security-model.html).
Operations: [`docs/operations.md`](sources/notification/docs/operations.html).
Dependencies: [`docs/dependencies.md`](sources/notification/docs/dependencies.html).
Design history: `specs/006-notification-service`, `specs/017-central-email-delivery`.

## Place in the platform

```
go-tangra/go-tangra          platform module + @go-tangra/ui kit
        |
go-tangra-auth  <---->  go-tangra-portal (gateway)  <---->  go-tangra-lcm
                                  |
                        go-tangra-notification  <----  warden, auth (Notifier / Events gRPC)
```

- Built on `github.com/go-tangra/go-tangra/v4` (mTLS transports, identity,
  service policy, audit, observability).
- Verifies platform tokens, resolves people and checks permissions through the
  auth SDK (`github.com/go-tangra/go-tangra-auth/sdk/v4`).
- Registers with the gateway through the portal SDK
  (`github.com/go-tangra/go-tangra-portal/sdk/v4`), which fronts the browser API
  and the federated UI remote.
- Can enroll for its SVID with lcm over the network
  (`github.com/go-tangra/go-tangra-lcm/sdk/v4`), as the platform stack does.

The repository holds one Go module, `github.com/go-tangra/go-tangra-notification/v4`.
Other services call it through the `sdk` module (`github.com/go-tangra/go-tangra-notification/sdk/v4`): `pkg/notifyclient` and the `notification.v1` protos.

## Layout

| Path | What |
|------|------|
| `api/openapi/notification.yaml` | browser API contract (served under `/api/notification/v1`) |
| `sdk/api/proto/notification/v1/` | `Notifier` (Send, SendTest) and `Events` (Publish) gRPC for services |
| `api/schema/backup.schema.json` | tenant backup document schema |
| `internal/config` | configuration + validation (secure defaults, named opt-outs) |
| `internal/store`, `internal/repo` | TimescaleDB schema (RLS, hypertables), repositories + in-memory double |
| `internal/sealed` | envelope encryption of channel settings (KEK -> DEK, `"__set__"` redaction) |
| `internal/audit` | closed audit vocabulary, batched writer, credential/content guard |
| `internal/authz` | Zanzibar grants (owner/editor/viewer/sharer, `use`) |
| `internal/channel`, `internal/channel/email` | delivery providers (stdlib `net/smtp`, hand-built MIME) |
| `internal/render` | safe Go-template rendering (fixed FuncMap, bounded time/size) |
| `internal/notify` | channels, templates and the send pipeline + log |
| `internal/messages`, `internal/inbox` | internal messages, scheduler, per-user inbox |
| `internal/stream` | Valkey-backed live event fan-out + SSE relay |
| `internal/transfer`, `internal/stats` | backup export/import, operator statistics |
| `internal/httpapi`, `internal/grpcapi` | browser and service APIs |
| `internal/app`, `cmd/notificationsvc` | wiring and the service binary (serve, `bootstrap`, `version`) |
| `pkg/notificationmanifest` | gateway manifest built from the OpenAPI document |
| `sdk/pkg/notifyclient` | Go client other services use to Send / Publish |
| `deploy` | compose stack, dev configuration, service policy |
| `tests/{contract,fuzz,integration}` | contract, fuzz and Docker-backed integration suites |
| `ui/` | Vue 3 + FlyonUI federated remote on `@go-tangra/ui` (channels, templates, log, messages, inbox, permissions, ops) |

## Build and test

You need Go 1.26, Node 22, Docker (for integration tests and the image), and a
GitHub token with `read:packages` to install `@go-tangra/ui` from GitHub Packages.

```bash
go build ./... && go vet ./... && go test -race ./...
(cd sdk && buf lint)
make test-integration                     # -tags integration, needs Docker (see below)
make lint cover fuzz redaction-scan vuln

cd ui
export NODE_AUTH_TOKEN=$(gh auth token)   # ui/.npmrc only references this variable
npm ci && npm run lint && npm run test:unit && npm run build
```

The unit coverage gate requires at least 80 % overall and 100 % for the
authorization, rendering, sealing, stream and email packages. Generated code,
SQL bindings and wiring are covered by the integration suite instead.

The integration suite runs the real auth and gateway services next to this
one. It builds them from checkouts of
[go-tangra-auth](https://github.com/go-tangra/go-tangra-auth) and
[go-tangra-portal](https://github.com/go-tangra/go-tangra-portal): by default
sibling clones next to this repository, or the directories named by
`GO_TANGRA_AUTH_DIR` and `GO_TANGRA_PORTAL_DIR`. The auth policy contract check
uses the same auth checkout and is skipped without one.

## Run locally

```bash
make compose-up                           # TimescaleDB :5434, Valkey :6381, Mailpit :8027/:1027
go run ./cmd/notificationsvc bootstrap -config deploy/dev.yaml
go run -tags ui ./cmd/notificationsvc -config deploy/dev.yaml   # after the ui build
```

`deploy/dev.yaml` expects a development SVID and a key-encryption key at
`deploy/kek.dev` (git-ignored). The full platform (gateway, auth, lcm and this
service) runs from the go-tangra platform stack (`deploy/stack`), which mounts
its own configuration and development KEK. See
`specs/006-notification-service/quickstart.md` for the end-to-end walkthrough.

## Container image

The image is `ghcr.io/go-tangra/go-tangra-notification`, built by
`.github/workflows/ci.yaml`. It carries `notificationsvc` with the embedded UI remote.

```bash
docker buildx build --secret id=npm_token,env=NODE_AUTH_TOKEN \
  --build-arg APP_VERSION=4.0.0 -t go-tangra-notification:dev .
docker run --rm go-tangra-notification:dev version
```

The image runs `notificationsvc -config deploy/dev.yaml` as user `app` (uid 10001).
It contains no key material: deployments mount their own configuration and
key-encryption key (the platform stack mounts it at `/app/deploy/kek.dev`).

## API permissions

`channels:read/manage`, `templates:read/manage`, `notifications:send/read`,
`messages:read/manage`, `inbox:read`, `events:publish`, `permissions:manage`,
`backup:manage`, `stats:read`. The gateway enforces the per-route permission
from the manifest; the module then enforces the Zanzibar grant (`use` is what
sending requires).

The module registers with auth as `notification` (auth SDK
`authclient.Registration`, feature 019) at start, retrying every 5 s until
auth accepts, then every five minutes: the permissions, the module roles
(`pkg/notificationmanifest.Roles`) and the built-in role grants
(`pkg/notificationmanifest.Grants`, unchanged). Module roles are locked in
auth; administrators assign them or clone them into custom roles:

| Role | Display name | Permissions |
|---|---|---|
| `administrator` | Notifications administrator | every permission except `events:publish` |
| `sender` | Notifications sender | channels:read, templates:read, notifications:send, notifications:read, messages:read, messages:manage, inbox:read |
| `viewer` | Notifications viewer | channels:read, templates:read, notifications:read, messages:read, inbox:read |

`events:publish` is for modules pushing live events; no module role carries
it (owner and admin keep it through the built-in grants). Channel and
template grants still apply on top of any role.

## Limits (defaults)

600 sends/min per tenant, 60/min per sender, 300 system template sends/min per
calling service; 5 live streams per person, 2000
per tenant; a 5-minute replay window; a 16 MiB backup upload; the scheduler
runs every 15 s with a 60 s lease.

## Versioning

- Releases are tagged `vX.Y.Z`. CI publishes the image as `X.Y.Z`, `X.Y`, `X`
  and `sha-<short>`. There is no `latest` tag.
- v4.0.0 rebuilds the service on the go-tangra v4 platform. The v3 line stays on
  the `v3` branch and its `v3.x` tags.
