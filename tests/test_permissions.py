import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from import_permissions import extract
from permission_content import permission_section


class PermissionDocumentationTests(unittest.TestCase):
    def test_snapshots_and_catalogue_are_consistent(self):
        catalogue = json.loads((ROOT / 'content/permissions.json').read_text())['modules']
        modules = json.loads((ROOT / 'content/modules.json').read_text())['modules']
        self.assertEqual(set(catalogue), {m['id'] for m in modules} - {'platform', 'portal'})
        for id_, data in catalogue.items():
            raw = (ROOT / data['snapshot']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), data['sha256'], id_)
            self.assertEqual(extract(raw.decode()), data['permissions'], id_)
            refs = [p['ref'] for p in data['permissions']]
            self.assertEqual(len(refs), len(set(refs)), id_)

    def test_every_permission_and_matching_endpoint_is_documented(self):
        modules = json.loads((ROOT / 'content/modules.json').read_text())['modules']
        catalogue = json.loads((ROOT / 'content/permissions.json').read_text())['modules']
        for module in modules:
            rendered = permission_section(module)
            self.assertIn(rendered, (ROOT / 'content/modules' / (module['id'] + '.md')).read_text())
            if module['id'] not in catalogue:
                continue
            for row in catalogue[module['id']]['permissions']:
                self.assertIn(f"### {module['id']}:{row['ref']}", rendered)
                for operation in module['api_operations']:
                    if operation.get('permission') == row['ref']:
                        self.assertIn(f"`{operation['method']}` | `{operation['path']}`", rendered)

    def test_exceptional_access_scopes_are_explained(self):
        modules = {m['id']: m for m in json.loads((ROOT / 'content/modules.json').read_text())['modules']}
        self.assertIn('does not make administrative actions anonymous', permission_section(modules['auth']))
        self.assertIn('Tenant owner/admin is not platform-admin', permission_section(modules['dns']))
        self.assertIn('across all tenants', permission_section(modules['sms-gw']))
        self.assertIn('API roles alone do not give access', permission_section(modules['paperless']))
        self.assertIn('does not declare a separate Portal', permission_section(modules['portal']))
