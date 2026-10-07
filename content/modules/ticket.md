# Ticket

Email helpdesk, conversations, mailboxes and triage rules.

**Architecture role**: Business modules. [See the complete component map](architecture/index.html).

**Documented source**: `51bd9b9f50c1` · nearest local service tag `v4.3.2` · v4 major. [Repository at this revision](https://github.com/go-tangra/go-tangra-ticket/tree/51bd9b9f50c137376be99b56bfa4cf3badbe7f1e). Tags are source metadata, not a claim of image publication or cross-module compatibility.


## Permissions and authorization

This catalogue contains **8 permissions** declared by the [module manifest](https://github.com/go-tangra/go-tangra-ticket/blob/51bd9b9f50c137376be99b56bfa4cf3badbe7f1e/pkg/ticketmanifest/manifest.go) at the revision above. Custom-role references use `module:resource:action`; the manifest and API contract use the local `resource:action` form. The action names are distinct grants: do not assume `manage` automatically includes `read` or another action.

Module permissions gate actions within the authenticated tenant. The endpoint still enforces its resource and workflow checks; a UI ability describes presentation and does not replace server authorization.

[How to assign and verify permissions](architecture/security.html#assign-and-verify-permissions). Module roles and built-in grant mappings are defined in the linked manifest; review those mappings before assigning a broad role.

| Qualified permission | What it allows |
| --- | --- |
| `ticket:tickets:read` | List and read tickets, conversations, attachments, tags, assignable users and the live stream |
| `ticket:tickets:manage` | Create and edit tickets, assign, change status, set tags, add notes and send replies |
| `ticket:tickets:delete` | Delete tickets with their conversations and attachments |
| `ticket:tags:manage` | Manage the tag and category vocabulary |
| `ticket:rules:manage` | Manage inbound triage rules |
| `ticket:mailboxes:manage` | Manage inbound mailboxes and acknowledgements |
| `ticket:stats:read` | Read the ticket dashboard statistics |
| `ticket:backup:manage` | Export and import tenant ticket data |

### ticket:tickets:read

List and read tickets, conversations, attachments, tags, assignable users and the live stream.

**UI actions**: `read` on `Ticket`, `TicketTag`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Tickets, Tags.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/ticket/v1/tickets` | listTickets |
| `GET` | `/api/ticket/v1/tickets/{id}` | getTicket |
| `GET` | `/api/ticket/v1/tickets/{id}/history` | listTicketHistory |
| `GET` | `/api/ticket/v1/tickets/{id}/body` | getTicketBody |
| `GET` | `/api/ticket/v1/tickets/{id}/attachments/{att_id}` | downloadTicketAttachment |
| `GET` | `/api/ticket/v1/tickets/{id}/comments` | listTicketComments |
| `GET` | `/api/ticket/v1/tags` | listTags |
| `GET` | `/api/ticket/v1/assignable-users` | listAssignableUsers |
| `GET` | `/api/ticket/v1/stream` | streamEvents |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### ticket:tickets:manage

Create and edit tickets, assign, change status, set tags, add notes and send replies.

**UI actions**: `create`, `update`, `assign`, `comment`, `reply` on `Ticket`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/ticket/v1/tickets` | createTicket |
| `PUT` | `/api/ticket/v1/tickets/{id}` | updateTicket |
| `POST` | `/api/ticket/v1/tickets/{id}/assign` | assignTicket |
| `POST` | `/api/ticket/v1/tickets/{id}/status` | setTicketStatus |
| `POST` | `/api/ticket/v1/tickets/{id}/tags` | setTicketTags |
| `POST` | `/api/ticket/v1/tickets/{id}/comments` | addTicketNote |
| `POST` | `/api/ticket/v1/tickets/{id}/reply` | replyToTicket |
| `DELETE` | `/api/ticket/v1/comments/{id}` | deleteComment |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### ticket:tickets:delete

Delete tickets with their conversations and attachments.

**UI actions**: `delete` on `Ticket`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `DELETE` | `/api/ticket/v1/tickets/{id}` | deleteTicket |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### ticket:tags:manage

Manage the tag and category vocabulary.

**UI actions**: `manage` on `TicketTag`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/ticket/v1/tags` | createTag |
| `PUT` | `/api/ticket/v1/tags/{id}` | updateTag |
| `DELETE` | `/api/ticket/v1/tags/{id}` | deleteTag |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### ticket:rules:manage

Manage inbound triage rules.

**UI actions**: `manage` on `TicketRule`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/ticket/v1/rules` | listRules |
| `POST` | `/api/ticket/v1/rules` | createRule |
| `POST` | `/api/ticket/v1/rules/test` | testRule |
| `GET` | `/api/ticket/v1/rules/{id}` | getRule |
| `PUT` | `/api/ticket/v1/rules/{id}` | updateRule |
| `DELETE` | `/api/ticket/v1/rules/{id}` | deleteRule |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### ticket:mailboxes:manage

Manage inbound mailboxes and acknowledgements.

**UI actions**: `manage` on `TicketMailbox`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Mailboxes.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/ticket/v1/mailboxes` | listMailboxes |
| `POST` | `/api/ticket/v1/mailboxes` | createMailbox |
| `PUT` | `/api/ticket/v1/mailboxes/{id}` | updateMailbox |
| `DELETE` | `/api/ticket/v1/mailboxes/{id}` | deleteMailbox |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### ticket:stats:read

Read the ticket dashboard statistics.

**UI actions**: `read` on `TicketStats`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Dashboard.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `GET` | `/api/ticket/v1/stats` | getStats |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.

### ticket:backup:manage

Export and import tenant ticket data.

**UI actions**: `manage` on `TicketBackup`. These are the manifest’s CASL presentation rules.

**API operations declaring this permission**:

| Method | Contract path | Action |
| --- | --- | --- |
| `POST` | `/api/ticket/v1/backup/export` | exportBackup |
| `POST` | `/api/ticket/v1/backup/import` | importBackup |

**Scope and additional checks**: This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.
<div class="guide-actions"><a href="how-to/ticket/docker.html">Install with Docker Compose →</a><a href="how-to/ticket/native.html">Install without Docker →</a><a href="downloads/ticket.zip">Download Compose bundle ↓</a></div>

## Dependencies and integration

**Required**: TimescaleDB, Valkey, S3-compatible storage, key-encryption key, Auth, Portal, mesh identity.

**Optional or feature-dependent**: inbound email relay, SMTP, Notification.

The inbound mail listener is a separate edge with a relay token. Configure mailboxes and SMTP/notification delivery before testing conversations; do not expose the private module API or admin listener as the mail edge.

The list describes infrastructure/features, not every transitive library. Check the linked deployment reference for exact versions, enabled features and peer grants. [Framework dependencies](architecture/dependencies.html) cover the shared Go libraries.

## Runtime and operation

| Item | Reference |
| --- | --- |
| Service binary | `ticketsvc` |
| Public example configuration | `deploy/dev.yaml`; adapt endpoints and paths for your environment |
| Native source build | Go `1.26.3`, toolchain `go1.26.8`, Node 22 for UI |
| Image repository | `ghcr.io/go-tangra/go-tangra-ticket`; choose a published compatible version |
| Private admin default | `127.0.0.1:9840`; check actual configuration |
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
| `Config` | `inbound` | `Inbound` |
| `Config` | `smtp` | `SMTP` |
| `Config` | `rules` | `Rules` |
| `Config` | `secrets` | `Secrets` |
| `Config` | `events` | `Events` |
| `Config` | `gateway` | `Gateway` |
| `Config` | `mesh_enroll` | `MeshEnroll` |
| `Config` | `limits_ticket` | `Limits` |
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
| `Inbound` | `addr` | `string` |
| `Inbound` | `tls_cert_file` | `string` |
| `Inbound` | `tls_key_file` | `string` |
| `Inbound` | `insecure_dev` | `bool` |
| `Inbound` | `relay_token_ref` | `string` |
| `Inbound` | `max_body_bytes` | `int64` |
| `Inbound` | `max_attachment_bytes` | `int64` |
| `Inbound` | `max_parts` | `int` |
| `Inbound` | `max_depth` | `int` |
| `SMTP` | `host` | `string` |
| `SMTP` | `port` | `int` |
| `SMTP` | `tls` | `string` |
| `SMTP` | `allow_plaintext` | `bool` |
| `SMTP` | `username` | `string` |
| `SMTP` | `password_ref` | `string` |
| `SMTP` | `mail_domain` | `string` |
| `SMTP` | `timeout_seconds` | `int` |
| `Rules` | `cost_limit` | `uint64` |
| `Rules` | `eval_timeout_ms` | `int` |
| `Rules` | `max_rules` | `int` |
| `Secrets` | `warden_service` | `string` |
| `Secrets` | `token_file` | `string` |
| `Secrets` | `refresh_seconds` | `int` |
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
| `Limits` | `max_page_size` | `int` |

[Configuration structures and validation](https://github.com/go-tangra/go-tangra-ticket/blob/51bd9b9f50c137376be99b56bfa4cf3badbe7f1e/internal/config/config.go)

## API operation index

These operations are extracted from the module's OpenAPI contract. Read the source contract for request/response schemas, permission checks and exact route bases; internal mesh endpoints must not be treated as anonymous public APIs.

| Method | Contract path | Operation |
| --- | --- | --- |
| `GET` | `/api/ticket/v1/tickets` | listTickets |
| `POST` | `/api/ticket/v1/tickets` | createTicket |
| `GET` | `/api/ticket/v1/tickets/{id}` | getTicket |
| `PUT` | `/api/ticket/v1/tickets/{id}` | updateTicket |
| `DELETE` | `/api/ticket/v1/tickets/{id}` | deleteTicket |
| `POST` | `/api/ticket/v1/tickets/{id}/assign` | assignTicket |
| `POST` | `/api/ticket/v1/tickets/{id}/status` | setTicketStatus |
| `POST` | `/api/ticket/v1/tickets/{id}/tags` | setTicketTags |
| `GET` | `/api/ticket/v1/tickets/{id}/history` | listTicketHistory |
| `GET` | `/api/ticket/v1/tickets/{id}/body` | getTicketBody |
| `GET` | `/api/ticket/v1/tickets/{id}/attachments/{att_id}` | downloadTicketAttachment |
| `GET` | `/api/ticket/v1/tickets/{id}/comments` | listTicketComments |
| `POST` | `/api/ticket/v1/tickets/{id}/comments` | addTicketNote |
| `POST` | `/api/ticket/v1/tickets/{id}/reply` | replyToTicket |
| `DELETE` | `/api/ticket/v1/comments/{id}` | deleteComment |
| `GET` | `/api/ticket/v1/tags` | listTags |
| `POST` | `/api/ticket/v1/tags` | createTag |
| `PUT` | `/api/ticket/v1/tags/{id}` | updateTag |
| `DELETE` | `/api/ticket/v1/tags/{id}` | deleteTag |
| `GET` | `/api/ticket/v1/rules` | listRules |
| `POST` | `/api/ticket/v1/rules` | createRule |
| `POST` | `/api/ticket/v1/rules/test` | testRule |
| `GET` | `/api/ticket/v1/rules/{id}` | getRule |
| `PUT` | `/api/ticket/v1/rules/{id}` | updateRule |
| `DELETE` | `/api/ticket/v1/rules/{id}` | deleteRule |
| `GET` | `/api/ticket/v1/mailboxes` | listMailboxes |
| `POST` | `/api/ticket/v1/mailboxes` | createMailbox |
| `PUT` | `/api/ticket/v1/mailboxes/{id}` | updateMailbox |
| `DELETE` | `/api/ticket/v1/mailboxes/{id}` | deleteMailbox |
| `GET` | `/api/ticket/v1/assignable-users` | listAssignableUsers |
| `GET` | `/api/ticket/v1/stats` | getStats |
| `GET` | `/api/ticket/v1/stream` | streamEvents |
| `POST` | `/api/ticket/v1/backup/export` | exportBackup |
| `POST` | `/api/ticket/v1/backup/import` | importBackup |
| `GET` | `/api/ticket/v1/health` | health |

[OpenAPI: api/openapi/ticket.yaml](https://github.com/go-tangra/go-tangra-ticket/blob/51bd9b9f50c137376be99b56bfa4cf3badbe7f1e/api/openapi/ticket.yaml)

## Detailed source references

- [README.md](sources/ticket/README.html) — captured at `51bd9b9f50c1`.
- [deploy/README.md](sources/ticket/deploy/README.html) — captured at `51bd9b9f50c1`.

## Limits, diagnostics and recovery

The inbound mail listener is a separate edge with a relay token. Configure mailboxes and SMTP/notification delivery before testing conversations; do not expose the private module API or admin listener as the mail edge.

Use the module's operations/deployment reference for retention, backup/restore, refusal behavior, interface examples and feature limitations. The installation guides cover common readiness, identity, registration and storage failures.

## Upstream overview: go-tangra-ticket

Tenant email helpdesk service for the
[go-tangra v4 platform](https://github.com/go-tangra/go-tangra).

It keeps **tickets** (status, priority, assignee, tags) with a **conversation
timeline** of internal notes and emailed public replies. **Inbound email** arrives
on a separate off-mesh edge and becomes a new ticket or threads back into an
existing one (`In-Reply-To`/`References` or the `[#<ticket-id>]` reference token).
Loop-safe (RFC 3834) auto-acknowledgements, sandboxed **CEL triage rules**,
mailboxes, history, statistics and tenant backup come with it. Attachments live in
S3-compatible object storage (RustFS or MinIO), HTML bodies are only ever returned
sanitised, and the relay token and SMTP password are secret **references**
(warden in production) that are resolved at use time and never logged.
Changes are published live on the platform event bus.

Operations: [`deploy/README.md`](sources/ticket/deploy/README.html).
Design history: `specs/014-ticket-service`.

## Place in the platform

```
go-tangra/go-tangra          platform module + @go-tangra/ui kit
        |
go-tangra-auth  <---->  go-tangra-portal (gateway)  <---->  go-tangra-lcm
                                  |
mail relay --(:9957)-->  go-tangra-ticket  ---->  object storage (S3), SMTP relay
                                  |
                          go-tangra-warden (relay token, SMTP password)
```

- Built on `github.com/go-tangra/go-tangra/v4` (mTLS transports, identity,
  service policy, audit, observability).
- Verifies platform tokens, resolves agents and checks permissions through the
  auth SDK (`github.com/go-tangra/go-tangra-auth/sdk/v4`).
- Registers with the gateway through the portal SDK
  (`github.com/go-tangra/go-tangra-portal/sdk/v4`), which fronts the browser API
  (`/api/ticket`) and the federated UI remote.
- Enrolls for its SVID with lcm over the network
  (`github.com/go-tangra/go-tangra-lcm/sdk/v4`), as the platform stack does.
- Resolves `warden:` secret references through the warden SDK
  (`github.com/go-tangra/go-tangra-warden/sdk/v4`).

The repository holds one Go module, `github.com/go-tangra/go-tangra-ticket/v4`.
Other services call it through `pkg/ticketclient` and the `ticket.v1` protos
(not proxied by the gateway).

## Layout

| Path | What |
|------|------|
| `api/openapi/ticket.yaml` | browser API contract (served under `/api/ticket`) |
| `api/proto/ticket/v1/` | module gRPC surface (`Tickets/{Create,Get,List,AddComment}`) |
| `internal/config` | configuration + validation (secure defaults, named opt-outs) |
| `internal/store`, `internal/repo` | TimescaleDB schema (RLS), repositories; `internal/memstore` is the in-memory test double |
| `internal/inbound` | off-mesh inbound mail edge (relay token, routing by mailbox address) |
| `internal/mailparse`, `internal/sanitize`, `internal/thread` | RFC 822 parsing, HTML sanitising, threading |
| `internal/mailer` | outbound SMTP (replies, acknowledgements) |
| `internal/secrets` | `warden:` / `file:` secret references with refresh |
| `internal/rules` | CEL triage rules (compile on save, cost limit, deadline) |
| `internal/blob` | S3-compatible attachment storage (minio-go) |
| `internal/sealed` | envelope encryption with the KEK |
| `internal/authz`, `internal/agents` | permission checks, assignable agents from auth |
| `internal/tickets`, `internal/comments`, `internal/tags`, `internal/mailboxes`, `internal/history` | domain services |
| `internal/events`, `internal/stream` | events on the platform bus, live stream |
| `internal/backup`, `internal/stats`, `internal/audit`, `internal/metrics` | backup export/import, statistics, audit, metrics |
| `internal/httpapi`, `internal/grpcapi` | browser and service APIs |
| `internal/app`, `cmd/ticketsvc` | wiring and the service binary (serve, `bootstrap`, `version`) |
| `pkg/ticketmanifest` | gateway manifest, module roles and built-in role grants |
| `pkg/ticketclient` | Go client other services use |
| `testdata/mail` | `.eml` fixture corpus (parser, sanitiser, threading, loop safety) |
| `deploy` | service policy and operations notes |
| `ui/` | Vue 3 + FlyonUI federated remote on `@go-tangra/ui` |

## Build and test

You need Go 1.26, Node 22, Docker (for the integration suite and the image), and a
GitHub token with `read:packages` to install `@go-tangra/ui` from GitHub Packages.

```bash
go build ./... && go vet ./... && go test -race ./...
buf lint
make test-integration                     # -tags integration: TimescaleDB, Valkey, RustFS, Mailpit via testcontainers
make lint cover vuln

cd ui
export NODE_AUTH_TOKEN=$(gh auth token)   # ui/.npmrc only references this variable
npm ci && npm run lint && npm run test:unit && npm run build
```

The integration suite (`tests/integration`) drives the whole email loop: a
fixture in, the ticket and its attachment stored, the acknowledgement and an
agent reply in Mailpit, and the requester's answer threaded back. Each
dependency can also point at a running service (`TICKET_IT_*` variables, see the
package comment).

The unit coverage gate requires at least 80 % overall and 100 % for the
authorization, sealing, secret-resolution and threading packages. Generated code,
SQL bindings and wiring are covered by the integration suite instead. The
Playwright specs in `ui/tests/e2e` need a running platform and operator
credentials; they skip otherwise.

## Run

The service runs in the go-tangra platform stack (`deploy/stack` in
[go-tangra](https://github.com/go-tangra/go-tangra)), next to TimescaleDB, Valkey,
RustFS and Mailpit. The stack mounts its configuration at
`/app/deploy/container.yaml`, the development key-encryption key at
`/app/deploy/kek.dev`, the edge certificate at `/edge` and a generated
development relay token at `/secrets/relay.token`. `deploy/kek.dev` in this
repository is a development key only; it is excluded from the image.

```bash
ticketsvc bootstrap -config deploy/container.yaml    # apply migrations and exit
ticketsvc -config deploy/container.yaml              # serve (applies migrations)
```

Listeners: gRPC `:9955` and HTTP `:9956` on the mesh (mTLS), admin `:9840`
(`/healthz`, `/readyz`), and the inbound mail edge `:9957` (TLS, relay token).
See `specs/014-ticket-service/quickstart.md` for the end-to-end walkthrough.

## Container image

The image is `ghcr.io/go-tangra/go-tangra-ticket`, built by
`.github/workflows/ci.yaml`. It carries `ticketsvc` with the embedded UI remote.

```bash
docker buildx build --secret id=npm_token,env=NODE_AUTH_TOKEN \
  --build-arg APP_VERSION=4.0.0 -t go-tangra-ticket:dev .
docker run --rm go-tangra-ticket:dev version
```

The image runs `ticketsvc -config deploy/container.yaml` as user `app`
(uid 10001). It contains no configuration and no key material: deployments mount
their own `deploy/container.yaml`, key-encryption key, inbound edge certificate
and secret references. The object store and the SMTP relay are separate services
the configuration points at (`object_store.endpoint`, `smtp.host`); the bucket is
created on start when missing.

## API permissions

`tickets:read/manage/delete`, `tags:manage`, `mailboxes:manage`, `rules:manage`,
`stats:read`, `backup:manage`. The gateway enforces the per-route permission from
the manifest; the module then checks the tenant scope.

## Roles

The module registers its permissions with auth at start and every five
minutes, together with ready-made module roles that auth offers in every
tenant (locked; administrators assign them or clone them into custom roles):

| Role | Display name | Permissions |
|---|---|---|
| `administrator` | Tickets administrator | all 8 |
| `agent` | Tickets agent | `tickets:read`, `tickets:manage`, `tags:manage` |
| `viewer` | Tickets viewer | `tickets:read` |

Built-in role grants (scoped to the ticket module by auth,
`pkg/ticketmanifest.Grants`): `owner` and `admin` hold the administrator set,
`operator` the agent set, `member` and `auditor` the viewer set.

## Versioning

- Releases are tagged `vX.Y.Z`. CI publishes the image as `X.Y.Z`, `X.Y`, `X`
  and `sha-<short>`. There is no `latest` tag.
- v4.0.0 rebuilds the service on the go-tangra v4 platform. The previous line
  stays on the `v3` branch and its `v1.x` tags.
