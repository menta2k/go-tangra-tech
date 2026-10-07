#!/usr/bin/env python3
"""Create portable per-service Compose bundles from recorded public sources.

Explicit maintenance command. Reads tracked files at inventory commits, never
working deployment secrets or local Compose overrides. Ordinary site builds use
the checked-in bundles and do not need sibling repositories.
"""
import argparse
import copy
import hashlib
import json
import re
import subprocess
from pathlib import Path

import yaml
from existing_core import adapt
from key_documentation import key_documentation

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deploy/compose"
TENANT = "00000000-0000-0000-0000-000000000001"
EXTRA_MODULES = {
    "asset": ["inventory", "paperless", "scheduler"],
    "deployer": ["inventory"],
    "ipam": ["inventory", "warden", "scheduler"],
    "dns": ["ipam", "warden", "inventory"],
    "signing": ["notification", "warden", "scheduler"],
    "hr": ["signing", "notification", "scheduler"],
    "ticket": ["warden"],
}

class Sources:
    def __init__(self, root, modules):
        self.root = root.resolve()
        self.modules = {m["id"]: m for m in modules}
        self.used = {}

    def read(self, module, path):
        if path.startswith("/") or ".." in Path(path).parts:
            raise ValueError(f"Not a repository-relative public path: {path}")
        m = self.modules[module]
        result = subprocess.run(["git", "-C", str(self.root / m["checkout"]), "show",
                                 f"{m['commit']}:{path}"], capture_output=True)
        if result.returncode:
            raise ValueError(f"Missing tracked public source {module}:{path} at {m['commit']}")
        self.used[f"{module}:{path}"] = {"module": module, "path": path, "commit": m["commit"],
                                        "sha256": hashlib.sha256(result.stdout).hexdigest()}
        return result.stdout.decode()

def dump(value):
    return yaml.safe_dump(value, sort_keys=False, width=1000)

def module_id(service):
    return "portal" if service == "gateway" else service

def dependencies(service):
    value = service.get("depends_on", {})
    return list(value) if isinstance(value, (dict, list)) else []

def closure(services, roots):
    selected = set()
    def visit(name):
        if name in selected:
            return
        if name not in services:
            raise ValueError(f"Missing dependency {name}")
        selected.add(name)
        for dep in dependencies(services[name]):
            visit(dep)
    for root in roots:
        visit(root)
    return selected

def token_job(base, name):
    job = copy.deepcopy(base)
    job["command"] = ["mint-enrollment-token", "-config", "deploy/container.yaml", "-spiffe",
                      f"spiffe://example.org/svc/{name}", "-ttl", "30m", "-out", f"/tokens/{name}.token"]
    return job

def new_service(name, config_target, extra_deps=None):
    return {
        "image": f"ghcr.io/go-tangra/go-tangra-{name}:4.0.0",
        "user": "0:0", "command": ["-config", config_target], "restart": "unless-stopped",
        "volumes": [f"./configs/{name}.yaml:{config_target}:ro", "tokens:/tokens:ro", "certs:/certs:ro", f"{name}-state:/state"],
        "depends_on": {
            "timescaledb": {"condition": "service_healthy"},
            "gateway": {"condition": "service_healthy"},
            "lcm": {"condition": "service_healthy"},
            f"{name}-token": {"condition": "service_completed_successfully"},
            **(extra_deps or {}),
        },
    }

KEYS_SCRIPT = '''#!/bin/sh
set -eu
umask 077
for directory in /keys/*; do
  [ -d "$directory" ] || continue
  if [ ! -s "$directory/kek" ]; then
    head -c 32 /dev/urandom | base64 > "$directory/kek.tmp"
    mv "$directory/kek.tmp" "$directory/kek"
  fi
  chmod 600 "$directory/kek"
done
echo "Private keys ready (existing keys preserved)."
'''

VAULT_CONFIG = '''ui = false
disable_mlock = true
api_addr = "http://vault:8200"
storage "file" { path = "/vault/file" }
listener "tcp" {
  address = "0.0.0.0:8200"
  tls_disable = 1
}
'''

