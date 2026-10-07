# Install Inventory without Docker

Run `inventorysvc` as a Linux host process connected to native or managed dependencies. This guide uses source revision `cfa3a28445fc` (v4); it does not require Docker at any step.

## Prerequisites and dependencies

Complete [native prerequisites](how-to/native-prerequisites.html), including Go `1.26.8`, Node 22 for the UI, a GitHub Packages token and a bootstrapped control plane. For the initial control plane installation, build the binaries first, then follow the prerequisites' bootstrap sequence before serving.

**Required**: TimescaleDB, Valkey, Auth, Portal, mesh identity.

**Optional or feature-dependent**: endpoint agents, LCM certificate delivery.

Provision these dependencies without containers, using the module's detailed reference for role/schema/ACL/bucket setup. [Module reference](modules/inventory.html).

Endpoint agents need their own enrollment and reporting configuration. Consumer access to host reports requires the documented consumer allow-list and matching service policy; it is not inherited from UI permissions.

## Obtain and build

From a directory where you keep source checkouts:

```sh
git clone https://github.com/go-tangra/go-tangra-inventory.git go-tangra-inventory
cd go-tangra-inventory
git checkout cfa3a28445fc7d175b900df81aecdac0dd6d9707
export GOWORK=off
go mod download
```

Export `NODE_AUTH_TOKEN` securely with GitHub Packages read access, then build the frontend and embedded service:

```sh
cd ui
npm ci
npm run build
cd ..
go build -tags "ui" -o bin/inventorysvc ./cmd/inventorysvc
```

Expected: the UI build succeeds and `bin/inventorysvc` is produced. Check `./bin/inventorysvc version`. A source-built binary without release ldflags may report a development version; do not interpret it as proof of a published release.

## Configure the native service

```sh
cp deploy/dev.yaml native.yaml
chmod 600 native.yaml
```

Edit `native.yaml` before bootstrap. Replace example credentials and container paths/hostnames; set database/application/migration roles, any event/object stores, identity and trust bundle, secret references, discovery and gateway targets, and writable state. The [configuration index](modules/inventory.html) identifies module keys; [native prerequisites](how-to/native-prerequisites.html) covers common paths and identity setup. Do not expect the unedited development YAML to work on your host.

Use the matching service account for runtime and ensure it can read only its own secrets and write its state. Required dependency connections must be reachable from that account. Keep admin and mesh listeners private.

## Bootstrap and start

After configuring dependencies, identity and peer grants:

```sh
./bin/inventorysvc bootstrap -config native.yaml
./bin/inventorysvc -config native.yaml
```

Expected: bootstrap exits successfully after its documented initialization/validation; serving starts without configuration/identity errors. Run the service in the foreground for the first verification. For a durable deployment, install the binary/configuration under your service manager with the same account, working directory, paths and environment.

## Verify installation

On the service host, if you retained the loopback admin default:

```sh
curl --fail http://127.0.0.1:9810/healthz
curl --fail http://127.0.0.1:9810/readyz
```

Expected: successful HTTP status from both checks and the documented readiness fields indicating available required dependencies. Change the address if your configuration differs. A non-loopback admin listener requires the authenticated transport configured by the framework; do not probe it as plain public HTTP.

Then check the workload's registration state, sign into the gateway with a user holding the module's permissions, and open Inventory. Expected: the module is registered and the authorized view loads. Perform a small module-specific read operation described in its [reference](modules/inventory.html). For configured optional integrations, verify those separately; base readiness does not establish every external feature.

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

Endpoint agents need their own enrollment and reporting configuration. Consumer access to host reports requires the documented consumer allow-list and matching service policy; it is not inherited from UI permissions.

## Stop and remove

For the foreground run, press Ctrl+C and confirm the process exits. Under a service manager, stop and disable the configured module unit. Remove the installed binary/configuration only after checking that no other service uses those files.

Stopping or removing the binary does not delete database records, objects or identities. Back up the module database, required encryption/signing keys, blobs and enrollment state before deliberately removing them. Retiring the service also requires revoking its identity and removing its gateway/policy grants; preserve the shared control plane for other modules.

## Sources and scope

[Module README](sources/inventory/README.html) · [Module configuration and interfaces](modules/inventory.html) · [Source Makefile](https://github.com/go-tangra/go-tangra-inventory/blob/cfa3a28445fc7d175b900df81aecdac0dd6d9707/Makefile) · [Source Dockerfile](https://github.com/go-tangra/go-tangra-inventory/blob/cfa3a28445fc7d175b900df81aecdac0dd6d9707/Dockerfile)

- [Detailed deploy/README.md](sources/inventory/deploy/README.html).

Commands follow the recorded source contracts; host/path adaptations are explained here. Clean-environment deployment acceptance and compatible published image combinations have not yet been established for this documentation snapshot.
