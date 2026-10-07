#!/usr/bin/env python3
"""Generate source-derived module references and installation guide drafts.

Explicit maintenance command; normal site builds consume the checked-in Markdown.
Review the generated adaptations before approving a release.
"""
import html
import json
import posixpath
import re
from pathlib import Path
from urllib.parse import urlsplit
from permission_content import permission_section
from key_documentation import key_documentation
from existing_core_guide import guide as existing_core_guide

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

EXCEPTIONS = {
    "auth": "Bootstrap requires `-operator-email`. Build the console both as a standalone console and a federated remote. OpenFGA store/model setup and signing-key state are part of Auth operations.",
    "portal": "The service's logical mesh name is `gateway`, although its repository/image is Portal. Build with the `shell` tag. Bootstrap the allow-list before modules register; the edge needs its own browser certificate, separate from mesh SVIDs.",
    "lcm": "LCM bootstraps the persistent mesh root. The `bootstrap -out … -services …` mode exports initial identities; preserve the database and KEK together. Public ACME certificates and mesh SVIDs serve different purposes.",
    "warden": "Initialize the Vault KV mount, AppRole and policy before serving. Preserve the KEK with database backups. The gateway's configured body limits must accommodate Warden operations.",
    "notification": "SMTP is the implemented delivery provider in this source snapshot. Do not treat future channel types as available providers. Configure and test the SMTP channel before expecting delivery.",
    "scheduler": "This module is absent from the recorded base platform Compose file. Create its `scheduler_app` role with LOGIN and NOBYPASSRLS before migrations; migrations grant to that existing role. No KEK is required. Configure both task-registration and executor policies.",
    "inventory": "Endpoint agents need their own enrollment and reporting configuration. Consumer access to host reports requires the documented consumer allow-list and matching service policy; it is not inherited from UI permissions.",
    "ipam": "ICMP scanning needs `CAP_NET_RAW`; Docker deployments need the corresponding container capability. Host sync needs a compatible Inventory version and its host-report consumer/policy grants. IPMI/KVM and Warden integrations are configured separately.",
    "dns": "PowerDNS Authoritative and Recursor must have reachable authenticated APIs. Docker restart integration uses a root-equivalent host socket and allow-listed container names. For native installation, disable that integration and manage PowerDNS through host services.",
    "deployer": "Configure only the target types and credentials you need. A successful LCM issuance does not prove a target delivery succeeded; check each target's result and its connectivity independently.",
    "asset": "Configure object storage for photos. Paperless is enabled by default in the documented integration; disable it explicitly if unused. Inventory sync and scheduled sync need reciprocal module policy and consumer grants.",
    "paperless": "Configure S3-compatible object storage and extraction providers. Database exports do not include every blob. Review sharing/OpenFGA configuration and extractor connectivity before validating document search.",
    "ticket": "The inbound mail listener is a separate edge with a relay token. Configure mailboxes and SMTP/notification delivery before testing conversations; do not expose the private module API or admin listener as the mail edge.",
    "signing": "Configure S3 storage, KEK and the tenant signing CA lifecycle. Expiry/reminder tasks depend on Scheduler integration; a source build alone does not enable them. Qualified signatures require the user's B-Trust BISS/card environment.",
    "hr": "The image is `go-tangra-hr` although the local checkout is `hr-service-v4`. Signing-required absence types depend on compatible Signing templates, event consumers and reconciliation; configure Notification and Scheduler where used.",
    "sms-gw": "This module is absent from the base platform stack. Its own Compose manifest supplies development PostgreSQL/carrier/callback fixtures and an optional service profile, not the whole control plane. Supply separate KEK and Hermes JWT secrets. Public Hermes TLS and mesh identity are independent.",
    "asterisk": "This read-only observer binds one PBX to one tenant. Grant SELECT only on the PBX source. Registration history, if enabled, writes to a separate module-owned MySQL database. Recordings are read-only. The supplied Compose file needs an existing mesh network; a systemd unit is supplied for native deployment.",
}

