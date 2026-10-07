#!/usr/bin/env python3
"""Validate standalone bundle integrity and optionally run Compose's parser."""
import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

def check_bundles(root):
    errors = []
    inventory = json.loads((root / "content/modules.json").read_text())["modules"]
    names = set()
    for module in inventory:
        if not module["binary"]:
            continue
        directory = root / "deploy/compose" / module["id"]
        manifest_path = directory / "bundle.json"
        if not manifest_path.is_file():
            errors.append(f"{module['id']}: missing standalone bundle")
            continue
        manifest = json.loads(manifest_path.read_text())
        compose = yaml.safe_load((directory / "compose.yaml").read_text())
        services = compose["services"]
        target = manifest["service"]
        if target not in services:
            errors.append(f"{module['id']}: missing target")
        if manifest.get("mode") == "existing-core":
            if {"auth", "lcm", "gateway"}.intersection(services):
                errors.append(f"{module['id']}: module bundle must not start a new core")
            if manifest["applications"] != [target]:
                errors.append(f"{module['id']}: unexpected peer application")
            if "mesh" in compose.get("networks", {}):
                errors.append(f"{module['id']}: default remote deployment depends on a local mesh network")
            if "FREYA_ADVERTISE_HOST" not in services[target].get("environment", {}):
                errors.append(f"{module['id']}: missing reachable advertised host")
            if any(name.endswith("-token") for name in services):
                errors.append(f"{module['id']}: token must come from existing Auth")
        elif not {"auth", "lcm", "gateway"}.issubset(services):
            errors.append(f"{module['id']}: incomplete core bootstrap bundle")
        if compose["name"] in names:
            errors.append(f"{module['id']}: duplicate project name")
        names.add(compose["name"])
        for name, digest in manifest["files"].items():
            path = Path(name)
            if path.is_absolute() or ".." in path.parts or name == ".env" or path.suffix in {".key", ".pem", ".kek"}:
                errors.append(f"{module['id']}: unsafe downloadable file {name}")
                continue
            file = directory / path
            if not file.is_file() or file.is_symlink() or hashlib.sha256(file.read_bytes()).hexdigest() != digest:
                errors.append(f"{module['id']}: bundle hash mismatch {name}")
            if file.is_file() and any(byte < 32 and byte not in {9, 10, 13} for byte in file.read_bytes()):
                errors.append(f"{module['id']}: unexpected control character in {name}")
        graph = {}
        for name, service in services.items():
            deps = service.get("depends_on", {})
            graph[name] = list(deps)
            namespace = service.get("network_mode", "")
            if namespace.startswith("service:"):
                graph[name].append(namespace.split(":", 1)[1])
            for dep in graph[name]:
                if dep not in services:
                    errors.append(f"{module['id']}/{name}: missing dependency {dep}")
                elif isinstance(deps, dict) and deps.get(dep, {}).get("condition") == "service_healthy" and not services[dep].get("healthcheck"):
                    errors.append(f"{module['id']}/{name}: dependency {dep} lacks required healthcheck")
            if service.get("container_name"):
                errors.append(f"{module['id']}/{name}: fixed container name prevents isolation")
            for mount in service.get("volumes", []):
                source = mount.split(":", 1)[0]
                if source.startswith("./") and source[2:] not in manifest.get("generated_files", []) and not (directory / source[2:]).is_file():
                    errors.append(f"{module['id']}/{name}: missing relative mount {source}")
                if not source.startswith((".", "/", "$")) and source not in compose.get("volumes", {}):
                    errors.append(f"{module['id']}/{name}: undeclared volume {source}")
                if "docker.sock" in mount:
                    errors.append(f"{module['id']}/{name}: unexpected host Docker socket")
            for port in service.get("ports", []):
                if not str(port).startswith("127.0.0.1:") and not (manifest.get("mode") == "existing-core" and name == target and str(port).startswith("${MODULE_BIND_IP:")):
                    errors.append(f"{module['id']}/{name}: workstation port is not loopback-bound: {port}")
        seen, visiting = set(), set()
        def visit(name):
            if name in visiting:
                errors.append(f"{module['id']}: dependency cycle involving {name}")
                return
            if name in seen:
                return
            visiting.add(name)
            for dep in graph.get(name, []):
                visit(dep)
            visiting.remove(name)
            seen.add(name)
        for name in services:
            visit(name)
        for service, destination in [("timescaledb", "/var/lib/postgresql/data"), ("valkey", "/data")]:
            if service in services and not any(v.split(":")[1] == destination for v in services[service].get("volumes", [])):
                errors.append(f"{module['id']}/{service}: storage is not persistent")
        for path in (directory / "configs").glob("*.yaml"):
            config = yaml.safe_load(path.read_text())
            for key in ("enroll", "mesh_enroll"):
                enroll = config.get(key, {})
                if enroll.get("enabled") and (enroll.get("insecure") or not enroll.get("ca_file")):
                    errors.append(f"{module['id']}/{path.name}: enrollment lacks verified CA")
            policy = config.get("authz", {}).get("path", "")
            if manifest.get("mode") == "existing-core":
                policy = "/policies/module.yaml"
            if not policy.startswith("/policies/") or not (directory / policy.lstrip("/")).is_file():
                errors.append(f"{module['id']}/{path.name}: missing module policy")
        guide = (root / "content/guides" / module["id"] / "docker.md").read_text()
        if f"downloads/{module['id']}.zip" not in guide or "docker compose up -d" not in guide:
            errors.append(f"{module['id']}: Docker guide does not use the standalone Compose bundle")
        for code in re.findall(r"```(?:sh|bash)\n(.*?)```", guide, re.S):
            if re.search(r"^\s*docker (?:run|pull|stop|rm|exec|logs)\b", code, re.M):
                errors.append(f"{module['id']}: Docker guide contains non-Compose deployment commands")
    return errors

def compose_config(root):
    errors = []
    for path in sorted((root / "deploy/compose").glob("*/compose.yaml")):
        result = subprocess.run(["docker", "compose", "--env-file", str(path.parent / ".env.example"), "-f", str(path), "config", "--quiet"],
                                capture_output=True, text=True,
                                env={**os.environ, "OPERATOR_EMAIL": "validation@example.test", "ASTERISK_CDR_DSN": "reader:fixture@tcp(pbx.example.test:3306)/asteriskcdrdb"})
        if result.returncode:
            errors.append(f"{path.parent.name}: docker compose config failed: {result.stderr.strip()}")
        overlay = path.parent / "compose.same-host.yaml"
        if overlay.is_file():
            result = subprocess.run(["docker", "compose", "--env-file", str(path.parent / ".env.same-host.example"), "-f", str(path), "-f", str(overlay), "config", "--quiet"], capture_output=True, text=True,
                                    env={**os.environ, "CORE_NETWORK": "fixture_core_mesh", "ASTERISK_CDR_DSN": "reader:fixture@tcp(pbx.example.test:3306)/asteriskcdrdb"})
            if result.returncode:
                errors.append(f"{path.parent.name}: same-host override failed: {result.stderr.strip()}")
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docker", action="store_true", help="Also validate with Docker Compose; no daemon or containers needed")
    args = parser.parse_args()
    errors = check_bundles(ROOT)
    if args.docker:
        errors += compose_config(ROOT)
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print("PASS: 17 Compose bundles; hashes, dependency graphs, mounts, storage, enrollment and Compose guides" + ("; Docker Compose parser" if args.docker else ""))

if __name__ == "__main__":
    main()
