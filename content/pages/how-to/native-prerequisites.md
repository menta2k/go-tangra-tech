# Native installation prerequisites

## Target environment

These instructions target a Linux host and the documented v4 module source revisions. Install Go **1.26.8**, Node **22**, npm, Git and a C toolchain when required by the module. Access to `@go-tangra/ui` on GitHub Packages needs a token with `read:packages`; export `NODE_AUTH_TOKEN` in the shell without committing it.

Native deployment means every required dependency is a native process or an existing managed service. Do not run `make compose-up`, testcontainers or Docker-backed integration targets for this path.

## Provision the stores before services

Use the dependency list and operations reference on the chosen module page. Install and start the required database, Valkey and any module-specific services through your Linux distribution or their supported native installation process. Managed endpoints are also suitable when the module's security and network requirements are met.

For modules requiring TimescaleDB, provision PostgreSQL with the TimescaleDB extension available. Create a module-owned database and separate migration and application roles. The following is a pattern; replace names and passwords with the exact module operations reference before executing it:

```sql
CREATE DATABASE module_database;
CREATE ROLE module_app LOGIN PASSWORD 'REPLACE_WITH_PRIVATE_PASSWORD' NOBYPASSRLS;
-- Connect to module_database as its migration owner before this statement:
CREATE EXTENSION IF NOT EXISTS timescaledb;
```

The migration role must own the required schema/objects; the application role must not bypass row-level security. Use `db.migrate_dsn` for bootstrap and `db.dsn` for runtime. Verify with a native `psql` connection that the database is reachable and the application role has `rolsuper = false` and `rolbypassrls = false`. [Scheduler's exact database requirements](sources/scheduler/deploy/README.html) demonstrate why the role must exist before migration.

For Valkey, configure the module's ACL user and event-stream permissions, then verify access with `valkey-cli` using your deployment's authentication method. For Auth, initialize OpenFGA and configure its store/model as described in [Auth operations](sources/auth/docs/operations.html). If a module requires S3, create the appropriate bucket and narrowly scoped credentials. Preserve these stores independently of binary upgrades.

## Bootstrap the native control plane

Build the [LCM native binary](how-to/lcm/native.html), [Auth](how-to/auth/native.html), and [Portal](how-to/portal/native.html) first. Set their native configuration files to your stores, trust domain, ports and file paths. Bootstrap runs before serving; it does not require every module to be running.

From the LCM checkout, after building `bin/lcmsvc`, provision the mesh root and initial identities with its documented bootstrap flags:

```sh
./bin/lcmsvc bootstrap -config /etc/go-tangra/lcm.yaml   -out /etc/go-tangra/identities -trust-domain example.org   -services gateway,auth,lcm
```

Replace `example.org` with the configured trust domain. Store the output where only the correct service accounts can read their private keys, and point each file-identity configuration at its certificate, key and bundle. Configure LCM's own identity/issuer and writable state according to [LCM operations](sources/lcm/docs/operations.html). Do not distribute the mesh root private key to workloads.

Next bootstrap Auth with its first operator email and Portal with the allow-list for the workload identities and route prefixes you will deploy. Start the control plane with the configured identities. [Gateway operations](sources/portal/docs/operations.html) and [module author guide](sources/portal/docs/module-guide.html) define registration grants and discovery targets. Follow [LCM enrollment](sources/lcm/docs/operations.html) to mint a single-use token for each additional workload, then persist its identity state for renewal/restart.

The platform's [enrollment reference](sources/platform/deploy/stack/ENROLLMENT.html) explains the trust relationships and API; its Compose exec wrappers belong to the Docker path. Use your native LCM client/SDK or authorized gateway API instead of those wrappers.

## Configure identity, secrets and paths

1. Copy the chosen module's public example YAML to a private native configuration file.
2. Replace container hostnames with real dependency endpoints and replace `/app`, `/certs`, `/secrets` and `/state` paths with host locations readable/writable by that service.
3. Set the service name and trust domain to match its SPIFFE identity. Configure file SVIDs, a real SPIRE workload socket, or LCM enrollment; none is a plaintext fallback.
4. Set discovery, gateway and Auth references to the actual mesh endpoints. Add reciprocal service policy grants and the gateway route allow-list.
5. Generate module-required encryption/signing keys through your secret-management process. Set file/environment references, not literal secrets in committed YAML.
6. Create writable enrollment/object-cache/ACME directories when configured. Restrict secret files to the service user and keep private admin listeners on loopback or authenticated mTLS.

[Framework configuration](architecture/configuration.html) documents identity, enrollment, discovery, admin and transport defaults. Module references add module-specific keys and operations requirements.

## Native integration exceptions

- **Warden**: initialize a native/managed Vault instance with the KV mount and AppRole described in [Warden operations](sources/warden/docs/operations.html).
- **Paperless**: use reachable S3 storage and configured native/managed Tika/Gotenberg extractors; configure authorization sharing according to [deployment notes](sources/paperless/deploy/README.html).
- **DNS**: use native/managed PowerDNS Authoritative and Recursor APIs. Disable Docker restart integration and restart PowerDNS through your host service manager.
- **Asterisk**: grant only SELECT to the PBX history source. If registration history is enabled, provision a separate module-owned MySQL database; bootstrap must never migrate the PBX database. Mount recordings read-only.
- **IPAM**: active ICMP scans require the appropriate host capability; configured IPMI/KVM/secret integrations need independent credentials and policy.
- **Signing / HR**: scheduled expiry/reminders/carry-over/reconciliation require Scheduler registration and execution grants; Signing also needs its object store and KEK.

## Verify prerequisites

Before starting the service, check every dependency from the service account, validate file permissions, confirm certificate validity/trust, and ensure intended ports are free. Then follow the module's bootstrap/start and health verification steps. A successful build does not establish that these dependencies are ready.