VAULT_START = r'''#!/bin/sh
set -eu
# Persistent single-node development Vault. Recovery material stays private.
vault server -config=/etc/vault/config.hcl &
server_pid=$!
trap 'kill "$server_pid"; wait "$server_pid"' TERM INT
attempt=0
while ! vault status -format=json >/tmp/vault-status.json 2>/dev/null; do
  if [ -s /tmp/vault-status.json ]; then break; fi
  attempt=$((attempt + 1))
  [ "$attempt" -lt 60 ] || exit 1
  sleep 1
done
if [ ! -s /vault-bootstrap/init.json ]; then
  umask 077
  vault operator init -key-shares=1 -key-threshold=1 -format=json > /vault-bootstrap/init.json.tmp
  mv /vault-bootstrap/init.json.tmp /vault-bootstrap/init.json
fi
# Parse the two JSON string fields without installing an extra CLI at startup.
unseal_key=$(sed -n '/"unseal_keys_b64"/,$ { /"[A-Za-z0-9+\/=]*"/ { s/^[[:space:]]*"\([A-Za-z0-9+\/=]*\)".*/\1/p; } }' /vault-bootstrap/init.json | head -n 1)
[ -n "$unseal_key" ] || { echo "Cannot read Vault unseal key" >&2; exit 1; }
vault operator unseal "$unseal_key" >/dev/null
wait "$server_pid"
'''

VAULT_INIT = r'''#!/bin/sh
set -eu
umask 077
export VAULT_TOKEN=$(sed -n 's/^[[:space:]]*"root_token":[[:space:]]*"\([^"]*\)".*/\1/p' /vault-bootstrap/init.json)
[ -n "$VAULT_TOKEN" ] || { echo "Cannot read Vault bootstrap token" >&2; exit 1; }
sh /vault-approle.sh
chmod 600 /vault-creds/role_id /vault-creds/secret_id
'''

def add_missing_services(source, services):
    services["scheduler-token"] = token_job(services["notification-token"], "scheduler")
    services["scheduler"] = new_service("scheduler", "deploy/container.yaml", {"valkey": {"condition": "service_healthy"}})
    services["scheduler"]["healthcheck"] = {"test": ["CMD", "wget", "-qO-", "http://127.0.0.1:9800/readyz"], "interval": "5s", "timeout": "3s", "retries": 40}
    services["sms-gw-token"] = token_job(services["notification-token"], "sms-gw")
    services["sms-gw"] = new_service("sms-gw", "deploy/container.yaml")
    services["sms-gw"].update({"read_only": True, "tmpfs": ["/tmp:rw,noexec,nosuid,size=16m"],
                                "ports": ["127.0.0.1:${SMS_PORT:-9901}:9901"]})
    services["sms-gw"]["volumes"] += ["sms-gw-keys:/secrets:ro", "sms-gw-acme:/acme"]
    services["asterisk-token"] = token_job(services["notification-token"], "asterisk")
    services["asterisk"] = new_service("asterisk", "/etc/asterisk-module/config.yaml",
                                        {"registration-db": {"condition": "service_healthy"}})
    services["asterisk"].update({"read_only": True, "tmpfs": ["/tmp:rw,noexec,nosuid,size=16m"],
                                  "environment": {"ASTERISK_CDR_DSN": "${ASTERISK_CDR_DSN:?Set a read-only PBX CDR DSN in .env}"},
                                  "extra_hosts": ["host.docker.internal:host-gateway"]})
    services["registration-db"] = {
        "image": "mysql:8.4", "environment": {"MYSQL_ROOT_PASSWORD": "registration-dev-only"},
        "volumes": ["registration-data:/var/lib/mysql", "./registration.sql:/docker-entrypoint-initdb.d/10-registration.sql:ro"],
        "healthcheck": {"test": ["CMD", "mysqladmin", "ping", "-h", "127.0.0.1", "-pregistration-dev-only"], "interval": "3s", "timeout": "3s", "retries": 60},
    }

