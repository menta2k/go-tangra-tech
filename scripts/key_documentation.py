"""Explain the key initialization job from its actual Compose mounts."""
import yaml


def key_documentation(compose_text):
    compose = yaml.safe_load(compose_text)
    job = compose['services'].get('keys-init')
    if not job:
        return ''
    rows = []
    for mount in job.get('volumes', []):
        volume, destination, *_ = mount.split(':')
        if destination.startswith('/keys/'):
            service = destination.rsplit('/', 1)[1]
            rows.append((volume, destination + '/kek', '/keys/kek', service + ' key-encryption key (KEK)'))
        elif destination == '/sms-secrets':
            rows.extend([(volume, '/sms-secrets/kek', '/secrets/kek', 'SMS Gateway key-encryption key (KEK)'),
                         (volume, '/sms-secrets/jwt.key', '/secrets/jwt.key', 'SMS Gateway public Hermes JWT secret')])
    text = '''\n## Key initialization: init-keys.sh

The bundle includes `init-keys.sh`; keep it beside `compose.yaml` when copying or extracting the bundle. You do not need to create the script or run it on the host. Compose mounts it read-only into the one-shot Alpine `keys-init` container and invokes it with `sh /init-keys.sh`, so an executable bit is not required. `docker compose up -d` runs the job automatically. Dependent application/initialization services wait for its successful completion (`service_completed_successfully`).

The script reads 32 random bytes from `/dev/urandom` for each missing or empty key file and writes them as base64 text. It uses a temporary file followed by a rename, sets `umask 077`, and applies file mode `0600`. Existing nonempty key files are preserved; the script does not validate or rotate them. The workstation container runs as root so it can initialize these private named volumes; application containers mount their key volume read-only.

| Named volume | File created inside keys-init | Application path | Purpose |
| --- | --- | --- | --- |
'''
    for volume, created, application, purpose in rows:
        text += f'| `{volume}` | `{created}` | `{application}` | {purpose} |\n'
    text += '''
These are application secrets, not enrollment tokens, mesh CA keys or workload certificates. In the existing-core workflow you still supply the Auth-signed enrollment token and public mesh CA separately. The SMS Hermes JWT secret is separate from Auth's platform token signing keys. No generated key is included in the downloadable bundle or printed by the script.

Check initialization without displaying keys:

```sh
docker compose ps -a keys-init
docker compose logs --tail=100 keys-init
```

Expected: the job exits with code 0. An exited one-shot container is normal; a nonzero exit blocks dependent services. For a failure, check the script mount, volume permissions and available disk space, then correct the issue before retrying startup. Do not delete a key volume as a troubleshooting shortcut.

Named volumes preserve these keys across container recreation and `docker compose down`. Back up each key volume together with the database/object data it protects, and restore the matching set. `docker compose down -v` deletes the keys along with this project's other named volumes. A subsequent startup creates new keys, which cannot decrypt data encrypted with the old keys. For an existing-data migration, restore its original keys before startup rather than letting this script generate replacements. Key rotation requires the module's supported migration/rotation procedure; rerunning this initializer is not rotation.
'''
    return text