def source_link(m, path):
    return f"sources/{m['id']}/{posixpath.splitext(path)[0]}.html"

def upstream(m, path):
    return f"{m['repository']}/blob/{m['commit']}/{path}"

def adapt_markdown(m, text, document="README.md"):
    source_paths = {d["path"] for d in m["sources"]}
    def link(match):
        label, value = match[1], match[2]
        parsed = urlsplit(value)
        if parsed.scheme or value.startswith("#"):
            # Local fragments from the README retain their ids when appended.
            return match[0]
        path = posixpath.normpath(posixpath.join(posixpath.dirname(document), parsed.path))
        destination = source_link(m, path) if path in source_paths else upstream(m, path)
        if parsed.fragment:
            destination += "#" + parsed.fragment
        return f"[{label}]({destination})"
    text = re.sub(r"\[([^\]]+)\]\(([^\s)]+)\)", link, text)
    text = re.sub(r"^# (.+)$", r"## Upstream overview: \1", text, flags=re.M)
    return text

def write(path, text):
    dest = CONTENT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text)

def reference(m):
    id_ = m["id"]
    text = f"# {m['name']}\n\n{m['summary']}\n\n"
    text += f"**Architecture role**: {m['category']}. [See the complete component map](architecture/index.html).\n\n"
    text += f"**Documented source**: `{m['commit'][:12]}` · nearest local service tag `{m['tag']}` · v4 major. [Repository at this revision]({m['repository']}/tree/{m['commit']}). Tags are source metadata, not a claim of image publication or cross-module compatibility.\n\n"
    text += permission_section(m)
    if m["binary"]:
        text += f'''<div class="guide-actions"><a href="how-to/{id_}/docker.html">Install with Docker Compose →</a><a href="how-to/{id_}/native.html">Install without Docker →</a><a href="downloads/{id_}.zip">Download Compose bundle ↓</a></div>

## Dependencies and integration

**Required**: {', '.join(m['required'])}.

**Optional or feature-dependent**: {', '.join(m['optional']) if m['optional'] else 'No additional optional dependency is identified in this summary; see the detailed source reference for supported integrations'}.

{EXCEPTIONS[id_]}

The list describes infrastructure/features, not every transitive library. Check the linked deployment reference for exact versions, enabled features and peer grants. [Framework dependencies](architecture/dependencies.html) cover the shared Go libraries.

## Runtime and operation

| Item | Reference |
| --- | --- |
| Service binary | `{m['binary']}` |
| Public example configuration | `{m['config_path']}`; adapt endpoints and paths for your environment |
| Native source build | Go `{m['go_version']}`, toolchain `{m['toolchain']}`, Node 22 for UI |
| Image repository | `{m['image']}`; choose a published compatible version |
| Private admin default | `127.0.0.1:{m['admin_port']}`; check actual configuration |
| Health and readiness | `/healthz` and `/readyz` on the configured admin listener |
| Web integration | Gateway registration, permission grants and federated UI |

Bootstrap initializes or validates the module's own stores; serving still needs a valid workload identity, reachable dependencies and policy. Logs, readiness, gateway registration and module-specific checks are described in the detailed references below.

## Configuration field index

The following names and types come from the public Go configuration structures. Group names identify nested types, not flat YAML paths. Required values, defaults, cross-field checks and enabled-feature behavior are explained by the module's source/operations references; never assume every listed setting is optional.

| Configuration group | YAML key | Value type |
| --- | --- | --- |
'''
        for row in m["config_fields"]:
            text += f"| `{row['group']}` | `{row['field']}` | `{row['type'].replace('|', '&#124;')}` |\n"
        if not m["config_fields"]:
            text += "| See upstream configuration reference | See source | See source |\n"
        config_paths = sorted({r["path"] for r in m["config_fields"]})
        text += "\n" + " · ".join(f"[Configuration structures and validation]({upstream(m, p)})" for p in config_paths) + "\n"
        text += "\n## API operation index\n\nThese operations are extracted from the module's OpenAPI contract. Read the source contract for request/response schemas, permission checks and exact route bases; internal mesh endpoints must not be treated as anonymous public APIs.\n\n"
        if m["api_operations"]:
            text += "| Method | Contract path | Operation |\n| --- | --- | --- |\n"
            for op in m["api_operations"]:
                text += f"| `{op['method']}` | `{op['path']}` | {op['summary'].replace('|', '&#124;')} |\n"
            text += "\n" + " · ".join(f"[OpenAPI: {p}]({upstream(m, p)})" for p in sorted({op["source"] for op in m["api_operations"]})) + "\n"
        else:
            text += "See the upstream module overview and repository API/SDK contracts below.\n"
    else:
        text += '''## Consume the platform

The platform is a framework/library, not a standalone service image. Consume it in a Go service using the documented release or replace the version with your chosen compatible v4 release:

```sh
GOWORK=off go get github.com/go-tangra/go-tangra/v4@v4.0.0
```

This example is the upstream README's version, not a declaration that it is the newest release. SDKs use their independently published `sdk/vX.Y.Z` tags and Go import paths ending `/sdk/v4`; add only the services whose APIs you consume.

## Shared libraries

- **Freya** supplies identity, transports, service policy, audit, observability, discovery and request limits.
- **`@go-tangra/ui`** supplies shared frontend components, forms, API client and theme. It is distributed through GitHub Packages; a token with `read:packages` is needed for installation.
- **audit-timescale** is an optional TimescaleDB audit sink. [Detailed consumption](sources/platform/contrib/audit-timescale/README.html).
- **policy-valkey** provides optional policy distribution and revocation integration. [Detailed consumption](sources/platform/contrib/policy-valkey/README.html).
- **Service SDKs** expose typed contracts and clients. Their nested modules are consumed by other services rather than deployed as additional daemons.

The [UI kit reference](sources/platform/ui/kit/README.html), [contrib overview](sources/platform/contrib/README.html), and each service README describe exact package contracts. The same library consumption applies whether the resulting service runs natively or in Docker.

## Architecture and defaults

[Security model](architecture/security.html) · [Framework configuration](architecture/configuration.html) · [Frontend architecture](architecture/frontend.html) · [Dependency justification](architecture/dependencies.html)
'''
    text += "\n## Detailed source references\n\n"
    for d in m["sources"]:
        text += f"- [{d['path']}]({source_link(m, d['path'])}) — captured at `{m['commit'][:12]}`.\n"
    if m["binary"]:
        text += "\n## Limits, diagnostics and recovery\n\n" + EXCEPTIONS[id_] + "\n\nUse the module's operations/deployment reference for retention, backup/restore, refusal behavior, interface examples and feature limitations. The installation guides cover common readiness, identity, registration and storage failures.\n"
    text += "\n" + adapt_markdown(m, (CONTENT / "sources" / id_ / "README.md").read_text())
    write(f"modules/{id_}.md", text)

