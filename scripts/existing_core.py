"""Adapt workstation module bundles to enroll into an existing mesh."""
import copy
import hashlib
import json
import re
from pathlib import Path

import yaml

CORE = {'auth', 'lcm', 'gateway'}

CONFIGURE = r'''#!/usr/bin/env python3
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
'''


def adapt(source, files, manifest, modules, get_config, database_sql):
    target = manifest['service']
    if target in CORE:
        manifest['mode'] = 'core-bootstrap'
        files['README.md'] = '**Initial core bootstrap only.** If Auth/Portal/LCM already run, use the add-on module bundles to enroll services; do not start a second core from this directory.\n\n' + files['README.md']
        manifest['files']['README.md'] = hashlib.sha256(files['README.md'].encode()).hexdigest()
        return files, manifest
    bundle = yaml.safe_load(files['compose.yaml'])
    services = bundle['services']
    # Drop every other application and all of its initialization jobs.
    applications = set(manifest['applications'])
    remove = (applications - {target}) | {n for n in services if n.endswith('-token')} | {'renewer', 'gateway-bootstrap', 'auth-bootstrap', 'lcm-bootstrap', 'certs-init', 'openfga', 'openfga-migrate'}
    for name in list(services):
        if name in remove or any(name.startswith(app + '-') for app in applications - {target}):
            services.pop(name)
    # Retain infrastructure only if reachable from the selected module's graph.
    for service in services.values():
        service['depends_on'] = {k: v for k, v in service.get('depends_on', {}).items() if k in services}
    selected = set()
    def visit(name):
        if name in selected:
            return
        selected.add(name)
        for dep in services[name].get('depends_on', {}):
            visit(dep)
    visit(target)
    selected.add('check')
    if 'mailpit' in services and 'mailpit' in files[f'configs/{target}.yaml']:
        selected.add('mailpit')
        services['mailpit'].pop('ports', None)
    services = {k: v for k, v in services.items() if k in selected}
    bundle['services'] = services
    config = yaml.safe_load(files[f'configs/{target}.yaml'])
    original = get_config(source, target)
    # Restore optional peer discovery pruned by the former all-in-one bundle.
    discovery = {**original.get('discovery', {}).get('static', {}), **config.get('discovery', {}).get('static', {})}
    discovery.update({'auth': ['@@AUTH_GRPC@@'], 'gateway': ['@@GATEWAY_GRPC@@'], 'lcm': ['@@LCM_GRPC@@']})
    config['discovery']['static'] = discovery
    config['trust_domain'] = '@@TRUST_DOMAIN@@'
    config['env'] = '@@MESH_ENV@@'
    enroll = config.get('enroll', config.get('mesh_enroll'))
    enroll.update({'enabled': True, 'tenant_id': '@@TENANT_ID@@', 'token_file': '/tokens/enrollment.token',
                   'enroll_url': '@@LCM_ENROLL_URL@@', 'lcm_grpc': '@@LCM_GRPC@@', 'ca_file': '/certs/ca.pem',
                   'server_spiffe_id': 'spiffe://@@TRUST_DOMAIN@@/svc/lcm', 'insecure': False})
    config.setdefault('gateway', {})['issuer'] = '@@GATEWAY_ISSUER@@'
    local_hosts = {name: f'local-{target}-{name}' for name in services if name not in {target, f'{target}-bootstrap', 'check', 'keys-init'} and not name.endswith('-init')}
    def rewrite(value):
        if isinstance(value, dict):
            return {key: rewrite(item) for key, item in value.items()}
        if isinstance(value, list):
            return [rewrite(item) for item in value]
        if isinstance(value, str):
            value = value.replace('https://localhost:8443', '@@GATEWAY_ISSUER@@')
            for host, alias in local_hosts.items():
                value = re.sub(r'(?<![A-Za-z0-9_-])' + re.escape(host) + r'(?=:)', alias, value)
            return value
        return value
    config = rewrite(config)
    files['configs/module.yaml'] = yaml.safe_dump(config, sort_keys=False, width=1000)
    files['policies/module.yaml'] = files[f'policies/{target}.yaml'].replace('spiffe://example.org/', 'spiffe://@@TRUST_DOMAIN@@/')
    for path in list(files):
        if (path.startswith(('configs/', 'policies/')) and path not in {'configs/module.yaml', 'policies/module.yaml'}):
            del files[path]
    for name, service in services.items():
        mounts = []
        for mount in service.get('volumes', []):
            if mount.startswith('tokens:'):
                mounts.append('${ENROLLMENT_TOKEN_FILE:-./private/enrollment.token}:/tokens/enrollment.token:ro')
            elif mount.startswith('certs:'):
                mounts.append('${MESH_CA_FILE:-./private/ca.pem}:/certs/ca.pem:ro')
            elif mount.startswith(f'./configs/{target}.yaml:'):
                mounts.append('./runtime/config.yaml:' + mount.split(':', 1)[1])
            elif mount.startswith(f'./policies/{target}.yaml:'):
                mounts.append('./runtime/policy.yaml:' + mount.split(':', 1)[1])
            else:
                mounts.append(mount)
        service['volumes'] = mounts
        service['networks'] = {'default': {'aliases': [local_hosts[name]]}} if name in local_hosts else ['default']
        if name == target:
            service['networks'] = {'default': {'aliases': [target]}}
            service.setdefault('environment', {})['FREYA_ADVERTISE_HOST'] = '${MODULE_ADVERTISE_HOST:?Set a module host reachable from the core}'
            for address in config['server'].values():
                port = int(address.rsplit(':', 1)[1])
                service.setdefault('ports', []).append('${MODULE_BIND_IP:?Set the private module host bind IP}:' + str(port) + ':' + str(port))
        elif name == f'{target}-bootstrap':
            service['networks'] = ['default']
        elif name == 'check':
            service.pop('networks', None)
    if 'keys-init' in services:
        service = services['keys-init']
        service['volumes'] = [v for v in service['volumes'] if not v.startswith(tuple(app + '-keys:' for app in applications - {target}))]
    if 'keys-init' in services and len(services['keys-init']['volumes']) == 1:
        del services['keys-init']
        for service in services.values():
            service.get('depends_on', {}).pop('keys-init', None)
    files['init-db.sql'] = database_sql({target: config}).replace('CREATE DATABASE openfga;\n', '')
    volumes = {}
    for service in services.values():
        for mount in service.get('volumes', []):
            name = mount.split(':', 1)[0]
            if not name.startswith(('.', '/', '$')):
                volumes[name] = {}
    bundle['volumes'] = volumes
    bundle['networks'] = {'default': {}}
    files['compose.same-host.yaml'] = yaml.safe_dump({'services': {target: {'networks': {'mesh': {'aliases': [target]}}}}, 'networks': {'mesh': {'external': True, 'name': '${CORE_NETWORK:?Set the existing local core network}'}}}, sort_keys=False)
    files['compose.yaml'] = '# Module enrollment into an existing core; no new Auth, Portal or LCM.\n' + yaml.safe_dump(bundle, sort_keys=False, width=1000)
    module = modules[manifest['module']]
    files['.env.example'] = f'''# Copy to private .env and replace with values from your existing core.
MODULE_ADVERTISE_HOST=module.internal.example
MODULE_BIND_IP=10.20.0.20
TRUST_DOMAIN=example.org
TENANT_ID=00000000-0000-0000-0000-000000000001
MESH_ENV=dev
AUTH_GRPC=core.internal.example:9543
GATEWAY_GRPC=core.internal.example:9643
LCM_GRPC=core.internal.example:9945
LCM_ENROLL_URL=https://core.internal.example:9947/api/lcm/v1/enroll
GATEWAY_ISSUER=https://portal.internal.example
ENROLLMENT_TOKEN_FILE=./private/enrollment.token
MESH_CA_FILE=./private/ca.pem
{module['id'].upper().replace('-', '_')}_VERSION={module['tag'].removeprefix('v')}
'''
    if target == 'asterisk':
        files['.env.example'] += 'ASTERISK_CDR_DSN=\n'
    if target == 'sms-gw':
        files['.env.example'] += 'SMS_PORT=9901\n'
    files['.env.same-host.example'] = files['.env.example'].replace('MODULE_ADVERTISE_HOST=module.internal.example', 'MODULE_ADVERTISE_HOST=' + target).replace('MODULE_BIND_IP=10.20.0.20', 'MODULE_BIND_IP=127.0.0.1').replace('core.internal.example:9543', 'auth:9543').replace('core.internal.example:9643', 'gateway:9643').replace('core.internal.example:9945', 'lcm:9945').replace('core.internal.example:9947', 'lcm:9947') + 'CORE_NETWORK=tangra_mesh\nCOMPOSE_FILE=compose.yaml:compose.same-host.yaml\n'
    files['configure.py'] = CONFIGURE
    files['README.md'] = f'''# Add {module['name']} to an existing Go-Tangra core

Runs only `{target}` and its local infrastructure. Auth, Portal/Gateway, LCM and peer modules must already be reachable. Docker networks do not span hosts; default installation uses routed core addresses and publishes the module mesh listeners on its private host interface. This is a workstation example with development store credentials; choose published compatible images and adapt infrastructure for production.

1. Set routable core endpoints in .env. The default compose.yaml supports a core on another host over a private routed network/VPN. Set MODULE_ADVERTISE_HOST to the module host DNS/IP reachable from the core and MODULE_BIND_IP to that host’s private interface IP. Mesh ports are published unchanged, matching their registered ports; keep admin listeners private. CORE_NETWORK is only used by the optional compose.same-host.yaml overlay when the core shares this Docker daemon.
2. Using the existing Auth signing keys, mint a short-lived token for `spiffe://YOUR_TRUST_DOMAIN/svc/{target}`. Save it privately at the configured ENROLLMENT_TOKEN_FILE path, and copy the existing mesh CA bundle to MESH_CA_FILE. Never copy a CA private key. The download contains neither token nor CA material.
For same-host installation, use .env.same-host.example as .env and set CORE_NETWORK to a network on this Docker daemon. Its COMPOSE_FILE setting enables compose.same-host.yaml automatically.

3. Authorize that exact SPIFFE identity/prefix on the existing gateway and allow required RPCs on Auth/LCM and other peers. Do this through the existing core's managed configuration, not by running a new core bootstrap job. See the website guide for registration instructions.
4. Configure required existing peer modules and reciprocal policy/consumer grants. Templates retain peer discovery addresses from the recorded source; edit configs/module.yaml for your topology and optional feature settings. Run configure.py after every template/.env change. Runtime YAML is rendered explicitly because most services do not expand environment variables in YAML.

```sh
cp .env.example .env
# Edit .env, install the enrollment token/CA files, and review templates/policies.
python3 configure.py
docker compose config --quiet
docker compose pull
docker compose up -d
docker compose logs --tail=100 {target}
docker compose --profile checks run --rm check
```

Sign into your existing Portal, confirm {module['name']} appears, assign its module permissions in Auth and perform an authorized read. Enrollment obtains identity, registration announces routes/UI and Auth permissions, and resource/user grants remain separate. Readiness alone does not prove those business operations.

Identity is persisted in `{target}-state`; keys and stores also use named volumes. A token is short-lived and single-use: restarting preserves state, but deleting identity requires a fresh token. `docker compose down` removes these containers and the local network, preserves volumes, and does not touch the remote core; the optional same-host external network is also retained. `docker compose down -v` irreversibly deletes this module's data/keys/identity; revoke its identity and retire its gateway/permission registrations deliberately when uninstalling.

Existing peers are not started automatically. For Asterisk supply SELECT-only external PBX CDR credentials; registration storage is separate. For SMS configure a carrier/client. DNS socket restart control is disabled; restart its local PowerDNS services explicitly. Optional integrations require their own configuration and acceptance checks.

No live deployment acceptance or published release compatibility is claimed. Documentation and templates are derived from the recorded public sources.
'''
    # Remove support files left over from applications/infrastructure no longer mounted.
    used = {v.split(':', 1)[0][2:] for service in services.values() for v in service.get('volumes', []) if v.startswith('./') and not v.startswith('./runtime/')}
    keep = used | {'compose.yaml', 'compose.same-host.yaml', '.env.example', '.env.same-host.example', 'README.md', 'configure.py', 'configs/module.yaml', 'policies/module.yaml'}
    files = {p: value for p, value in files.items() if p in keep}
    manifest.update({'mode': 'existing-core', 'topology': 'remote-core', 'applications': [target], 'services': sorted(services),
                     'generated_files': ['runtime/config.yaml', 'runtime/policy.yaml'],
                     'files': {p: hashlib.sha256(value.encode()).hexdigest() for p, value in sorted(files.items())}})
    return files, manifest