def get_config(source, svc):
    if svc == "scheduler":
        return yaml.safe_load(source.read("scheduler", "deploy/container.yaml"))
    if svc == "sms-gw":
        config = yaml.safe_load(source.read("sms-gw", "deploy/container.yaml"))
        config["server"] = {"grpc_addr": "0.0.0.0:9983", "http_addr": "0.0.0.0:9984"}
        config["public"]["http_addr"] = "0.0.0.0:9901"
        config["public"]["https_addr"] = ""
        config["db"]["dsn"] = "postgres://smsgw_app:dev@timescaledb:5432/sms_gw?sslmode=disable"
        config["db"]["migrate_dsn"] = "postgres://postgres:dev@timescaledb:5432/sms_gw?sslmode=disable"
        config["kek"]["path"] = "/secrets/kek"
        config["public_auth"]["jwt_secret"]["file"] = "/secrets/jwt.key"
        config["identity"] = {"provider": "provided"}
        config["enroll"] = {"enabled": True, "tenant_id": TENANT, "token_file": "/tokens/sms-gw.token", "state_file": "/state/svid.json", "lcm_grpc": "lcm:9945"}
        config["discovery"] = {"static": {"gateway": ["gateway:9643"], "auth": ["auth:9543"], "lcm": ["lcm:9945"]}}
        return config
    if svc == "asterisk":
        config = yaml.safe_load(source.read("asterisk", "configs/dev.yaml"))
        config["trust_domain"] = "example.org"
        config["env"] = "development"
        config["server"] = {"http_addr": "0.0.0.0:9982", "grpc_addr": "0.0.0.0:9981"}
        config["mesh_enroll"] = {"enabled": True, "tenant_id": TENANT, "token_file": "/tokens/asterisk.token", "state_file": "/state/svid.json", "lcm_grpc": "lcm:9945"}
        config["binding"].update({"tenant_id": TENANT, "pbx_id": "00000000-0000-0000-0000-000000000002",
                                  "cdr_dsn": "${ASTERISK_CDR_DSN}", "config_dsn": "",
                                  "registration_dsn": "asterisk_app:registration-dev-only@tcp(registration-db:3306)/asterisk_registration?parseTime=true",
                                  "recording_root": "", "monitoring_url": ""})
        config["gateway"]["issuer"] = "https://localhost:8443"
        config["discovery"] = {"static": {"auth": ["auth:9543"], "gateway": ["gateway:9643"], "lcm": ["lcm:9945"]}}
        return config
    return yaml.safe_load(source.read("platform", f"deploy/stack/configs/{svc}.yaml"))

def prepare_configs(source, selected, modules):
    configs = {svc: get_config(source, svc) for svc in selected if module_id(svc) in modules}
    for svc, config in configs.items():
        config["authz"]["path"] = f"/policies/{svc}.yaml"
        if "kek" in config and svc != "sms-gw":
            config["kek"]["path"] = "/keys/kek"
        for name in ("enroll", "mesh_enroll"):
            if config.get(name, {}).get("enabled"):
                config[name].update({"enroll_url": "https://lcm:9947/api/lcm/v1/enroll", "insecure": False,
                                     "ca_file": "/certs/ca.pem", "server_spiffe_id": "spiffe://example.org/svc/lcm"})
        if "scheduler" in selected and any(f["field"] == "task_scheduler" for f in modules[module_id(svc)]["config_fields"]):
            config["task_scheduler"] = {"enabled": True, "service": "scheduler"}
            config.setdefault("discovery", {}).setdefault("static", {})["scheduler"] = ["scheduler:9905"]
        if svc == "gateway" and "ipam" not in selected:
            config["console"]["enabled"] = False
        if svc == "dns":
            config["docker"]["enabled"] = False
            config["metrics"]["prometheus_url"] = "http://prometheus:9090"
        # Remove nonexistent discovery peers. Optional integrations can be added deliberately.
        discovery = config.get("discovery", {}).get("static", {})
        config.get("discovery", {}).update({"static": {k: v for k, v in discovery.items() if k in selected}})
    return configs