def citations(m):
    text = f"\n## Sources and scope\n\n[Module README]({source_link(m, 'README.md')}) · [Module configuration and interfaces](modules/{m['id']}.html) · [Source Makefile]({upstream(m, 'Makefile')}) · [Source Dockerfile]({upstream(m, 'Dockerfile')})\n\n"
    for d in m["sources"]:
        if d["path"] in {"deploy/README.md", "docs/operations.md", "docs/validation.md"}:
            text += f"- [Detailed {d['path']}]({source_link(m, d['path'])}).\n"
    text += "\nCommands follow the recorded source contracts; host/path adaptations are explained here. Clean-environment deployment acceptance and compatible published image combinations have not yet been established for this documentation snapshot.\n"
    return text

def verification(m, native):
    id_ = m["id"]
    text = "\n## Verify installation\n\n"
    if native:
        text += f'''On the service host, if you retained the loopback admin default:

```sh
curl --fail http://127.0.0.1:{m['admin_port']}/healthz
curl --fail http://127.0.0.1:{m['admin_port']}/readyz
```

Expected: successful HTTP status from both checks and the documented readiness fields indicating available required dependencies. Change the address if your configuration differs. A non-loopback admin listener requires the authenticated transport configured by the framework; do not probe it as plain public HTTP.
'''
    else:
        text += f"Confirm the container/init jobs do not exit with errors. Check `/healthz` and `/readyz` on the configured **private admin listener** (default loopback port `{m['admin_port']}` inside the container). Use your private probe in that container's network namespace; the container loopback address is not the host's loopback. Do not publish admin ports just to make a browser check work.\n"
    text += f"\nThen check the workload's registration state, sign into the gateway with a user holding the module's permissions, and open {m['name']}. Expected: the module is registered and the authorized view loads. Perform a small module-specific read operation described in its [reference](modules/{id_}.html). For configured optional integrations, verify those separately; base readiness does not establish every external feature.\n"
    return text

