import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


class ExistingCoreTests(unittest.TestCase):
    def modules(self):
        for directory in sorted((ROOT / 'deploy/compose').iterdir()):
            if directory.is_dir():
                manifest = json.loads((directory / 'bundle.json').read_text())
                if manifest.get('mode') == 'existing-core':
                    yield directory, manifest

    def test_addons_run_one_application_with_routable_registered_endpoints(self):
        count = 0
        for directory, manifest in self.modules():
            count += 1
            compose = yaml.safe_load((directory / 'compose.yaml').read_text())
            self.assertEqual([manifest['service']], manifest['applications'])
            self.assertFalse({'auth', 'gateway', 'lcm'} & set(compose['services']))
            self.assertEqual({'default'}, set(compose['networks']))
            overlay = yaml.safe_load((directory / 'compose.same-host.yaml').read_text())
            self.assertTrue(overlay['networks']['mesh']['external'])
            self.assertFalse(any(name.endswith('-token') for name in compose['services']))
            target = compose['services'][manifest['service']]
            self.assertNotIn('mesh', target['networks'])
            self.assertIn('FREYA_ADVERTISE_HOST', target['environment'])
            config = yaml.safe_load((directory / 'configs/module.yaml').read_text())
            for address in config['server'].values():
                port = address.rsplit(':', 1)[1]
                self.assertTrue(any(value.startswith('${MODULE_BIND_IP:') and value.endswith(':' + port + ':' + port) for value in target['ports']))
            self.assertIn('MODULE_ADVERTISE_HOST', target['environment']['FREYA_ADVERTISE_HOST'])
            self.assertTrue(any(v.endswith(':/tokens/enrollment.token:ro') for v in target['volumes']))
            self.assertTrue(any(v.endswith(':/certs/ca.pem:ro') for v in target['volumes']))
        self.assertEqual(14, count)

    def test_render_all_modules_with_different_realistic_core_settings(self):
        for directory, manifest in self.modules():
            with self.subTest(module=directory.name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary) / directory.name
                shutil.copytree(directory, root)
                (root / 'private').mkdir()
                (root / 'private/enrollment.token').write_text('private-token-fixture')
                (root / 'private/ca.pem').write_text('public-ca-fixture')
                settings = (root / '.env.example').read_text().replace('example.org', 'mesh.acme.test').replace('https://portal.internal.example', 'https://portal.acme.test').replace('core.internal.example:9543', 'core-auth:19543').replace('core.internal.example:9643', 'core-portal:19643').replace('core.internal.example:9945', 'core-lcm:19945').replace('https://core.internal.example:9947', 'https://core-lcm:19947')
                (root / '.env').write_text(settings)
                result = subprocess.run(['python3', str(root / 'configure.py')], capture_output=True, text=True)
                self.assertEqual(0, result.returncode, result.stderr)
                config = yaml.safe_load((root / 'runtime/config.yaml').read_text())
                self.assertEqual('mesh.acme.test', config['trust_domain'])
                enroll = config.get('enroll', config.get('mesh_enroll'))
                self.assertEqual('spiffe://mesh.acme.test/svc/lcm', enroll['server_spiffe_id'])
                self.assertEqual('https://core-lcm:19947/api/lcm/v1/enroll', enroll['enroll_url'])
                self.assertEqual(['core-auth:19543'], config['discovery']['static']['auth'])
                self.assertEqual(['core-portal:19643'], config['discovery']['static']['gateway'])
                self.assertEqual('https://portal.acme.test', config['gateway']['issuer'])
                compose = yaml.safe_load((root / 'compose.yaml').read_text())
                for name, service in compose['services'].items():
                    if name in {'timescaledb', 'valkey', 'registration-db', 'vault', 'mailpit'}:
                        self.assertIn(f'local-{manifest["service"]}-{name}', service['networks']['default']['aliases'])
                for name in ('auth', 'gateway', 'lcm'):
                    self.assertFalse((root / 'runtime').joinpath(name + '.yaml').exists())
                policy = (root / 'runtime/policy.yaml').read_text()
                self.assertNotIn('spiffe://example.org/', policy)
                self.assertNotIn('@@', policy)
                self.assertIn('spiffe://mesh.acme.test/', policy)
                self.assertEqual(0o600, (root / 'runtime/config.yaml').stat().st_mode & 0o777)
                self.assertNotIn('private-token-fixture', result.stdout + result.stderr)

    def test_renderer_rejects_missing_credentials_and_unsafe_interpolation(self):
        directory = ROOT / 'deploy/compose/notification'
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'notification'
            shutil.copytree(directory, root)
            (root / '.env').write_text((root / '.env.example').read_text())
            result = subprocess.run(['python3', str(root / 'configure.py')], capture_output=True, text=True)
            self.assertNotEqual(0, result.returncode)
            self.assertFalse((root / 'runtime').exists())
            (root / '.env').write_text((root / '.env.example').read_text().replace('TRUST_DOMAIN=example.org', "TRUST_DOMAIN=bad'quoted"))
            result = subprocess.run(['python3', str(root / 'configure.py')], capture_output=True, text=True)
            self.assertNotEqual(0, result.returncode)
            self.assertIn('TRUST_DOMAIN', result.stderr)

    def test_core_bundle_guides_clearly_identify_bootstrap_scope(self):
        for id_ in ['auth', 'portal', 'lcm']:
            manifest = json.loads((ROOT / 'deploy/compose' / id_ / 'bundle.json').read_text())
            self.assertEqual('core-bootstrap', manifest['mode'])
            self.assertIn('Core bootstrap only', (ROOT / 'content/guides' / id_ / 'docker.md').read_text())
