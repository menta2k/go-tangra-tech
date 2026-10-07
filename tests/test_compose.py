import hashlib
import importlib.util
import json
import os
import sys
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

checker = load("check_compose")
builder = load("build")
generator = load("create_compose")

class ComposeContractTests(unittest.TestCase):
    def test_every_standalone_bundle_has_resolvable_bootstrap_graph(self):
        self.assertEqual([], checker.check_bundles(ROOT))

    @unittest.skipUnless(shutil.which("docker"), "Docker CLI unavailable")
    def test_all_bundles_are_accepted_by_docker_compose(self):
        result = subprocess.run(["docker", "compose", "version"], capture_output=True)
        if result.returncode:
            self.skipTest("Docker Compose CLI unavailable")
        self.assertEqual([], checker.compose_config(ROOT))

    def test_zip_downloads_match_reviewed_bundles(self):
        for directory in sorted((ROOT / "deploy/compose").iterdir()):
            if not directory.is_dir():
                continue
            manifest = json.loads((directory / "bundle.json").read_text())
            with zipfile.ZipFile(ROOT / "dist/downloads" / f"{directory.name}.zip") as archive:
                expected = {f"{directory.name}/{name}" for name in manifest["files"]}
                self.assertEqual(expected, set(archive.namelist()))
                for name, digest in manifest["files"].items():
                    self.assertEqual(digest, hashlib.sha256(archive.read(f"{directory.name}/{name}")).hexdigest())
                self.assertNotIn(f"{directory.name}/.env", archive.namelist())

    def test_private_env_is_excluded_and_changed_reviewed_files_fail(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source = root / "source"
            bundle = source / "module"
            bundle.mkdir(parents=True)
            data = b"services: {}\n"
            (bundle / "compose.yaml").write_bytes(data)
            (bundle / ".env").write_text("SECRET=never-package\n")
            (bundle / "bundle.json").write_text(json.dumps({"files": {"compose.yaml": hashlib.sha256(data).hexdigest()}}))
            builder.package_compose(source, root / "downloads")
            with zipfile.ZipFile(root / "downloads/module.zip") as archive:
                self.assertEqual(["module/compose.yaml"], archive.namelist())
            (bundle / "compose.yaml").write_text("modified\n")
            with self.assertRaisesRegex(ValueError, "without review"):
                builder.package_compose(source, root / "second")

    def test_package_rejects_path_traversal(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "source/module").mkdir(parents=True)
            (root / "source/module/bundle.json").write_text(json.dumps({"files": {"../outside.env": "bad"}}))
            with self.assertRaisesRegex(ValueError, "Unsafe"):
                builder.package_compose(root / "source", root / "downloads")

    def test_key_initialization_preserves_existing_keys(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "auth").mkdir()
            script = generator.KEYS_SCRIPT.replace("/keys/", str(root) + "/")
            subprocess.run(["sh", "-c", script], check=True, capture_output=True)
            key = (root / "auth/kek").read_bytes()
            subprocess.run(["sh", "-c", script], check=True, capture_output=True)
            self.assertEqual(key, (root / "auth/kek").read_bytes())
            self.assertEqual(0o600, (root / "auth/kek").stat().st_mode & 0o777)

    def test_vault_scripts_parse_recovery_material_without_secret_output(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "bootstrap").mkdir()
            (root / "creds").mkdir()
            binary = root / "vault"
            binary.write_text('''#!/bin/sh
case "$1 $2" in
 "server "*) sleep 0.3 ;;
 "status -format=json") printf '%s\\n' '{"initialized":false}'; exit 2 ;;
 "operator init") cat <<'JSON'
{
  "unseal_keys_b64": [
    "Zml4dHVyZQ=="
  ],
  "root_token": "fixture-token"
}
JSON
 ;;
 "operator unseal") [ "$3" = "Zml4dHVyZQ==" ] || exit 1 ;;
esac
''')
            binary.chmod(0o755)
            script = generator.VAULT_START.replace("/vault-bootstrap", str(root / "bootstrap")).replace("/tmp/vault-status.json", str(root / "status.json"))
            result = subprocess.run(["sh", "-c", script], env={**os.environ, "PATH": str(root) + ":" + os.environ["PATH"]}, capture_output=True, text=True, timeout=5)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertNotIn("Zml4dHVyZQ==", result.stdout)
            approle = root / "approle.sh"
            approle.write_text(f'''[ "$VAULT_TOKEN" = "fixture-token" ] || exit 1
printf role > '{root}/creds/role_id'
printf secret > '{root}/creds/secret_id'
''')
            script = generator.VAULT_INIT.replace("/vault-bootstrap", str(root / "bootstrap")).replace("/vault-creds", str(root / "creds")).replace("/vault-approle.sh", str(approle))
            result = subprocess.run(["sh", "-c", script], capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertNotIn("fixture-token", result.stdout)

    def test_asterisk_keeps_registration_store_separate_from_pbx(self):
        directory = ROOT / "deploy/compose/asterisk"
        config = yaml.safe_load((directory / "configs/module.yaml").read_text())
        self.assertEqual("${ASTERISK_CDR_DSN}", config["binding"]["cdr_dsn"])
        self.assertIn("local-asterisk-registration-db:3306", config["binding"]["registration_dsn"])
        sql = (directory / "registration.sql").read_text()
        self.assertNotIn("cdr", sql.lower())
        self.assertNotIn("pbx", sql.lower())

    def test_writable_storage_and_private_probe_for_distroless_modules(self):
        for id_ in ["sms-gw", "asterisk"]:
            compose = yaml.safe_load((ROOT / "deploy/compose" / id_ / "compose.yaml").read_text())
            self.assertEqual(f"service:{id_}", compose["services"]["check"]["network_mode"])
            self.assertTrue(any(v.split(":")[1] == "/state" for v in compose["services"][id_]["volumes"]))
            self.assertIn("--profile checks run --rm check", (ROOT / "content/guides" / id_ / "docker.md").read_text())

if __name__ == "__main__":
    unittest.main()