def troubleshoot(m):
    return f'''\n## Troubleshooting

| Symptom | Check and corrective action |
| --- | --- |
| Bootstrap fails or database is unreachable | Check the dependency endpoint, migration credentials, pre-created app role, database ownership and required extensions; fix these before retrying bootstrap. |
| Invalid or missing identity | Confirm trust domain, cert/key/bundle or enrollment token paths and permissions. Persist enrollment state; a used token must be replaced, not replayed. |
| Module absent from the gateway | Check SPIFFE identity, granted route prefix, module readiness, gateway discovery and registry lease. Configure reciprocal Auth/LCM/module service policy. |
| Permission denied | Check user tenant, module permission/role and resource relationships; a service identity alone does not grant user permissions. |
| Sealed data cannot be opened after restore | Restore the matching encryption key along with the module database. Do not generate a replacement key for existing sealed data. |
| Port already in use or state unwritable | Adjust the configuration and discovery consistently; give only the service account write access to its own state directories. |
| Optional integration does not work | Review the module-specific configuration and peer policy; verify the external system from the service environment. |

{EXCEPTIONS[m['id']]}
'''

def native_guide(m):
    id_, binary = m["id"], m["binary"]
    checkout = f"go-tangra-{id_}"
    text = f'''# Install {m['name']} without Docker

Run `{binary}` as a Linux host process connected to native or managed dependencies. This guide uses source revision `{m['commit'][:12]}` (v4); it does not require Docker at any step.

## Prerequisites and dependencies

Complete [native prerequisites](how-to/native-prerequisites.html), including Go `{m['toolchain'].removeprefix('go')}`, Node 22 for the UI, a GitHub Packages token and a bootstrapped control plane. For the initial control plane installation, build the binaries first, then follow the prerequisites' bootstrap sequence before serving.

**Required**: {', '.join(m['required'])}.

**Optional or feature-dependent**: {', '.join(m['optional']) if m['optional'] else 'see the module operations reference'}.

Provision these dependencies without containers, using the module's detailed reference for role/schema/ACL/bucket setup. [Module reference](modules/{id_}.html).

{EXCEPTIONS[id_]}

## Obtain and build

From a directory where you keep source checkouts:

```sh
git clone {m['repository']}.git {checkout}
cd {checkout}
git checkout {m['commit']}
export GOWORK=off
go mod download
```

Export `NODE_AUTH_TOKEN` securely with GitHub Packages read access, then build the frontend and embedded service:

```sh
cd {m['ui_dir']}
npm ci
npm run build
'''
    if id_ == "auth":
        text += "npm run build:remote\n"
    text += f'''cd ..
go build -tags "{m['build_tags']}" -o bin/{binary} ./cmd/{binary}
```

Expected: the UI build succeeds and `bin/{binary}` is produced. Check `./bin/{binary} version`. A source-built binary without release ldflags may report a development version; do not interpret it as proof of a published release.

## Configure the native service

```sh
cp {m['config_path']} native.yaml
chmod 600 native.yaml
```

Edit `native.yaml` before bootstrap. Replace example credentials and container paths/hostnames; set database/application/migration roles, any event/object stores, identity and trust bundle, secret references, discovery and gateway targets, and writable state. The [configuration index](modules/{id_}.html) identifies module keys; [native prerequisites](how-to/native-prerequisites.html) covers common paths and identity setup. Do not expect the unedited development YAML to work on your host.

Use the matching service account for runtime and ensure it can read only its own secrets and write its state. Required dependency connections must be reachable from that account. Keep admin and mesh listeners private.
'''
    if id_ == "dns":
        text += "\nDisable the Docker restart feature in native YAML; use PowerDNS's host service manager for restart. Configure PowerDNS API keys through private file/environment references.\n"
    if id_ == "ipam":
        text += f'''\nFor ICMP discovery, after reviewing the deployment's permission needs:

```sh
sudo setcap cap_net_raw+ep bin/{binary}
```

Reapply the capability after replacing the binary. Skip it if that scanning feature is disabled.
'''
    if id_ == "asterisk":
        text += "\nPopulate the required ASTERISK environment references documented in the README. Use read-only PBX credentials; point optional registration storage at its separate module database and recordings at a read-only host path.\n"
    extra = " -operator-email you@example.org" if id_ == "auth" else ""
    if id_ == "portal":
        extra = ' -allow "spiffe://example.org/svc/auth=/api/v1,/authorize,/.well-known,/console;auth"'
    text += f'''\n## Bootstrap and start

After configuring dependencies, identity and peer grants:

```sh
./bin/{binary} bootstrap -config native.yaml{extra}
./bin/{binary} -config native.yaml
```

Expected: bootstrap exits successfully after its documented initialization/validation; serving starts without configuration/identity errors. Run the service in the foreground for the first verification. For a durable deployment, install the binary/configuration under your service manager with the same account, working directory, paths and environment.
'''
    if id_ == "auth":
        text += "\nReplace `you@example.org` with the actual first operator email. Accept the invitation through your configured notification delivery and complete operator setup.\n"
    if id_ == "portal":
        text += "\nReplace the example trust domain and add `-allow` entries for each real module's SPIFFE ID, prefixes and remote name. The example only grants Auth; it is not a complete installation allow-list. Configure edge TLS separately from workload identity.\n"
    if id_ == "lcm":
        text += "\nFor first mesh setup, use the additional `-out`, `-trust-domain` and `-services` bootstrap flags in [native prerequisites](how-to/native-prerequisites.html). The plain bootstrap above performs initialization/checks rather than distributing every workload identity.\n"
    if id_ == "asterisk":
        text += f"\nA supplied [systemd unit]({upstream(m, 'deploy/tangra-asterisk.service')}) documents the service account, environment file, read-only recordings and state directory. Adapt its paths before installing it; it is not enabled by the build command.\n"
    text += verification(m, True) + troubleshoot(m)
    text += f'''\n## Stop and remove

For the foreground run, press Ctrl+C and confirm the process exits. Under a service manager, stop and disable the configured module unit. Remove the installed binary/configuration only after checking that no other service uses those files.

Stopping or removing the binary does not delete database records, objects or identities. Back up the module database, required encryption/signing keys, blobs and enrollment state before deliberately removing them. Retiring the service also requires revoking its identity and removing its gateway/policy grants; preserve the shared control plane for other modules.
'''
    text += citations(m)
    write(f"guides/{id_}/native.md", text)

