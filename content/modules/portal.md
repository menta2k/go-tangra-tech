# Portal / Gateway

Public application edge, leased module registry and federated shell.

**Architecture role**: Control plane. [See the complete component map](architecture/index.html).

**Documented source**: `b473bb7a96e4` · nearest local service tag `v4.6.0` · v4 major. [Repository at this revision](https://github.com/go-tangra/go-tangra-portal/tree/b473bb7a96e4be87cd55f511880c67446c35e303). Tags are source metadata, not a claim of image publication or cross-module compatibility.


## Permissions and authorization

Portal registers and checks the permissions supplied by each module manifest; it does not declare a separate Portal user permission catalogue at this revision. It registers permission definitions on modules’ behalf; modules register their own roles and built-in grants. Route permission checks and UI abilities come from those manifests. [Permission synchronization source](https://github.com/go-tangra/go-tangra-portal/blob/b473bb7a96e4be87cd55f511880c67446c35e303/internal/app/permissions.go). See the [assignment and enforcement guide](architecture/security.html#assign-and-verify-permissions).
<div class="guide-actions"><a href="how-to/portal/docker.html">Install with Docker Compose →</a><a href="how-to/portal/native.html">Install without Docker →</a><a href="downloads/portal.zip">Download Compose bundle ↓</a></div>

## Dependencies and integration

**Required**: Auth, LCM or supplied SVID, TimescaleDB, Valkey.

**Optional or feature-dependent**: registered module remotes.

The service's logical mesh name is `gateway`, although its repository/image is Portal. Build with the `shell` tag. Bootstrap the allow-list before modules register; the edge needs its own browser certificate, separate from mesh SVIDs.

The list describes infrastructure/features, not every transitive library. Check the linked deployment reference for exact versions, enabled features and peer grants. [Framework dependencies](architecture/dependencies.html) cover the shared Go libraries.

## Runtime and operation

| Item | Reference |
| --- | --- |
| Service binary | `gatewaysvc` |
| Public example configuration | `deploy/dev.yaml`; adapt endpoints and paths for your environment |
| Native source build | Go `1.26.3`, toolchain `go1.26.8`, Node 22 for UI |
| Image repository | `ghcr.io/go-tangra/go-tangra-portal`; choose a published compatible version |
| Private admin default | `127.0.0.1:9290`; check actual configuration |
| Health and readiness | `/healthz` and `/readyz` on the configured admin listener |
| Web integration | Gateway registration, permission grants and federated UI |

Bootstrap initializes or validates the module's own stores; serving still needs a valid workload identity, reachable dependencies and policy. Logs, readiness, gateway registration and module-specific checks are described in the detailed references below.

## Configuration field index

The following names and types come from the public Go configuration structures. Group names identify nested types, not flat YAML paths. Required values, defaults, cross-field checks and enabled-feature behavior are explained by the module's source/operations references; never assume every listed setting is optional.

| Configuration group | YAML key | Value type |
| --- | --- | --- |
| `Config` | `public_origin` | `string` |
| `Config` | `edge` | `Edge` |
| `Config` | `db` | `DB` |
| `Config` | `valkey` | `Valkey` |
| `Config` | `auth` | `Auth` |
| `Config` | `leases` | `Leases` |
| `Config` | `forward` | `Forward` |
| `Config` | `operators` | `Operators` |
| `Config` | `enroll` | `Enroll` |
| `Config` | `console` | `Console` |
| `Enroll` | `enabled` | `bool` |
| `Enroll` | `enroll_url` | `string` |
| `Enroll` | `lcm_grpc` | `string` |
| `Enroll` | `tenant_id` | `string` |
| `Enroll` | `token_file` | `string` |
| `Enroll` | `state_file` | `string` |
| `Edge` | `addr` | `string` |
| `Edge` | `cert_file` | `string` |
| `Edge` | `key_file` | `string` |
| `Edge` | `allowed_origins` | `[]string` |
| `Edge` | `trusted_proxies` | `[]string` |
| `Edge` | `rate_limit` | `edge.RateLimit` |
| `Edge` | `frame_sources` | `[]string` |
| `Edge` | `connect_sources` | `[]string` |
| `DB` | `dsn` | `string` |
| `DB` | `migrate_dsn` | `string` |
| `DB` | `max_conns` | `int32` |
| `Valkey` | `addresses` | `[]string` |
| `Valkey` | `username` | `string` |
| `Valkey` | `password` | `string` |
| `Valkey` | `allow_plaintext` | `bool` |
| `Valkey` | `ca_file` | `string` |
| `Auth` | `service` | `string` |
| `Auth` | `issuer` | `string` |
| `Auth` | `audience` | `string` |
| `Leases` | `ttl` | `time.Duration` |
| `Leases` | `renew` | `time.Duration` |
| `Forward` | `body_bytes` | `int64` |
| `Forward` | `streams_per_client` | `int` |
| `Forward` | `stream_max` | `time.Duration` |
| `Forward` | `module_timeout` | `time.Duration` |
| `Operators` | `roles` | `[]string` |

[Configuration structures and validation](https://github.com/go-tangra/go-tangra-portal/blob/b473bb7a96e4be87cd55f511880c67446c35e303/internal/config/config.go)

## API operation index

These operations are extracted from the module's OpenAPI contract. Read the source contract for request/response schemas, permission checks and exact route bases; internal mesh endpoints must not be treated as anonymous public APIs.

| Method | Contract path | Operation |
| --- | --- | --- |
| `GET` | `/gateway/v1/me` | Identity of the caller (session or bearer) with display name and avatar |
| `GET` | `/gateway/v1/me/modules` | Registered modules visible to the caller with remote entries and navigation |
| `GET` | `/gateway/v1/me/abilities` | CASL rules derived from the caller API permissions, per module |
| `GET` | `/gateway/v1/events` | Server-sent events for registry and ability version changes (shell refetch trigger) |
| `GET` | `/gateway/v1/stream` | Per-signed-in-user SSE bus: realtime events any module publishes to the shared platform stream |
| `GET` | `/gateway/v1/ops/registrations` | Every registration with health and traffic (operators) |
| `POST` | `/gateway/v1/ops/registrations/{module}/drain` | drainModule |
| `POST` | `/gateway/v1/ops/registrations/{module}/undrain` | undrainModule |
| `POST` | `/gateway/v1/ops/registrations/{module}/revoke` | revokeModule |
| `GET` | `/gateway/v1/ops/allowlist` | listAllowlist |
| `POST` | `/gateway/v1/ops/allowlist` | addAllowlist |
| `POST` | `/gateway/v1/ops/allowlist/{id}/revoke` | revokeAllowlist |
| `GET` | `/gateway/v1/ops/audit` | gatewayAudit |
| `GET` | `/m/{module}/{asset}` | Federated remote assets relayed from the module (immutable caching for hashed assets; mf-manifest.json no-store) |

[OpenAPI: api/openapi/gateway.yaml](https://github.com/go-tangra/go-tangra-portal/blob/b473bb7a96e4be87cd55f511880c67446c35e303/api/openapi/gateway.yaml)

## Detailed source references

- [README.md](sources/portal/README.html) — captured at `b473bb7a96e4`.
- [docs/dependencies.md](sources/portal/docs/dependencies.html) — captured at `b473bb7a96e4`.
- [docs/module-guide.md](sources/portal/docs/module-guide.html) — captured at `b473bb7a96e4`.
- [docs/operations.md](sources/portal/docs/operations.html) — captured at `b473bb7a96e4`.
- [docs/security-model.md](sources/portal/docs/security-model.html) — captured at `b473bb7a96e4`.

## Limits, diagnostics and recovery

The service's logical mesh name is `gateway`, although its repository/image is Portal. Build with the `shell` tag. Bootstrap the allow-list before modules register; the edge needs its own browser certificate, separate from mesh SVIDs.

Use the module's operations/deployment reference for retention, backup/restore, refusal behavior, interface examples and feature limitations. The installation guides cover common readiness, identity, registration and storage failures.

## Upstream overview: go-tangra-portal

The application gateway of the [go-tangra v4 platform](https://github.com/go-tangra/go-tangra):
the platform's edge, its module registry and the shell UI.

- **Edge.** The gateway is the only public listener. Browsers and API clients talk to it;
  it verifies sessions and bearer tokens with the auth service, decides permissions, and
  forwards HTTP, gRPC and gRPC-Web calls to modules over their pinned mTLS channel.
- **Module registry.** Modules stay private. They register their routes, gRPC methods,
  API permissions and CASL abilities with `gateway.v1.Registry` (Register / Renew /
  Deregister / Watch) under a lease, and only SPIFFE identities on the allow-list may do so.
- **Shell UI.** The gateway embeds the Vue 3 + FlyonUI Module Federation host (`shell/`,
  built on `@go-tangra/ui`), which composes every registered module's UI remote.

Security model: [`docs/security-model.md`](sources/portal/docs/security-model.html).
Operations: [`docs/operations.md`](sources/portal/docs/operations.html).
Module authors: [`docs/module-guide.md`](sources/portal/docs/module-guide.html).
Dependencies: [`docs/dependencies.md`](sources/portal/docs/dependencies.html).
Design history: `specs/003-application-gateway`.

> v4.0.0 replaces the v3 go-tangra portal with this gateway. The v3 portal stays on the
> `v3` branch and its `v3.x` tags (and images).

## Place in the platform

```
go-tangra/go-tangra          platform module + @go-tangra/ui kit
        |
go-tangra-auth  <---->  go-tangra-portal (gateway)  <---->  go-tangra-lcm
                                  ^
        warden, inventory, notification, paperless, deployer, ipam, ticket, asset, dns
        (register through the portal sdk and ship their UI as federated remotes)
```

- Built on `github.com/go-tangra/go-tangra/v4` (mTLS transports, identity, service
  policy, audit, observability).
- Exchanges sessions and verifies tokens through the auth SDK
  (`github.com/go-tangra/go-tangra-auth/sdk/v4`).
- Enrolls for its own SVID with lcm (`github.com/go-tangra/go-tangra-lcm/sdk/v4`).

## Modules in this repository

| Module | Path | Consumers |
|---|---|---|
| `github.com/go-tangra/go-tangra-portal/v4` | `/` | the gateway (`cmd/gatewaysvc`) and `examples/hello-module` |
| `github.com/go-tangra/go-tangra-portal/sdk/v4` | `sdk/` | every module: the `gateway.v1` protobuf API, the manifest schema and `pkg/gatewayclient` (manifest builder, registration loop) |

The gateway builds against the in-repo SDK through
`replace github.com/go-tangra/go-tangra-portal/sdk/v4 => ./sdk`. Modules use the
SDK's published `sdk/vX.Y.Z` tag.

## Layout

| Path | Purpose |
|------|---------|
| `cmd/gatewaysvc` | binary (serve, `bootstrap` seeds the allow-list, `version`) |
| `internal/registry` | registrations, leases, marks, allow-list, route snapshot |
| `internal/httpapi` | edge handler: dispatcher, shell/ops API, SSE, remote relay |
| `internal/identity`, `internal/authz` | session exchange / bearer verification; permission decisions and CASL abilities |
| `internal/proxy/{httpproxy,grpcproxy,grpcweb}` | forwarding over the pinned mTLS channel |
| `internal/health` | probes and circuit breaking |
| `api/openapi/gateway.yaml` | shell and operations API under `/gateway/v1` |
| `sdk/api/proto/gateway/v1`, `sdk/api/schema` | registry API and module manifest contract |
| `shell/` | Module Federation host, embedded with `-tags shell` |
| `examples/hello-module` | smallest complete module (API + remote UI) |
| `deploy` | development compose stack, dev configuration, allow-list policies |
| `tests/{contract,fuzz,integration}` | contract, fuzz and Docker-backed integration suites |

## Build and test

You need Go 1.26, Node 22, Docker (for integration tests and the image), `buf`, and a
GitHub token with `read:packages` to install `@go-tangra/ui` from GitHub Packages.

```bash
go build ./... && go vet ./... && go test -race ./...
(cd sdk && go vet ./... && go test -race ./...)
for d in sdk examples/hello-module internal/proxy/grpcproxy/echov1; do (cd $d && buf lint); done
make test-integration                     # -tags integration, needs Docker and a go-tangra-auth checkout
make lint cover fuzz redaction-scan perf-gate vuln

cd shell
export NODE_AUTH_TOKEN=$(gh auth token)   # shell/.npmrc only references this variable
npm ci && npm run lint && npm run test:unit && npm run build
```

The integration harness runs the auth service as a subprocess. It builds `authsvc` from
a go-tangra-auth checkout: `../go-tangra-auth` next to this repository by default, or the
directory named by `GO_TANGRA_AUTH_DIR`.

The unit coverage gate requires at least 80 % overall and 100 % for the security
packages. Generated code, SQL bindings and wiring are covered by the integration suite.

## Run locally

`deploy/dev.yaml` reads its SVID from `../../.dev/ca`. Create a throw-away CA there with
the platform's development CA tool:

```bash
go run github.com/go-tangra/go-tangra/v4/cmd/freya-devca@v4.0.0 \
  -out ../../.dev/ca -trust-domain example.org -services gateway,auth,hello
make compose-up                           # TimescaleDB, Valkey, OpenFGA, Mailpit
## Upstream overview: in a go-tangra-auth checkout: authsvc bootstrap and serve with -config deploy/gateway-mode.yaml, then:
go run ./cmd/gatewaysvc bootstrap -config deploy/dev.yaml \
  -allow "spiffe://example.org/svc/auth=/api/v1,/authorize,/.well-known,/console;auth" \
  -allow "spiffe://example.org/svc/hello=/api/hello;hello"
(cd shell && npm ci && npm run build) && go run -tags shell ./cmd/gatewaysvc -config deploy/dev.yaml &
(cd examples/hello-module/ui && npm ci && npm run build) && go run -tags ui ./examples/hello-module -config deploy/hello.yaml &
open https://localhost:8443/
```

The full platform stack (every service, lcm-issued identities) lives in the platform
repository under `deploy/stack`.

## Container image

The image is `ghcr.io/go-tangra/go-tangra-portal`, built by `.github/workflows/ci.yaml`.
It carries `gatewaysvc` with the embedded shell.

```bash
docker buildx build --secret id=npm_token,env=NODE_AUTH_TOKEN \
  --build-arg APP_VERSION=4.0.0 -t go-tangra-portal:dev .
docker run --rm go-tangra-portal:dev version
```

The image runs `gatewaysvc -config deploy/dev.yaml` as user `app` (uid 10001), with
`deploy/` (configuration and allow-list policies, no key material) at `/app/deploy`.
Deployments mount their own configuration, edge certificate and enrollment token.

## Versioning

- Service releases are tagged `vX.Y.Z`. CI publishes the image as `X.Y.Z`, `X.Y`, `X`
  and `sha-<short>`. There is no `latest` tag.
- The SDK is released separately with `sdk/vX.Y.Z` tags. These tags never build an image.
- v4.0.0 rebuilds the portal as the go-tangra v4 gateway. The v3 portal stays on the
  `v3` branch and its `v3.x` tags.
