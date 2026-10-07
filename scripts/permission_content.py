"""Render the checked-in, source-derived permission catalogue."""
import json
from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1] / 'content'

NOTES = {
    'auth': 'Auth authenticates its console with its own session cookie and enforces tenant authorization internally. Its gateway routes are marked public to permit that authentication flow; this does not make administrative actions anonymous. User/group role assignment cannot grant permissions the actor lacks (owners have the documented exemption), and the last owner is protected. Tenant operations are reserved for platform operators.',
    'lcm': 'Certificate permissions apply to certificates/SVIDs the caller is granted. Issuance, revocation, deployment, issuer management and secret access are separate capabilities; a read grant does not imply those operations.',
    'warden': 'API permissions are combined with resource grants on secrets and folders. Owner/editor/viewer/sharer relationships, expiry and folder inheritance constrain which secrets a caller can reach. Revealing passwords is sensitive even when the permission is named read.',
    'notification': 'Channel and template resource grants still apply on top of module roles; sending requires the relevant use access. The administrator module role excludes events:publish, which is a module capability; owner/admin built-in grants retain it. Reading channel settings returns redacted settings.',
    'paperless': 'The module additionally checks Zanzibar grants on each document or category. API roles alone do not give access to every document. Sharing viewer/sharer access requires share access; granting/revoking editor or owner requires owner control. A revoke affects grants on the named resource.',
    'dns': 'Server configuration, supermaster creation/deletion and cross-tenant restore require platform administration. Tenant owner/admin is not platform-admin. config:manage is absent from the built-in tenant-role grants. Mesh reads, IPAM synchronization and LCM ACME challenges have separate actor allow-lists.',
    'inventory': 'User UI permissions do not grant peer services access to host reports. A consumer needs the configured consumer allow-list and matching service policy; endpoint agents use their own enrollment/reporting identity.',
    'hr': 'Permissions distinguish team-calendar visibility, personal requests and HR administration. Request-review workflow rules still apply: nobody reviews their own request. Signing-required requests also depend on the configured Signing workflow.',
    'sms-gw': 'Provider read operations redact credentials. dashboard:read exposes deployment-wide monitoring totals across all tenants; grant it only to users who should see that scope. Public Hermes clients authenticate separately from browser module permissions.',
    'asterisk': 'The observer is pinned to one PBX and tenant and reads the PBX through SELECT-only credentials. Recordings have their own permission and are excluded from the viewer role; investigator includes them. Live, registration, recordings and monitoring still require their respective configured integrations.',
}


def cell(value):
    return value.replace('|', '&#124;').replace('\n', ' ')


def permission_section(module):
    id_ = module['id']
    if id_ == 'platform':
        return '\n## Permissions and authorization\n\nThe framework provides service identity and service-policy enforcement; it has no standalone user permission catalogue. Each service declares its own module-scoped permissions. See the [permission assignment and enforcement guide](architecture/security.html#assign-and-verify-permissions).\n'
    if id_ == 'portal':
        url = f"{module['repository']}/blob/{module['commit']}/internal/app/permissions.go"
        return f'\n## Permissions and authorization\n\nPortal registers and checks the permissions supplied by each module manifest; it does not declare a separate Portal user permission catalogue at this revision. It registers permission definitions on modules’ behalf; modules register their own roles and built-in grants. Route permission checks and UI abilities come from those manifests. [Permission synchronization source]({url}). See the [assignment and enforcement guide](architecture/security.html#assign-and-verify-permissions).\n'
    data = json.loads((CONTENT / 'permissions.json').read_text())['modules'][id_]
    url = f"{module['repository']}/blob/{module['commit']}/{data['path']}"
    text = '\n## Permissions and authorization\n\n'
    text += f"This catalogue contains **{len(data['permissions'])} permissions** declared by the [module manifest]({url}) at the revision above. Custom-role references use `module:resource:action`; the manifest and API contract use the local `resource:action` form. The action names are distinct grants: do not assume `manage` automatically includes `read` or another action.\n\n"
    text += NOTES.get(id_, 'Module permissions gate actions within the authenticated tenant. The endpoint still enforces its resource and workflow checks; a UI ability describes presentation and does not replace server authorization.') + '\n\n'
    text += '[How to assign and verify permissions](architecture/security.html#assign-and-verify-permissions). Module roles and built-in grant mappings are defined in the linked manifest; review those mappings before assigning a broad role.\n\n'
    text += '| Qualified permission | What it allows |\n| --- | --- |\n'
    for row in data['permissions']:
        text += f"| `{id_}:{row['ref']}` | {cell(row['description'])} |\n"
    for row in data['permissions']:
        text += f"\n### {id_}:{row['ref']}\n\n{row['description']}.\n\n"
        abilities = row['abilities']
        if abilities:
            text += '**UI actions**: ' + '; '.join(', '.join(f'`{a}`' for a in ability['actions']) + ' on ' + ', '.join(f'`{s}`' for s in ability['subjects']) for ability in abilities) + '. These are the manifest’s CASL presentation rules.\n\n'
        if row['navigation']:
            text += '**Navigation gated by this permission**: ' + ', '.join(n['title'] for n in row['navigation']) + '.\n\n'
        operations = [op for op in module['api_operations'] if op.get('permission') in (row['ref'], id_ + ':' + row['ref'])]
        if operations:
            text += '**API operations declaring this permission**:\n\n| Method | Contract path | Action |\n| --- | --- | --- |\n'
            for op in operations:
                text += f"| `{op['method']}` | `{op['path']}` | {cell(op['summary'])} |\n"
        else:
            text += 'The imported OpenAPI operations do not declare a matching `x-freya-permission` for this grant. Use the manifest and server authorization implementation to identify its enforcement; this absence does not indicate public access.\n'
        text += f"\n**Scope and additional checks**: {NOTES.get(id_, 'This grant does not remove tenant boundaries, resource checks or workflow restrictions. The endpoint must authorize the requested operation even when the UI exposes it.')}\n"
    return text