def database_sql(configs):
    sql = ["-- Local workstation credentials. One owned DB and non-bypass app role per service.", "CREATE DATABASE openfga;"]
    for svc, config in sorted(configs.items()):
        if "db" not in config:
            continue
        database = "sms_gw" if svc == "sms-gw" else svc
        role = "smsgw_app" if svc == "sms-gw" else f"{svc}_app"
        sql += [f"CREATE DATABASE {database};", f"\\c {database}", "CREATE EXTENSION IF NOT EXISTS timescaledb;",
                "CREATE EXTENSION IF NOT EXISTS citext;", "CREATE EXTENSION IF NOT EXISTS btree_gist;",
                f"CREATE ROLE {role} LOGIN PASSWORD 'dev' NOBYPASSRLS;", f"GRANT CONNECT ON DATABASE {database} TO {role};", "\\c postgres"]
    return "\n".join(sql) + "\n"

def make_bundle(source, base, target, modules):
    services = copy.deepcopy(base["services"])
    add_missing_services(source, services)
    roots = {"auth", "lcm", "gateway", "renewer", "mailpit", "gateway-bootstrap", "auth-bootstrap", target}
    queue = [target]
    while queue:
        svc = queue.pop()
        for extra in EXTRA_MODULES.get(svc, []):
            if extra not in roots:
                roots.add(extra)
                queue.append(extra)
    if target == "dns":
        roots.add("prometheus")
    selected = closure(services, roots)
    # ACME demo and optional isolated LDAP are not needed for mesh bootstrap.
    services["lcm"].get("depends_on", {}).pop("pebble-certs", None)
    selected.discard("pebble-certs")
    configs = prepare_configs(source, selected, modules)
    bundle = {"name": f"tangra-{module_id(target)}", "services": {k: services[k] for k in services if k in selected}}
    files = {}
    key_modules = [svc for svc, cfg in configs.items() if "kek" in cfg and svc != "sms-gw"]
    key_volumes = {svc: f"{svc}-keys" for svc in key_modules}
    keys_init_volumes = [f"{vol}:/keys/{svc}" for svc, vol in key_volumes.items()]
    if "sms-gw" in selected:
        keys_init_volumes += ["sms-gw-keys:/sms-secrets"]
    script = KEYS_SCRIPT
    if "sms-gw" in selected:
        script += '''for name in kek jwt.key; do
  if [ ! -s "/sms-secrets/$name" ]; then
    head -c 32 /dev/urandom | base64 > "/sms-secrets/$name.tmp"
    mv "/sms-secrets/$name.tmp" "/sms-secrets/$name"
  fi
  chmod 600 "/sms-secrets/$name"
done
'''
    files["init-keys.sh"] = script
    bundle["services"]["keys-init"] = {"image": "alpine:3.20", "user": "0:0", "entrypoint": ["sh", "/init-keys.sh"],
                                             "volumes": ["./init-keys.sh:/init-keys.sh:ro", *keys_init_volumes], "restart": "no"}
    for svc, cfg in configs.items():
        files[f"configs/{svc}.yaml"] = dump(cfg)
        policy = source.read(module_id(svc), "deploy/policy.yaml").replace("spiffe://tangra.local/", "spiffe://example.org/")
        files[f"policies/{svc}.yaml"] = policy
    for name, service in list(bundle["services"].items()):
        service.pop("container_name", None)
        service.pop("profiles", None)
        # Isolation per project; no external mesh or fixed-subnet network required.
        service.pop("networks", None)
        module = None
        for mount in service.get("volumes", []):
            match = re.match(r"\./configs/([^/]+)\.yaml:", mount)
            if match:
                module = match[1]
                break
        if module:
            service["volumes"] = [v for v in service.get("volumes", []) if not v.startswith("./keys/") and not v.startswith("pebble-certs:") and not v.startswith("/var/run/docker.sock:")]
            service["volumes"].append(f"./policies/{module}.yaml:/policies/{module}.yaml:ro")
            if module in key_volumes:
                service["volumes"].append(f"{key_volumes[module]}:/keys:ro")
            if not any(v.startswith("certs:") for v in service["volumes"]):
                service["volumes"].append("certs:/certs:ro")
            service.setdefault("depends_on", {})["keys-init"] = {"condition": "service_completed_successfully"}
            version_var = module_id(module).upper().replace("-", "_") + "_VERSION"
            service["image"] = modules[module_id(module)]["image"] + ":${" + version_var + ":-" + modules[module_id(module)]["tag"].removeprefix("v") + "}"
        if name == "lcm":
            service.pop("environment", None)
        if name == "timescaledb":
            service["volumes"].append("database-data:/var/lib/postgresql/data")
        if name == "valkey":
            service["command"] += ["--appendonly", "yes"]
            service["volumes"] = ["valkey-data:/data"]
            for svc in configs:
                if svc == "scheduler":
                    service["command"] += ["--user", "scheduler", "on", ">dev", "~*", "&*", "+@all"]
        if name == "mailpit":
            service["ports"] = ["127.0.0.1:${MAILPIT_PORT:-8025}:8025"]
        if name == "auth-bootstrap":
            service["command"][-1] = "${OPERATOR_EMAIL:?Set OPERATOR_EMAIL in .env}"
        if name == "gateway":
            service["ports"] = ["127.0.0.1:${GATEWAY_PORT:-8443}:8443"]
            if "ipam" in selected:
                service["ports"].append("127.0.0.1:${CONSOLE_PORT:-8444}:8444")
        if name == "inventory":
            service["ports"] = ["127.0.0.1:${INVENTORY_PORT:-9977}:9977"]
        if name == "ticket":
            service["ports"] = ["127.0.0.1:${TICKET_MAIL_PORT:-9957}:9957"]
        if name == "ipam":
            service["cap_add"] = ["NET_RAW"]
        if name == "gateway-bootstrap":
            command = ["bootstrap", "-config", "deploy/container.yaml"]
            for svc in sorted(configs):
                if svc == "gateway":
                    continue
                prefixes = "/api/v1,/authorize,/.well-known,/console" if svc == "auth" else "/api/warden,/warden/share" if svc == "warden" else f"/api/{svc}"
                command += ["-allow", f"spiffe://example.org/svc/{svc}={prefixes};{svc}"]
            service["command"] = command
        # Inherited image bootstrap jobs have a finite lifecycle.
        if name not in configs and name not in {"renewer", "timescaledb", "valkey", "openfga", "mailpit", "rustfs", "tika", "gotenberg", "vault", "pdns-auth", "pdns-recursor", "prometheus", "registration-db"}:
            service["restart"] = "no"
        elif name != "vault-init":
            service.setdefault("restart", "unless-stopped")

    # Persistent Vault replaces the upstream ephemeral in-memory dev instance.
    if "vault" in selected:
        files["vault/config.hcl"] = VAULT_CONFIG
        files["vault/start.sh"] = VAULT_START
        files["vault/init.sh"] = VAULT_INIT
        files["vault/approle.sh"] = source.read("platform", "deploy/stack/vault-init.sh")
        bundle["services"]["vault"] = {"image": "hashicorp/vault:1.18", "user": "0:0", "entrypoint": ["sh", "/vault-start.sh"],
            "environment": {"VAULT_ADDR": "http://127.0.0.1:8200"},
            "volumes": ["vault-data:/vault/file", "vault-bootstrap:/vault-bootstrap", "./vault/config.hcl:/etc/vault/config.hcl:ro", "./vault/start.sh:/vault-start.sh:ro"],
            "restart": "unless-stopped", "healthcheck": {"test": ["CMD", "vault", "status"], "interval": "3s", "timeout": "3s", "retries": 60}}
        bundle["services"]["vault-init"] = {"image": "hashicorp/vault:1.18", "user": "0:0", "entrypoint": ["sh", "/vault-init.sh"],
            "environment": {"VAULT_ADDR": "http://vault:8200", "OUT": "/vault-creds"},
            "volumes": ["vault-bootstrap:/vault-bootstrap:ro", "vault-creds:/vault-creds", "./vault/init.sh:/vault-init.sh:ro", "./vault/approle.sh:/vault-approle.sh:ro"],
            "restart": "no", "depends_on": {"vault": {"condition": "service_healthy"}}}

    # Explicit migration/initialization for the three separately added services.
    if target in {"scheduler", "sms-gw", "asterisk"}:
        runtime = bundle["services"][target]
        bootstrap = copy.deepcopy(runtime)
        bootstrap.pop("ports", None)
        bootstrap.pop("healthcheck", None)
        bootstrap["command"] = ["bootstrap", "-config", runtime["command"][1]]
        bootstrap["restart"] = "no"
        bundle["services"][f"{target}-bootstrap"] = bootstrap
        runtime["depends_on"][f"{target}-bootstrap"] = {"condition": "service_completed_successfully"}
    if "asterisk" in selected:
        files["registration.sql"] = "CREATE DATABASE asterisk_registration;\nCREATE USER 'asterisk_app'@'%' IDENTIFIED BY 'registration-dev-only';\nGRANT ALL ON asterisk_registration.* TO 'asterisk_app'@'%';\n"
    if "prometheus" in selected:
        files["prometheus/prometheus.yml"] = dump({"global": {"scrape_interval": "15s"}, "scrape_configs": [
            {"job_name": "pdns-auth", "static_configs": [{"targets": ["pdns-auth:8081"]}]},
            {"job_name": "pdns-recursor", "static_configs": [{"targets": ["pdns-recursor:8082"]}]},
        ]})
    files["init-db.sql"] = database_sql(configs)

    # Copy only explicitly mounted tracked support files; private key files are never read.
    for service in bundle["services"].values():
        for mount in service.get("volumes", []):
            source_path = mount.split(":", 1)[0]
            if source_path.startswith("./"):
                path = source_path[2:]
                if path not in files:
                    files[path] = source.read("platform", "deploy/stack/" + path)

    port = int(configs[target]["admin"]["addr"].rsplit(":", 1)[1])
    bundle["services"]["check"] = {"image": "alpine:3.20", "profiles": ["checks"], "network_mode": f"service:{target}",
        "entrypoint": ["sh", "-ec"], "command": [f'for i in $(seq 1 60); do if wget -qO- http://127.0.0.1:{port}/healthz && wget -qO- http://127.0.0.1:{port}/readyz; then echo; echo "Health and readiness passed"; exit 0; fi; sleep 2; done; exit 1'],
        "depends_on": {target: {"condition": "service_started"}}, "restart": "no"}
    # Dollar signs in shell snippets must survive Compose interpolation.
    bundle["services"]["check"]["command"][0] = bundle["services"]["check"]["command"][0].replace("$(seq", "$$(seq")
    volumes = {}
    for service in bundle["services"].values():
        for mount in service.get("volumes", []):
            name = mount.split(":", 1)[0]
            if not name.startswith((".", "/", "$")):
                volumes[name] = {}
    bundle["volumes"] = volumes
    files["compose.yaml"] = "# Standalone workstation installation with its own control plane.\n# Generated from recorded public sources; review image availability before use.\n" + dump(bundle)
    env = ["# Workstation example. Keep a private .env; do not commit real credentials.", "OPERATOR_EMAIL=you@example.org", "GATEWAY_PORT=8443", "MAILPIT_PORT=8025", "# Changing host ports also requires updating origins in configs/*.yaml."]
    for svc in sorted(configs):
        m = modules[module_id(svc)]
        env.append(f"{m['id'].upper().replace('-', '_')}_VERSION={m['tag'].removeprefix('v')}")
    if target == "asterisk":
        env += ["# Required: SELECT-only credentials for your existing PBX CDR database.", "ASTERISK_CDR_DSN="]
    files[".env.example"] = "\n".join(env) + "\n"
    module = modules[module_id(target)]
    files["README.md"] = f'''# Standalone {module['name']} Compose installation

Includes an isolated Auth/Portal/LCM control plane and the dependencies of the enabled module features. No existing Go-Tangra stack or sibling source checkout is required. The framework and SDKs are libraries rather than standalone daemons.

This is a local workstation configuration (development database/Valkey/object-store credentials, self-signed browser TLS and private internal plaintext infrastructure). Mesh enrollment verifies the generated CA. Encryption keys are generated once in private named volumes; no private keys are shipped in this bundle.

```sh
cp .env.example .env
# Edit .env: operator email, available image versions, and any required integration values.
docker compose config --quiet
docker compose pull
docker compose up -d
docker compose logs auth-bootstrap
docker compose --profile checks run --rm check
```

Accept the operator invitation from auth-bootstrap logs or http://localhost:8025 and sign in at https://localhost:8443. The named project is `tangra-{module['id']}`. Use only the versions available in your registry; recorded local tags are not a verified compatible release matrix.

Stop the deployment with `docker compose stop`, start it again with `docker compose up -d`, and remove its containers with `docker compose down`. Named volumes preserve databases, objects, keys, identity and bootstrap state. **`docker compose down -v` deletes that state** and requires fresh initialization. When Vault is included, its single-node persistent file backend and private recovery volume survive restart; auto-unseal with co-located recovery material is for workstation use.

No admin ports or Docker daemon socket are published. The `check` service probes the module's own network namespace on private admin port {port}. For multiple simultaneous bundles, change conflicting host ports and matching origins in configs/*.yaml. DNS configuration saves require `docker compose restart pdns-auth pdns-recursor` to apply managed server files; Docker-socket restart control is disabled.

For Asterisk, populate `ASTERISK_CDR_DSN` with a reachable SELECT-only PBX source. Its bundled registration database is separate; PBX data is never initialized or migrated. For SMS, create a provider/client through the management UI before sending; no real carrier is included. Configure optional external targets (AMI, SMTP delivery, qualified signing, real ACME, endpoint agents) separately.

Main service: `{target}`. Included application services: {', '.join(sorted(configs))}.
Source review and Compose validation do not establish clean-environment deployment acceptance; see the website Docker guide for module-specific checks and source links.
'''
    return files, {"module": module["id"], "service": target, "project": bundle["name"],
                   "admin_port": port, "applications": sorted(configs), "services": sorted(bundle["services"]),
                   "files": {path: hashlib.sha256(data.encode()).hexdigest() for path, data in sorted(files.items())}}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="Sibling Go-Tangra source checkouts")
    args = parser.parse_args()
    modules = json.loads((ROOT / "content/modules.json").read_text())["modules"]
    source = Sources(args.root, modules)
    by_id = {m["id"]: m for m in modules}
    base = yaml.safe_load(source.read("platform", "deploy/stack/compose.yaml"))
    source.read("platform", "transport/runtime.go")
    source.read("auth", "cmd/authsvc/mint.go")
    source.read("portal", "cmd/gatewaysvc/bootstrap.go")
    for m in modules:
        if not m["binary"]:
            continue
        target = "gateway" if m["id"] == "portal" else m["id"]
        files, manifest = make_bundle(source, base, target, by_id)
        files, manifest = adapt(source, files, manifest, by_id, get_config, database_sql)
        files["README.md"] += key_documentation(files["compose.yaml"])
        manifest["files"]["README.md"] = hashlib.sha256(files["README.md"].encode()).hexdigest()
        directory = OUT / m["id"]
        directory.mkdir(parents=True, exist_ok=True)
        old_manifest = directory / "bundle.json"
        if old_manifest.is_file():
            for old_path in json.loads(old_manifest.read_text())["files"]:
                if old_path not in files:
                    (directory / old_path).unlink(missing_ok=True)
        for path, text in files.items():
            dest = directory / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(text)
        (directory / "bundle.json").write_text(json.dumps(manifest, indent=2) + "\n")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "sources.json").write_text(json.dumps(list(source.used.values()), indent=2) + "\n")
    print(f"Generated 14 existing-core module bundles and 3 initial-core bootstrap bundles in {OUT}")

if __name__ == "__main__":
    main()