def docker_guide(m, platform):
    id_ = m["id"]
    bundle = json.loads((ROOT / "deploy/compose" / id_ / "bundle.json").read_text())
    if bundle.get("mode") == "existing-core":
        write(f"guides/{id_}/docker.md", existing_core_guide(m, bundle) + key_documentation((ROOT / "deploy/compose" / id_ / "compose.yaml").read_text()))
        return
    svc = bundle["service"]
    applications = ", ".join(bundle["applications"])
    text = f'''# Install {m['name']} with Docker Compose

**Core bootstrap only**: this bundle creates an initial core. If Auth/Portal/LCM are already running, manage upgrades or replacement through that existing core; do not start this bundle to add a regular module. Regular module guides enroll into your existing core.

Install `{svc}` using its standalone Compose bundle. It includes an isolated Auth/Portal/LCM control plane, required infrastructure and the enabled feature dependencies: **{applications}**. An existing Go-Tangra installation or module source checkout is not required.

## Prerequisites and dependencies

Use Docker Engine with Compose v2 or later and registry access. Check `docker version` and `docker compose version`, sufficient disk/memory and the host ports required by the included services. The bundle is for a local workstation: it uses development infrastructure credentials and self-signed browser TLS. Its service mesh verifies the generated CA during enrollment.

The defaults record local v4 service tags, including `{m['tag']}` for {m['name']}; confirm image availability and compatibility before starting. Each included application has its own version variable in `.env.example`.

**Module dependencies**: {', '.join(m['required'])}. The bundle provisions the local control plane and infrastructure for its enabled features. External business systems, provider accounts and hardware targets still need their own configuration.

## Download the standalone bundle

[Download the complete {m['name']} Compose bundle](downloads/{id_}.zip) · [View compose.yaml](downloads/{id_}/compose.yaml) · [View environment example](downloads/{id_}/.env.example)

Download the ZIP, then extract it:

```sh
unzip {id_}.zip
cd {id_}
cp .env.example .env
```

Alternatively, from a checkout of this documentation repository, use `cd deploy/compose/{id_}` and copy `.env.example` there. Keep the whole bundle together: the Compose file mounts its relative `configs/`, `policies/` and initialization files.

## Configure the installation

Edit `.env` to set `OPERATOR_EMAIL` to your first operator's address and choose published compatible versions for each application. The default gateway is `https://localhost:8443`; Mailpit is `http://localhost:8025`. The project name is `{bundle['project']}` and its network/volumes are isolated from other bundles.

If another bundle is running, change conflicting host port variables and the matching issuer/public/allowed-origin URLs in `configs/*.yaml`. Changing only a host port leaves the browser authentication URLs inconsistent. No admin ports or Docker daemon socket are published.

Review `configs/{svc}.yaml` and the policies before enabling external integrations. Bootstrap creates database roles/schema, mesh identities, enrollment tokens and gateway registration grants. Keys are generated once inside private named volumes and retained across restarts; no private key is included in the download.
'''
    if id_ == "asterisk":
        text += "\nSet `ASTERISK_CDR_DSN` in `.env` to a reachable PBX MySQL CDR database using SELECT-only credentials, for example `reader:YOUR_PASSWORD@tcp(PBX_HOST:3306)/asteriskcdrdb?parseTime=true`. Compose refuses to configure without this value. `host.docker.internal` reaches the Docker host where supported by the supplied host-gateway mapping. The bundled `registration-db` is module-owned and separate; bootstrap never migrates the PBX source. AMI, recording playback and monitoring start disabled; configure them explicitly if needed.\n"
    elif id_ == "sms-gw":
        text += "\nThe public Hermes HTTP listener is bound to host loopback port 9901 by default (`SMS_PORT` changes the host port). The bundle creates the module database, KEK, JWT secret, enrollment and ACME state volumes. Create a provider and API client through the management UI before sending SMS; configure a real carrier or your own mock provider. Enable and configure public HTTPS before using that listener beyond a private development environment.\n"
    elif id_ == "dns":
        text += "\nPowerDNS Authoritative/Recursor and a private Prometheus are included. Docker-socket restart integration is disabled; after changing managed DNS server configuration, apply it with `docker compose restart pdns-auth pdns-recursor`. DNS uses loopback host ports 5300/5301 from the manifest.\n"
    elif id_ == "ipam":
        text += "\nThe bundle includes Inventory, Warden and Scheduler, enables scheduled task integration and grants `NET_RAW` for ICMP scanning. Network targets, BMC credentials and endpoint agents are external to the bundle.\n"
    elif id_ in {"signing", "hr", "asset"}:
        text += "\nThe bundle includes Scheduler and enables supported task registrations. Configure module-specific templates, providers and user relationships before checking scheduled business workflows; having the scheduler running does not create every tenant task.\n"
    text += f'''\n## Validate, bootstrap and start

From the bundle directory:

```sh
docker compose config --quiet
docker compose pull
docker compose up -d
docker compose ps -a
docker compose logs --tail=100 auth-bootstrap {svc}
```

Expected: configuration validation succeeds, images pull, initialization jobs exit successfully and services stay running. `depends_on` gates store readiness and completed bootstrap/token jobs. Read failed job logs before retrying. The default project contains only this module's application/dependency selection, rather than the entire platform stack.

Accept the invitation from `auth-bootstrap` logs or development Mailpit, set the password and TOTP, and sign in to the gateway. Its browser certificate is self-signed for localhost; trust it only on your own development workstation.

## Verify installation

The included check service uses the module's own network namespace to probe private admin port **{bundle['admin_port']}**. Run:

```sh
docker compose --profile checks run --rm check
docker compose logs --tail=100 {svc}
```

Expected: `Health and readiness passed`, followed by exit status 0. The check retries startup readiness for up to two minutes. No admin port needs to be published. Then sign in with a user holding {m['name']}'s permissions, confirm the module is registered in the gateway, and perform a small read operation from its [module reference](modules/{id_}.html). Test configured external integrations separately.

## Troubleshooting

| Symptom | Check and remedy |
| --- | --- |
| Compose rejects an environment value | Populate the required `.env` fields; Asterisk needs a read-only CDR DSN. Run `docker compose config --quiet` again. |
| Image pull fails | Select a published compatible version for that service in `.env`; local source tags alone do not prove registry availability. |
| A bootstrap job fails | Use `docker compose logs JOB_NAME`; check store health, role/schema setup, paths and the generated key volumes before retrying `docker compose up -d`. |
| Module is not registered | Check `{svc}` logs, readiness, its persisted enrollment state, and the bundled gateway allow-list/policy. A spent token cannot replace deleted identity state. |
| Browser sign-in URL is wrong | Match host port changes with public/issuer/origin values in the configuration files, then recreate affected services. |
| Sealed records fail after restore | Restore matching key volumes along with database/object data. Never overwrite an existing key with a new random key. |
| Vault is sealed after restart | Where included, check `docker compose logs vault`; the private recovery volume must match `vault-data`. Recreate the dependent AppRole job with `docker compose up -d --force-recreate vault-init warden`. |
| A port is already occupied | Stop the other bundle, or change the conflicting ports and matching configuration origins consistently. |

## Stop and remove

Stop only this service while preserving data:

```sh
docker compose stop {svc}
```

Stop all services in the standalone installation, then bring them back:

```sh
docker compose stop
docker compose up -d
```

Remove containers/network while preserving persistent volumes:

```sh
docker compose down
```

**Destructive reset**: `docker compose down -v` also deletes databases, objects, mesh CA/identity, keys, tokens and any Vault/registration state in the bundle. Back up the complete set before deliberately resetting; this requires fresh initialization. The external PBX/carrier/targets are never cleanup targets.

## Sources and scope

[Module README]({source_link(m, 'README.md')}) · [Module configuration and interfaces](modules/{id_}.html) · [Platform stack reference](sources/platform/deploy/stack/README.html)

This bundle adapts the recorded public platform/service deployment contracts into a standalone directory. Its added Compose integration is maintained in this repository; the upstream base stack does not contain every later module. Configuration and integrity validation do not establish live deployment acceptance or a tested release matrix.
'''
    text += key_documentation((ROOT / "deploy/compose" / id_ / "compose.yaml").read_text())
    write(f"guides/{id_}/docker.md", text)

def main():
    modules = json.loads((CONTENT / "modules.json").read_text())["modules"]
    platform = next(m for m in modules if m["id"] == "platform")
    for m in modules:
        reference(m)
        if m["binary"]:
            native_guide(m)
            docker_guide(m, platform)
    print(f"Wrote {len(modules)} module references and {2 * sum(bool(m['binary']) for m in modules)} installation guides.")

if __name__ == "__main__":
    main()
