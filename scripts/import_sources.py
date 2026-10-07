#!/usr/bin/env python3
"""Explicitly snapshot public documentation from verified v4 checkouts."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
# Deliberately explicit. Never discover or read real deployment secret files.
COMPONENTS = [
    ("platform", "Go-Tangra Platform", "Foundation", "go-tangra", "Secure service framework, shared UI kit and development stack.", None, None, None, None),
    ("auth", "Auth", "Control plane", "go-tangra-auth", "Tenant identity, sessions, tokens and fine-grained authorization.", "authsvc", "console", "console remote", 9190),
    ("portal", "Portal / Gateway", "Control plane", "go-tangra-portal-v4", "Public application edge, leased module registry and federated shell.", "gatewaysvc", "shell", "shell", 9290),
    ("lcm", "LCM", "Control plane", "go-tangra-lcm-v4", "Mesh certificate authority, SVID enrollment and certificate lifecycle.", "lcmsvc", "ui", "ui", 9390),
    ("warden", "Warden", "Control plane", "go-tangra-warden-v4", "Vault-backed secrets management and controlled credential sharing.", "wardensvc", "ui", "ui", 9490),
    ("notification", "Notification", "Platform services", "go-tangra-notification-v4", "Central SMTP notifications, inbox messages and delivery management.", "notificationsvc", "ui", "ui", 9590),
    ("scheduler", "Scheduler", "Platform services", "go-tangra-scheduler-v4", "Typed tenant and platform jobs, cron scheduling, retries and history.", "schedulersvc", "ui", "ui", 9800),
    ("inventory", "Inventory", "Infrastructure", "go-tangra-inventory-v4", "Endpoint agents, hardware/software snapshots and change tracking.", "inventorysvc", "ui", "ui", 9810),
    ("ipam", "IPAM", "Infrastructure", "go-tangra-ipam-v4", "IP addresses, networks, active discovery and IPMI/KVM operations.", "ipamsvc", "ui", "ui", 9820),
    ("dns", "DNS", "Infrastructure", "go-tangra-dns-v4", "PowerDNS management, DNS records, IPAM synchronization and ACME challenges.", "dnssvc", "ui", "ui", 9850),
    ("deployer", "Deployer", "Infrastructure", "go-tangra-deployer-v4", "Distribute certificates to infrastructure targets and track deployment.", "deployersvc", "ui", "ui", 9690),
    ("asset", "Asset", "Business modules", "go-tangra-asset-v4", "IT asset lifecycle, consumables, licenses, insurance and depreciation.", "assetsvc", "ui", "ui", 9830),
    ("paperless", "Paperless", "Business modules", "go-tangra-paperless-v4", "Documents, object storage, text extraction, full-text search and sharing.", "paperlesssvc", "ui", "ui", 9790),
    ("ticket", "Ticket", "Business modules", "go-tangra-ticket-v4", "Email helpdesk, conversations, mailboxes and triage rules.", "ticketsvc", "ui", "ui", 9840),
    ("signing", "Signing", "Business modules", "go-tangra-signing-v4", "PDF templates, signing submissions, personal and qualified signatures.", "signingsvc", "ui", "ui", 9860),
    ("hr", "HR", "Business modules", "hr-service-v4", "Leave requests, allowances, team calendars and signing integration.", "hrsvc", "ui", "ui", 9870),
    ("sms-gw", "SMS Gateway", "Communications", "go-tangra-sms-gw-v4", "Hermes SMS API, carrier receipts, callbacks and tenant management.", "smsgwsvc", "ui", "ui", 9593),
    ("asterisk", "Asterisk", "Communications", "go-tangra-asterisk-v4", "Read-only PBX observation, call history, recordings and RTP diagnostics.", "asterisksvc", "ui", "ui", 9094),
]

DEPENDENCIES = {
    "platform": ([], []),
    "auth": (["TimescaleDB", "Valkey", "OpenFGA", "mesh identity"], ["SMTP", "LDAP directory"]),
    "portal": (["Auth", "LCM or supplied SVID", "TimescaleDB", "Valkey"], ["registered module remotes"]),
    "lcm": (["TimescaleDB", "Valkey", "key-encryption key", "Auth", "Portal"], ["ACME issuer", "DNS provider"]),
    "warden": (["TimescaleDB", "Valkey", "Vault KV/AppRole", "key-encryption key", "Auth", "Portal", "mesh identity"], []),
    "notification": (["TimescaleDB", "Valkey", "key-encryption key", "Auth", "Portal", "mesh identity"], ["SMTP delivery provider", "Scheduler"]),
    "scheduler": (["TimescaleDB", "Valkey", "Auth", "Portal", "mesh identity"], ["task-executing modules"]),
    "inventory": (["TimescaleDB", "Valkey", "Auth", "Portal", "mesh identity"], ["endpoint agents", "LCM certificate delivery"]),
    "ipam": (["TimescaleDB", "Valkey", "key-encryption key", "Auth", "Portal", "mesh identity"], ["Inventory", "Warden", "Scheduler", "ICMP capability", "IPMI targets"]),
    "dns": (["TimescaleDB", "Valkey", "PowerDNS APIs", "key-encryption key", "Auth", "Portal", "mesh identity"], ["IPAM", "Prometheus", "Docker restart integration"]),
    "deployer": (["TimescaleDB", "Valkey", "key-encryption key", "Auth", "Portal", "mesh identity"], ["LCM", "Warden", "deployment targets"]),
    "asset": (["TimescaleDB", "Valkey", "S3-compatible storage", "key-encryption key", "Auth", "Portal", "mesh identity"], ["Inventory", "Paperless", "Scheduler"]),
    "paperless": (["TimescaleDB", "Valkey", "S3-compatible storage", "Auth", "Portal", "mesh identity"], ["OpenFGA sharing", "Tika", "Gotenberg"]),
    "ticket": (["TimescaleDB", "Valkey", "S3-compatible storage", "key-encryption key", "Auth", "Portal", "mesh identity"], ["inbound email relay", "SMTP", "Notification"]),
    "signing": (["TimescaleDB", "Valkey", "S3-compatible storage", "key-encryption key", "Auth", "Portal", "mesh identity"], ["Scheduler", "Notification", "Warden", "B-Trust BISS"]),
    "hr": (["TimescaleDB", "Valkey", "Auth", "Portal", "mesh identity"], ["Signing", "Scheduler", "Notification"]),
    "sms-gw": (["PostgreSQL", "key-encryption key", "Hermes JWT secret", "Auth", "Portal", "mesh identity"], ["carrier provider", "ACME", "Prometheus"]),
    "asterisk": (["read-only PBX MySQL CDR", "Auth", "Portal", "mesh identity"], ["module-owned registration MySQL", "AMI", "read-only recordings", "dedicated Prometheus"]),
}

def git(directory, *args):
    result = subprocess.run(["git", "-C", str(directory), *args], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else "unavailable"

def public_repo(module_path):
    return "https://" + module_path.removesuffix("/v4")

def extract_config(directory):
    """Only public field names/types, never example configuration values."""
    rows = []
    candidates = [directory / "internal/config/config.go", directory / "config/config.go"]
    for path in candidates:
        if not path.is_file():
            continue
        struct = "Config"
        for line in path.read_text().splitlines():
            match = re.match(r"type (\w+) struct", line)
            if match:
                struct = match[1]
            match = re.search(r'^\s*(\w+)\s+([^`]+)`[^`]*yaml:"([^",]+)', line)
            if match and match[3] != "-":
                rows.append({"group": struct, "field": match[3], "type": match[2].strip(), "path": str(path.relative_to(directory))})
    return rows

def extract_api(directory):
    rows = []
    for path in sorted((directory / "api/openapi").glob("*.yaml")):
        document = yaml.safe_load(path.read_text())
        for endpoint, methods in document.get("paths", {}).items():
            for method, operation in methods.items():
                if method not in {"get", "post", "put", "patch", "delete", "options", "head"}:
                    continue
                rows.append({"method": method.upper(), "path": endpoint,
                             "summary": operation.get("summary", operation.get("operationId", "")),
                             "permission": operation.get("x-freya-permission", ""),
                             "source": str(path.relative_to(directory))})
    return rows

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    modules = []
    for id_, name, category, checkout, summary, binary, ui, tags, port in COMPONENTS:
        directory = args.root.resolve() / checkout
        if not (directory / "README.md").is_file():
            raise SystemExit(f"Missing required v4 repository: {directory}")
        go_mod = (directory / "go.mod").read_text()
        module_path = re.search(r"^module (.+)$", go_mod, re.M)[1]
        if not module_path.endswith("/v4"):
            raise SystemExit(f"Refusing non-v4 module: {module_path}")
        commit = git(directory, "rev-parse", "HEAD")
        tag = git(directory, "describe", "--tags", "--match", "v4.*", "--abbrev=0")
        repo = public_repo(module_path)
        required, optional = DEPENDENCIES[id_]
        config_path = "configs/dev.yaml" if id_ == "asterisk" else "deploy/container.yaml"
        if not (directory / config_path).is_file():
            config_path = "deploy/dev.yaml" if binary else "docs/configuration.md"
        cli = (directory / "cmd" / binary / "main.go").read_text() if binary and (directory / "cmd" / binary / "main.go").exists() else ""
        sources = [directory / "README.md"]
        sources += sorted((directory / "docs").glob("*.md"))
        sources += [directory / "deploy/README.md"]
        if id_ == "platform":
            sources += [directory / "deploy/stack/README.md", directory / "deploy/stack/ENROLLMENT.md", directory / "contrib/README.md", directory / "contrib/audit-timescale/README.md", directory / "contrib/policy-valkey/README.md", directory / "ui/kit/README.md"]
        docs = []
        for source in sources:
            if not source.is_file():
                continue
            rel = source.relative_to(directory)
            data = source.read_bytes()
            dest = ROOT / "content/sources" / id_ / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            docs.append({"path": str(rel), "sha256": hashlib.sha256(data).hexdigest(), "url": f"{repo}/blob/{commit}/{rel}"})
        modules.append({"id": id_, "name": name, "category": category, "summary": summary,
                        "checkout": checkout, "repository": repo, "module": module_path,
                        "commit": commit, "tag": tag, "go_version": re.search(r"^go (.+)$", go_mod, re.M)[1],
                        "toolchain": re.search(r"^toolchain (.+)$", go_mod, re.M)[1],
                        "binary": binary, "ui_dir": ui, "build_tags": tags,
                        "admin_port": port, "config_path": config_path,
                        "image": f"ghcr.io/go-tangra/go-tangra-{id_}" if binary else None,
                        "stack_service": "gateway" if id_ == "portal" else id_ if binary and id_ not in {"scheduler", "sms-gw", "asterisk"} else None,
                        "bootstrap": "bootstrap" in cli, "required": required, "optional": optional,
                        "sources": docs, "config_fields": extract_config(directory), "api_operations": extract_api(directory),
                        "validation": "source-reviewed"})
    out = ROOT / "content/modules.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"snapshot_date": "2026-10-05", "major": "v4", "modules": modules}, indent=2) + "\n")
    print(f"Snapshotted {len(modules)} v4 components and {sum(len(m['sources']) for m in modules)} source documents.")

if __name__ == "__main__":
    main()
