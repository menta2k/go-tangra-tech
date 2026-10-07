# Auth

Tenant identity, sessions, tokens and fine-grained authorization.

**Architecture role**: Control plane. [See the complete component map](architecture/index.html).

**Documented source**: `bb0045aa72dd` · nearest local service tag `v4.7.0` · v4 major. [Repository at this revision](https://github.com/go-tangra/go-tangra-auth/tree/bb0045aa72dd1451d73a6ee2764c5d69ec9cc633). Tags are source metadata, not a claim of image publication or cross-module compatibility.


## Permissions and authorization

This catalogue contains **9 permissions** declared by the [module manifest](https://github.com/go-tangra/go-tangra-auth/blob/bb0045aa72dd1451d73a6ee2764c5d69ec9cc633/pkg/authmanifest/manifest.go) at the revision above. Custom-role references use `module:resource:action`; the manifest and API contract use the local `resource:action` form. The action names are distinct grants: do not assume `manage` automatically includes `read` or another action.

Auth authenticates its console with its own session cookie and enforces tenant authorization internally. Its gateway routes are marked public to permit that authentication flow; this does not make administrative actions anonymous. User/group role assignment cannot grant permissions the actor lacks (owners have the documented exemption), and the last owner is protected. Tenant operations are reserved for platform operators.

[How to assign and verify permissions](architecture/security.html#assign-and-verify-permissions). Module roles and built-in grant mappings are defined in the linked manifest; review those mappings before assigning a broad role.

| Qualified permission | What it allows |
| --- | --- |
| `auth:profile:read` | See and manage the own account, sessions and second factor |
| `auth:users:manage` | Invite, deactivate and assign roles to users of the tenant |
| `auth:groups:manage` | Create groups, manage their members and the roles they grant |
| `auth:roles:manage` | Create and edit custom roles |
| `auth:policy:manage` | Edit the tenant sign-in policy |
| `auth:audit:read` | Read the tenant audit log |
| `auth:clients:manage` | Register OAuth client applications |
| `auth:directory:manage` | Connect LDAP directories, search them and import users as inactive |
| `auth:tenants:operate` | Create, suspend and inspect tenants (platform operators) |

### auth:profile:read

See and manage the own account, sessions and second factor.

**UI actions**: `read`, `update` on `Profile`, `Session`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Security.

The imported OpenAPI operations do not declare a matching `x-freya-permission` for this grant. Use the manifest and server authorization implementation to identify its enforcement; this absence does not indicate public access.

**Scope and additional checks**: Auth authenticates its console with its own session cookie and enforces tenant authorization internally. Its gateway routes are marked public to permit that authentication flow; this does not make administrative actions anonymous. User/group role assignment cannot grant permissions the actor lacks (owners have the documented exemption), and the last owner is protected. Tenant operations are reserved for platform operators.

### auth:users:manage

Invite, deactivate and assign roles to users of the tenant.

**UI actions**: `manage` on `User`, `Invitation`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Users.

The imported OpenAPI operations do not declare a matching `x-freya-permission` for this grant. Use the manifest and server authorization implementation to identify its enforcement; this absence does not indicate public access.

**Scope and additional checks**: Auth authenticates its console with its own session cookie and enforces tenant authorization internally. Its gateway routes are marked public to permit that authentication flow; this does not make administrative actions anonymous. User/group role assignment cannot grant permissions the actor lacks (owners have the documented exemption), and the last owner is protected. Tenant operations are reserved for platform operators.

### auth:groups:manage

Create groups, manage their members and the roles they grant.

**UI actions**: `manage` on `Group`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Groups.

The imported OpenAPI operations do not declare a matching `x-freya-permission` for this grant. Use the manifest and server authorization implementation to identify its enforcement; this absence does not indicate public access.

**Scope and additional checks**: Auth authenticates its console with its own session cookie and enforces tenant authorization internally. Its gateway routes are marked public to permit that authentication flow; this does not make administrative actions anonymous. User/group role assignment cannot grant permissions the actor lacks (owners have the documented exemption), and the last owner is protected. Tenant operations are reserved for platform operators.

### auth:roles:manage

Create and edit custom roles.

**UI actions**: `manage` on `Role`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Roles.

The imported OpenAPI operations do not declare a matching `x-freya-permission` for this grant. Use the manifest and server authorization implementation to identify its enforcement; this absence does not indicate public access.

**Scope and additional checks**: Auth authenticates its console with its own session cookie and enforces tenant authorization internally. Its gateway routes are marked public to permit that authentication flow; this does not make administrative actions anonymous. User/group role assignment cannot grant permissions the actor lacks (owners have the documented exemption), and the last owner is protected. Tenant operations are reserved for platform operators.

### auth:policy:manage

Edit the tenant sign-in policy.

**UI actions**: `manage` on `Policy`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Policy.

The imported OpenAPI operations do not declare a matching `x-freya-permission` for this grant. Use the manifest and server authorization implementation to identify its enforcement; this absence does not indicate public access.

**Scope and additional checks**: Auth authenticates its console with its own session cookie and enforces tenant authorization internally. Its gateway routes are marked public to permit that authentication flow; this does not make administrative actions anonymous. User/group role assignment cannot grant permissions the actor lacks (owners have the documented exemption), and the last owner is protected. Tenant operations are reserved for platform operators.

### auth:audit:read

Read the tenant audit log.

**UI actions**: `read` on `AuditEvent`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Audit.

The imported OpenAPI operations do not declare a matching `x-freya-permission` for this grant. Use the manifest and server authorization implementation to identify its enforcement; this absence does not indicate public access.

**Scope and additional checks**: Auth authenticates its console with its own session cookie and enforces tenant authorization internally. Its gateway routes are marked public to permit that authentication flow; this does not make administrative actions anonymous. User/group role assignment cannot grant permissions the actor lacks (owners have the documented exemption), and the last owner is protected. Tenant operations are reserved for platform operators.

### auth:clients:manage

Register OAuth client applications.

**UI actions**: `manage` on `ClientApplication`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Clients.

The imported OpenAPI operations do not declare a matching `x-freya-permission` for this grant. Use the manifest and server authorization implementation to identify its enforcement; this absence does not indicate public access.

**Scope and additional checks**: Auth authenticates its console with its own session cookie and enforces tenant authorization internally. Its gateway routes are marked public to permit that authentication flow; this does not make administrative actions anonymous. User/group role assignment cannot grant permissions the actor lacks (owners have the documented exemption), and the last owner is protected. Tenant operations are reserved for platform operators.

### auth:directory:manage

Connect LDAP directories, search them and import users as inactive.

**UI actions**: `manage` on `DirectoryConnection`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Directories.

The imported OpenAPI operations do not declare a matching `x-freya-permission` for this grant. Use the manifest and server authorization implementation to identify its enforcement; this absence does not indicate public access.

**Scope and additional checks**: Auth authenticates its console with its own session cookie and enforces tenant authorization internally. Its gateway routes are marked public to permit that authentication flow; this does not make administrative actions anonymous. User/group role assignment cannot grant permissions the actor lacks (owners have the documented exemption), and the last owner is protected. Tenant operations are reserved for platform operators.

### auth:tenants:operate

Create, suspend and inspect tenants (platform operators).

**UI actions**: `manage` on `Tenant`, `OperatorGrant`. These are the manifest’s CASL presentation rules.

**Navigation gated by this permission**: Tenants.

The imported OpenAPI operations do not declare a matching `x-freya-permission` for this grant. Use the manifest and server authorization implementation to identify its enforcement; this absence does not indicate public access.

**Scope and additional checks**: Auth authenticates its console with its own session cookie and enforces tenant authorization internally. Its gateway routes are marked public to permit that authentication flow; this does not make administrative actions anonymous. User/group role assignment cannot grant permissions the actor lacks (owners have the documented exemption), and the last owner is protected. Tenant operations are reserved for platform operators.
<div class="guide-actions"><a href="how-to/auth/docker.html">Install with Docker Compose →</a><a href="how-to/auth/native.html">Install without Docker →</a><a href="downloads/auth.zip">Download Compose bundle ↓</a></div>

## Dependencies and integration

**Required**: TimescaleDB, Valkey, OpenFGA, mesh identity.

**Optional or feature-dependent**: SMTP, LDAP directory.

Bootstrap requires `-operator-email`. Build the console both as a standalone console and a federated remote. OpenFGA store/model setup and signing-key state are part of Auth operations.

The list describes infrastructure/features, not every transitive library. Check the linked deployment reference for exact versions, enabled features and peer grants. [Framework dependencies](architecture/dependencies.html) cover the shared Go libraries.

## Runtime and operation

| Item | Reference |
| --- | --- |
| Service binary | `authsvc` |
| Public example configuration | `deploy/dev.yaml`; adapt endpoints and paths for your environment |
| Native source build | Go `1.26.3`, toolchain `go1.26.8`, Node 22 for UI |
| Image repository | `ghcr.io/go-tangra/go-tangra-auth`; choose a published compatible version |
| Private admin default | `127.0.0.1:9190`; check actual configuration |
| Health and readiness | `/healthz` and `/readyz` on the configured admin listener |
| Web integration | Gateway registration, permission grants and federated UI |

Bootstrap initializes or validates the module's own stores; serving still needs a valid workload identity, reachable dependencies and policy. Logs, readiness, gateway registration and module-specific checks are described in the detailed references below.

## Configuration field index

The following names and types come from the public Go configuration structures. Group names identify nested types, not flat YAML paths. Required values, defaults, cross-field checks and enabled-feature behavior are explained by the module's source/operations references; never assume every listed setting is optional.

| Configuration group | YAML key | Value type |
| --- | --- | --- |
| `Config` | `issuer` | `string` |
| `Config` | `edge` | `Edge` |
| `Config` | `db` | `DB` |
| `Config` | `valkey` | `Valkey` |
| `Config` | `openfga` | `OpenFGA` |
| `Config` | `kek` | `KEK` |
| `Config` | `email` | `Email` |
| `Config` | `token` | `Token` |
| `Config` | `session` | `Session` |
| `Config` | `gateway` | `Gateway` |
| `Config` | `profile` | `Profile` |
| `Config` | `mfa` | `MFA` |
| `Config` | `directory` | `Directory` |
| `Config` | `webauthn` | `WebAuthn` |
| `Directory` | `enabled` | `bool` |
| `Directory` | `allow_plaintext` | `bool` |
| `Directory` | `targets` | `DirectoryTargets` |
| `Directory` | `dial_timeout` | `time.Duration` |
| `Directory` | `max_size_limit` | `int` |
| `Directory` | `max_time_limit` | `time.Duration` |
| `Directory` | `rate_per_minute` | `int` |
| `Directory` | `max_connections_per_tenant` | `int` |
| `DirectoryTargets` | `deny_cidrs` | `[]string` |
| `DirectoryTargets` | `allow_cidrs` | `[]string` |
| `DirectoryTargets` | `allowed_ports` | `[]int` |
| `Gateway` | `enabled` | `bool` |
| `Gateway` | `service` | `string` |
| `Profile` | `avatar_max_bytes` | `int64` |
| `Profile` | `avatar_max_pixels` | `int64` |
| `Profile` | `avatar_size` | `int` |
| `Profile` | `avatar_decode_concurrency` | `int` |
| `Profile` | `lookup_rate_per_minute` | `int` |
| `MFA` | `issuer` | `string` |
| `Edge` | `addr` | `string` |
| `Edge` | `cert_file` | `string` |
| `Edge` | `key_file` | `string` |
| `Edge` | `allowed_origins` | `[]string` |
| `Edge` | `trusted_proxies` | `[]string` |
| `Edge` | `rate_limit` | `edge.RateLimit` |
| `DB` | `dsn` | `string` |
| `DB` | `migrate_dsn` | `string` |
| `DB` | `max_conns` | `int32` |
| `Valkey` | `addresses` | `[]string` |
| `Valkey` | `username` | `string` |
| `Valkey` | `password` | `string` |
| `Valkey` | `allow_plaintext` | `bool` |
| `Valkey` | `ca_file` | `string` |
| `OpenFGA` | `url` | `string` |
| `OpenFGA` | `preshared_key` | `string` |
| `OpenFGA` | `store_id` | `string` |
| `OpenFGA` | `allow_plaintext` | `bool` |
| `KEK` | `source` | `string` |
| `KEK` | `path` | `string` |
| `KEK` | `env` | `string` |
| `Email` | `transport` | `string` |
| `Email` | `host` | `string` |
| `Email` | `port` | `int` |
| `Email` | `username` | `string` |
| `Email` | `password` | `string` |
| `Email` | `from` | `string` |
| `Email` | `allow_plaintext` | `bool` |
| `Token` | `access_lifetime` | `time.Duration` |
| `Token` | `rotation_interval` | `time.Duration` |
| `Token` | `retiring_period` | `time.Duration` |
| `Token` | `clock_skew` | `time.Duration` |
| `Session` | `revocation_poll` | `time.Duration` |

[Configuration structures and validation](https://github.com/go-tangra/go-tangra-auth/blob/bb0045aa72dd1451d73a6ee2764c5d69ec9cc633/internal/config/config.go)

## API operation index

These operations are extracted from the module's OpenAPI contract. Read the source contract for request/response schemas, permission checks and exact route bases; internal mesh endpoints must not be treated as anonymous public APIs.

| Method | Contract path | Operation |
| --- | --- | --- |
| `GET` | `/.well-known/jwks.json` | Published verification keys |
| `GET` | `/api/v1/tenants/resolve` | Resolve a tenant slug before sign-in (never reveals existence beyond slug validity) |
| `POST` | `/api/v1/signin` | Sign in with email + password (+ tenant; omitted or blank → derived from the email domain) (step 1) |
| `POST` | `/api/v1/signin/mfa` | Complete sign-in with a TOTP or recovery code (step 2) |
| `POST` | `/api/v1/signin/mfa/webauthn/options` | Security-key request options for a pending sign-in (feature 018; the user's usable keys) |
| `POST` | `/api/v1/signin/mfa/webauthn` | Complete sign-in with a security-key assertion (step 2; failures count toward the lockout like a wrong code) |
| `POST` | `/api/v1/signout` | End the current session everywhere |
| `GET` | `/api/v1/session` | Current user, tenant, effective roles, display name and avatar (never phone) |
| `POST` | `/api/v1/session/token` | Mint a fresh access token from the live session |
| `GET` | `/api/v1/sessions` | List my live sessions (paged, sorted). Without any list parameter the bare array of the previous release is returned (one release). |
| `POST` | `/api/v1/sessions/{id}/revoke` | Revoke one of my sessions |
| `POST` | `/api/v1/me/password` | Change password (ends all other sessions) |
| `GET` | `/api/v1/me/password-policy` | Password rules of the caller's tenant (shown on the change-password form) |
| `POST` | `/api/v1/me/mfa/enroll` | Start TOTP enrolment (returns otpauth URI; not yet enabled) |
| `POST` | `/api/v1/me/mfa/confirm` | Confirm enrolment with a code; returns recovery codes once |
| `POST` | `/api/v1/me/mfa/disable` | Disable TOTP (requires current password + code; refused when tenant requires MFA) |
| `POST` | `/api/v1/me/mfa/recovery-codes` | Regenerate recovery codes |
| `GET` | `/api/v1/me/mfa` | My second factors (authenticator app, security keys, recovery codes left, tenant requirement) |
| `POST` | `/api/v1/me/mfa/webauthn/register/options` | Start registering a named security key (attestation none; my keys excluded) |
| `POST` | `/api/v1/me/mfa/webauthn/register` | Finish registering a security key; the first factor returns recovery codes once |
| `PATCH` | `/api/v1/me/mfa/webauthn/{id}` | Rename one of my security keys |
| `DELETE` | `/api/v1/me/mfa/webauthn/{id}` | Remove one of my security keys after confirming a current factor (code, recovery code or key assertion) |
| `POST` | `/api/v1/me/mfa/stepup/options` | Security-key request options that confirm a removal |
| `POST` | `/api/v1/recovery` | Request a password-recovery email (always 202) |
| `POST` | `/api/v1/recovery/complete` | Set a new password with a recovery token (single use) |
| `POST` | `/api/v1/recovery/password-policy` | Password rules for a still-valid reset token (not consumed; token in the body, never the URL; rate-limited) |
| `POST` | `/api/v1/invitations/accept` | Accept an invitation and set the initial password |
| `POST` | `/api/v1/invitations/password-policy` | Password rules for a still-redeemable invitation token (not consumed; token in the body, never the URL; no invitee data; rate-limited) |
| `GET` | `/api/v1/admin/users` | List users (admin); q matches email, first or last name; status=imported lists imported users; items carry avatar_url, groups, directory and invitation_id |
| `GET` | `/api/v1/admin/users/{id}` | One user of the tenant as the users list shows it (admin) |
| `POST` | `/api/v1/admin/invitations` | Invite a user with roles (admin) |
| `POST` | `/api/v1/admin/invitations/{id}/resend` | resendInvitation |
| `PUT` | `/api/v1/admin/users/{id}/roles` | Replace a user's roles (admin; cannot grant permissions the actor lacks; last-owner protected) |
| `POST` | `/api/v1/admin/users/{id}/deactivate` | deactivateUser |
| `POST` | `/api/v1/admin/users/{id}/reactivate` | reactivateUser |
| `POST` | `/api/v1/admin/users/activate` | Invite imported users (admin); roles and groups pass the escalation check once, before any invitation |
| `POST` | `/api/v1/admin/users/{id}/remove-imported` | Delete an imported user that was never activated (admin; no e-mail) |
| `POST` | `/api/v1/admin/users/{id}/sessions/revoke` | Force sign-out everywhere |
| `GET` | `/api/v1/admin/users/{id}/mfa` | A user's second-factor methods (admin; key names and use, never key material or credential ids) |
| `POST` | `/api/v1/admin/users/{id}/mfa/reset` | Remove a user's authenticator app, security keys and recovery codes and end their sessions (admin; not self, not a more privileged user) |
| `GET` | `/api/v1/roles` | Subject picker (feature 005): slug, display name, origin, module display name and retired flag of the tenant roles, any signed-in member |
| `GET` | `/api/v1/admin/roles` | List roles with permissions, origin (builtin, module, custom), module and retirement (feature 019); paged and sorted. Without any list parameter the bare array of the previous release is returned (one release). |
| `POST` | `/api/v1/admin/roles` | Create a custom role; permissions are qualified module:resource:action refs |
| `PUT` | `/api/v1/admin/roles/{id}` | Update a custom role's permissions (built-in and module roles are locked); legacy refs are accepted only if the role already holds them |
| `POST` | `/api/v1/admin/roles/{id}/remove` | Remove a custom role (unassigns everyone) |
| `POST` | `/api/v1/admin/roles/{id}/clone` | Copy any role but owner into a new custom role with its current permissions (legacy grants not copied); the caller must hold every permission (feature 019) |
| `GET` | `/api/v1/admin/permissions` | Permission catalogue grouped by module (feature 019): qualified ref, module, module display name, grantable for the caller; retired modules omitted; legacy rows flagged |
| `GET` | `/api/v1/admin/policy` | Tenant security policy |
| `PUT` | `/api/v1/admin/policy` | updatePolicy |
| `GET` | `/api/v1/admin/audit` | Tenant audit trail (filter by user, event_type, time), newest first. Without from/to the last 7 days are listed (to defaults to now, from to to minus 7 days). Legacy: cursor/limit alone keep the cursor shape plus total for one release; mixing both styles is validation_failed on cursor. |
| `GET` | `/api/v1/admin/clients` | Registered client applications (paged, sorted). Without any list parameter the bare array of the previous release is returned (one release). |
| `POST` | `/api/v1/admin/clients` | Register a client application (redirect URIs; returns secret once for confidential clients) |
| `GET` | `/api/v1/operator/tenants` | List tenants (operator; paged, sorted) |
| `POST` | `/api/v1/operator/tenants` | Create a tenant and invite its first owner |
| `GET` | `/api/v1/operator/tenants/{id}` | One tenant (operator) |
| `POST` | `/api/v1/operator/tenants/{id}/suspend` | suspendTenant |
| `POST` | `/api/v1/operator/tenants/{id}/reactivate` | reactivateTenant |
| `POST` | `/api/v1/operator/grants` | Create a time-limited, audited access grant into a tenant (SR-006) |
| `GET` | `/api/v1/me/profile` | Own profile including phone |
| `PUT` | `/api/v1/me/profile` | Update own names/phone (audited by field name only); success carries X-Freya-Identity-Refresh |
| `PUT` | `/api/v1/me/avatar` | Replace own avatar (raw image body PNG/JPEG/WebP up to 2 MiB; re-encoded server-side) |
| `DELETE` | `/api/v1/me/avatar` | removeMyAvatar |
| `GET` | `/api/v1/users/{id}/avatar/{avatar_id}` | Avatar bytes (image/jpeg, private immutable caching); 404 for other tenants, unknown ids and stale hashes |
| `GET` | `/api/v1/users` | Subject picker (feature 005): public profiles of active members of the caller tenant matching name or email (<= 20; same rate limit as lookups) |
| `POST` | `/api/v1/users/lookup` | Batch lookup of display name and avatar (same tenant; unknown ids omitted) |
| `GET` | `/api/v1/users/{id}` | Display name and avatar of a member of the caller's tenant (rate-limited; uniform 404) |
| `GET` | `/api/v1/admin/users/{id}/profile` | Any user's profile including phone (admin) |
| `PUT` | `/api/v1/admin/users/{id}/profile` | updateUserProfile |
| `DELETE` | `/api/v1/admin/users/{id}/avatar` | removeUserAvatar |
| `GET` | `/api/v1/admin/users/{id}/effective-roles` | Roles a user holds with their sources (direct / groups) |
| `GET` | `/api/v1/admin/users/{id}/groups` | userGroups |
| `GET` | `/api/v1/admin/groups` | Groups of the tenant with member counts and roles (admin; paged, sorted) |
| `POST` | `/api/v1/admin/groups` | createGroup |
| `GET` | `/api/v1/admin/groups/{id}` | getGroup |
| `PUT` | `/api/v1/admin/groups/{id}` | updateGroup |
| `POST` | `/api/v1/admin/groups/{id}/remove` | Delete a group; member_count must equal the current count |
| `GET` | `/api/v1/admin/groups/{id}/members` | Members of a group, latest first (paged, sorted). Legacy: cursor alone keeps {items, next} plus total for one release; mixing both styles is validation_failed on cursor. |
| `POST` | `/api/v1/admin/groups/{id}/members` | Add users (max 100); existing members are no-ops; escalation guard applies |
| `POST` | `/api/v1/admin/groups/{id}/members/{user_id}/remove` | removeGroupMember |
| `PUT` | `/api/v1/admin/groups/{id}/roles` | Replace the group's roles; cannot grant permissions the actor lacks (owners exempt) |
| `GET` | `/api/v1/admin/directories` | LDAP directory connections of the tenant (directory:manage; paged, sorted) |
| `POST` | `/api/v1/admin/directories` | Create a connection; the bind password is sealed and never returned (directory:manage) |
| `POST` | `/api/v1/admin/directories/test` | Test unsaved settings; connection_id without bind_password reuses that connection's stored password only for its own url, tls_mode and ca_pem (directory:manage) |
| `GET` | `/api/v1/admin/directories/{id}` | One connection including ca_pem (directory:manage) |
| `PUT` | `/api/v1/admin/directories/{id}` | Partial update; an omitted bind_password keeps the stored one unless url, tls_mode or ca_pem change (then validation_failed) (directory:manage) |
| `POST` | `/api/v1/admin/directories/{id}/remove` | Delete a connection; users already imported stay (directory:manage) |
| `POST` | `/api/v1/admin/directories/{id}/test` | Test a saved connection and record last_test (directory:manage) |
| `POST` | `/api/v1/admin/directories/{id}/search` | Preview directory entries under the connection base with their import status; nothing is written (directory:manage) |
| `POST` | `/api/v1/admin/directories/{id}/import` | Import the chosen entries (re-fetched by uid under the base) as inactive users (directory:manage) |
| `GET` | `/authorize` | OAuth 2.1 authorization endpoint (code + PKCE S256 only); renders the console sign-in |
| `POST` | `/api/v1/oauth/token` | Exchange an authorization code (+ code_verifier) for an access token |

[OpenAPI: api/openapi/console.yaml](https://github.com/go-tangra/go-tangra-auth/blob/bb0045aa72dd1451d73a6ee2764c5d69ec9cc633/api/openapi/console.yaml)

## Detailed source references

- [README.md](sources/auth/README.html) — captured at `bb0045aa72dd`.
- [docs/dependencies.md](sources/auth/docs/dependencies.html) — captured at `bb0045aa72dd`.
- [docs/operations.md](sources/auth/docs/operations.html) — captured at `bb0045aa72dd`.
- [docs/security-model.md](sources/auth/docs/security-model.html) — captured at `bb0045aa72dd`.

## Limits, diagnostics and recovery

Bootstrap requires `-operator-email`. Build the console both as a standalone console and a federated remote. OpenFGA store/model setup and signing-key state are part of Auth operations.

Use the module's operations/deployment reference for retention, backup/restore, refusal behavior, interface examples and feature limitations. The installation guides cover common readiness, identity, registration and storage failures.

## Upstream overview: go-tangra-auth

Tenant authentication and authorization service for the
[go-tangra v4 platform](https://github.com/go-tangra/go-tangra).

It signs users in through its own console, issues short-lived EdDSA tokens that
platform services verify offline, answers fine-grained authorization decisions
through OpenFGA, and gives tenant administrators and platform operators an
audited management surface: tenants, users, invitations, MFA and recovery,
roles, groups, user profiles and LDAP directory import.

Security model: [`docs/security-model.md`](sources/auth/docs/security-model.html).
Operations: [`docs/operations.md`](sources/auth/docs/operations.html).
Design history: `specs/002-tenant-auth-service`, `specs/004-groups-user-profiles`,
`specs/016-auth-ldap-import`.

## Place in the platform

```
go-tangra/go-tangra          platform module + @go-tangra/ui kit
        |
go-tangra-auth  <---->  go-tangra-portal (gateway)  <---->  modules (lcm, warden, ...)
```

- Built on `github.com/go-tangra/go-tangra/v4` (mTLS transports, identity,
  service policy, audit, observability).
- The portal gateway fronts the console and the browser API. Modules register
  their permissions with auth and verify tokens with the auth SDK.
- Registers with the gateway through the portal SDK
  (`github.com/go-tangra/go-tangra-portal/sdk/v4`).

## Modules in this repository

| Module | Path | Consumers |
|---|---|---|
| `github.com/go-tangra/go-tangra-auth/v4` | `/` | the service (`cmd/authsvc`) and `pkg/authmanifest` |
| `github.com/go-tangra/go-tangra-auth/sdk/v4` | `sdk/` | other services: the `auth.v1` protobuf API and `pkg/authclient` (offline JWT verification and revocation feed) |

The service builds against the in-repo SDK through
`replace github.com/go-tangra/go-tangra-auth/sdk/v4 => ./sdk`. Consumers use the
SDK's published `sdk/vX.Y.Z` tag.

## Layout

| Path | Purpose |
|------|---------|
| `cmd/authsvc` | service binary (serve, `bootstrap`, `version`) |
| `internal/app` | wiring: config, platform, stores, services, HTTP/gRPC |
| `internal/...` | sessions, tokens, passwords, MFA, invitations, tenants, authz, OAuth, directory import, and their SQL bindings |
| `console` | Vue 3 + FlyonUI console on `@go-tangra/ui` (served at `/console/`, plus a federated remote) |
| `api/openapi`, `sdk/api/proto` | contracts (`console.yaml`, `auth.v1`) |
| `deploy` | compose stack, dev configuration, policies |
| `tests/{contract,fuzz,integration}` | contract, fuzz and Docker-backed integration suites |

## Build and test

You need Go 1.26, Node 22, Docker (for integration tests and the image), and a
GitHub token with `read:packages` to install `@go-tangra/ui` from GitHub Packages.

```bash
go build ./... && go vet ./... && go test -race ./...
(cd sdk && go vet ./... && go test -race ./...)
make test-integration                     # -tags integration, needs Docker
make lint cover fuzz redaction-scan vuln

cd console
export NODE_AUTH_TOKEN=$(gh auth token)   # console/.npmrc only references this variable
npm ci && npm run lint && npm run test:unit && npm run build && npm run build:remote
```

The unit coverage gate requires at least 80 % overall and 100 % for the
security-critical packages. Generated code, SQL bindings and wiring are covered
by the integration suite instead.

## Run locally

```bash
make compose-up                           # TimescaleDB, Valkey, OpenFGA
go run ./cmd/authsvc bootstrap -config deploy/dev.yaml -operator-email ops@example.org
go run -tags "console remote" ./cmd/authsvc -config deploy/dev.yaml   # after the console build
```

## Container image

The image is `ghcr.io/go-tangra/go-tangra-auth`, built by `.github/workflows/ci.yaml`.

```bash
docker buildx build --secret id=npm_token,env=NODE_AUTH_TOKEN \
  --build-arg APP_VERSION=4.0.0 -t go-tangra-auth:dev .
docker run --rm go-tangra-auth:dev version
```

The image runs `authsvc -config deploy/dev.yaml` as user `app` (uid 10001).
Production deployments mount their own configuration.

## Versioning

- Service releases are tagged `vX.Y.Z`. CI publishes the image as `X.Y.Z`,
  `X.Y`, `X` and `sha-<short>`. There is no `latest` tag.
- The SDK is released separately with `sdk/vX.Y.Z` tags. These tags never build an image.
- v4.0.0 is the first release of this repository. It matches the go-tangra v4
  platform major version.
