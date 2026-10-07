# Install DNS without Docker

Run `dnssvc` as a Linux host process connected to native or managed dependencies. This guide uses source revision `10f9be2df98b` (v4); it does not require Docker at any step.

## Prerequisites and dependencies

Complete [native prerequisites](how-to/native-prerequisites.html), including Go `1.26.8`, Node 22 for the UI, a GitHub Packages token and a bootstrapped control plane. For the initial control plane installation, build the binaries first, then follow the prerequisites' bootstrap sequence before serving.

**Required**: TimescaleDB, Valkey, PowerDNS APIs, key-encryption key, Auth, Portal, mesh identity.

**Optional or feature-dependent**: IPAM, Prometheus, Docker restart integration.

Provision these dependencies without containers, using the module's detailed reference for role/schema/ACL/bucket setup. [Module reference](modules/dns.html).

PowerDNS Authoritative and Recursor must have reachable authenticated APIs. Docker restart integration uses a root-equivalent host socket and allow-listed container names. For native installation, disable that integration and manage PowerDNS through host services.

## Obtain and build

From a directory where you keep source checkouts:

```sh
git clone https://github.com/go-tangra/go-tangra-dns.git go-tangra-dns
cd go-tangra-dns
git checkout 10f9be2df98b2476c2029afcbeb8dec622b30788
export GOWORK=off
go mod download
```

Export `NODE_AUTH_TOKEN` securely with GitHub Packages read access, then build the frontend and embedded service:

```sh
cd ui
npm ci
npm run build
cd ..
go build -tags "ui" -o bin/dnssvc ./cmd/dnssvc
```

Expected: the UI build succeeds and `bin/dnssvc` is produced. Check `./bin/dnssvc version`. A source-built binary without release ldflags may report a development version; do not interpret it as proof of a published release.

## Configure the native service

```sh
cp deploy/dev.yaml native.yaml
chmod 600 native.yaml
```

Edit `native.yaml` before bootstrap. Replace example credentials and container paths/hostnames; set database/application/migration roles, any event/object stores, identity and trust bundle, secret references, discovery and gateway targets, and writable state. The [configuration index](modules/dns.html) identifies module keys; [native prerequisites](how-to/native-prerequisites.html) covers common paths and identity setup. Do not expect the unedited development YAML to work on your host.

Use the matching service account for runtime and ensure it can read only its own secrets and write its state. Required dependency connections must be reachable from that account. Keep admin and mesh listeners private.

Disable the Docker restart feature in native YAML; use PowerDNS's host service manager for restart. Configure PowerDNS API keys through private file/environment references.

## Bootstrap and start

After configuring dependencies, identity and peer grants:

```sh
./bin/dnssvc bootstrap -config native.yaml
./bin/dnssvc -config native.yaml
```

Expected: bootstrap exits successfully after its documented initialization/validation; serving starts without configuration/identity errors. Run the service in the foreground for the first verification. For a durable deployment, install the binary/configuration under your service manager with the same account, working directory, paths and environment.

## Verify installation

On the service host, if you retained the loopback admin default:

```sh
curl --fail http://127.0.0.1:9850/healthz
curl --fail http://127.0.0.1:9850/readyz
```

Expected: successful HTTP status from both checks and the documented readiness fields indicating available required dependencies. Change the address if your configuration differs. A non-loopback admin listener requires the authenticated transport configured by the framework; do not probe it as plain public HTTP.

Then check the workload's registration state, sign into the gateway with a user holding the module's permissions, and open DNS. Expected: the module is registered and the authorized view loads. Perform a small module-specific read operation described in its [reference](modules/dns.html). For configured optional integrations, verify those separately; base readiness does not establish every external feature.

## Troubleshooting

| Symptom | Check and corrective action |
| --- | --- |
| Bootstrap fails or database is unreachable | Check the dependency endpoint, migration credentials, pre-created app role, database ownership and required extensions; fix these before retrying bootstrap. |
| Invalid or missing identity | Confirm trust domain, cert/key/bundle or enrollment token paths and permissions. Persist enrollment state; a used token must be replaced, not replayed. |
| Module absent from the gateway | Check SPIFFE identity, granted route prefix, module readiness, gateway discovery and registry lease. Configure reciprocal Auth/LCM/module service policy. |
| Permission denied | Check user tenant, module permission/role and resource relationships; a service identity alone does not grant user permissions. |
| Sealed data cannot be opened after restore | Restore the matching encryption key along with the module database. Do not generate a replacement key for existing sealed data. |
| Port already in use or state unwritable | Adjust the configuration and discovery consistently; give only the service account write access to its own state directories. |
| Optional integration does not work | Review the module-specific configuration and peer policy; verify the external system from the service environment. |

PowerDNS Authoritative and Recursor must have reachable authenticated APIs. Docker restart integration uses a root-equivalent host socket and allow-listed container names. For native installation, disable that integration and manage PowerDNS through host services.

## Stop and remove

For the foreground run, press Ctrl+C and confirm the process exits. Under a service manager, stop and disable the configured module unit. Remove the installed binary/configuration only after checking that no other service uses those files.

Stopping or removing the binary does not delete database records, objects or identities. Back up the module database, required encryption/signing keys, blobs and enrollment state before deliberately removing them. Retiring the service also requires revoking its identity and removing its gateway/policy grants; preserve the shared control plane for other modules.

## Sources and scope

[Module README](sources/dns/README.html) · [Module configuration and interfaces](modules/dns.html) · [Source Makefile](https://github.com/go-tangra/go-tangra-dns/blob/10f9be2df98b2476c2029afcbeb8dec622b30788/Makefile) · [Source Dockerfile](https://github.com/go-tangra/go-tangra-dns/blob/10f9be2df98b2476c2029afcbeb8dec622b30788/Dockerfile)

- [Detailed deploy/README.md](sources/dns/deploy/README.html).

Commands follow the recorded source contracts; host/path adaptations are explained here. Clean-environment deployment acceptance and compatible published image combinations have not yet been established for this documentation snapshot.
