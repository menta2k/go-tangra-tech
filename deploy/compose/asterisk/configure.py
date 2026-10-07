#!/usr/bin/env python3
"""Render private module configuration; uses only the Python standard library."""
import json
import os
import re
from pathlib import Path

root = Path(__file__).resolve().parent
settings = {}
for raw in (root / '.env').read_text().splitlines():
    line = raw.strip()
    if not line or line.startswith('#'):
        continue
    key, separator, value = line.partition('=')
    if not separator:
        raise SystemExit('Invalid .env assignment')
    settings[key.strip()] = value.strip().strip('"').strip("'")
patterns = {
    'TRUST_DOMAIN': r'[A-Za-z0-9][A-Za-z0-9.-]*',
    'TENANT_ID': r'[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}',
    'MESH_ENV': r'[A-Za-z0-9_-]+',
    'GATEWAY_ISSUER': r'https://[A-Za-z0-9.:-]+(?:/[A-Za-z0-9._/-]*)?',
    'LCM_ENROLL_URL': r'https://[A-Za-z0-9.:-]+/[A-Za-z0-9._/-]+',
}
patterns['MODULE_ADVERTISE_HOST'] = r'[A-Za-z0-9][A-Za-z0-9.-]*'
patterns['MODULE_BIND_IP'] = r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}'
for name in ('AUTH_GRPC', 'GATEWAY_GRPC', 'LCM_GRPC'):
    patterns[name] = r'[A-Za-z0-9.-]+:[0-9]+'
for name, pattern in patterns.items():
    value = settings.get(name, '')
    if not re.fullmatch(pattern, value):
        raise SystemExit('Set a valid ' + name + ' in .env')
for name in ('ENROLLMENT_TOKEN_FILE', 'MESH_CA_FILE'):
    path = Path(settings.get(name, ''))
    if not path.is_absolute():
        path = root / path
    if not path.is_file() or not path.stat().st_size:
        raise SystemExit('Supply the existing core material named by ' + name)
    settings[name] = str(path.resolve())
# Absolute paths also let Compose bind the supplied files unambiguously.
# .env remains private and is never part of the reviewed bundle downloads.
os.umask(0o077)
runtime = root / 'runtime'
runtime.mkdir(exist_ok=True)
for source, destination in [('configs/module.yaml', 'config.yaml'), ('policies/module.yaml', 'policy.yaml')]:
    text = (root / source).read_text()
    for name in patterns:
        text = text.replace('@@' + name + '@@', settings[name])
    if '@@' in text:
        raise SystemExit('Unresolved configuration placeholder')
    path = runtime / destination
    path.write_text(text)
    path.chmod(0o600)
print('Private runtime configuration rendered. Review it before starting Compose.')
