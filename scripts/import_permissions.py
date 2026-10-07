#!/usr/bin/env python3
"""Snapshot public permission manifests at the inventory's recorded revisions."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def git(directory, *args):
    return subprocess.check_output(['git', '-C', str(directory), *args], text=True)


def extract(text):
    rows = []
    for resource, action, description in re.findall(r'\{Resource:\s*"([^"]+)",\s*Action:\s*"([^"]+)",\s*Description:\s*("(?:[^"\\]|\\.)*")\s*\}', text):
        rows.append({'ref': resource + ':' + action, 'description': json.loads(description)})
    if not rows:
        raise ValueError('Manifest has no recognized permission definitions')
    for row in rows:
        row['abilities'] = []
        row['navigation'] = []
        for actions, subjects, requires in re.findall(r'\{Action:\s*\[\]string\{([^}]+)\},\s*Subject:\s*\[\]string\{([^}]+)\},\s*Requires:\s*"([^"]+)"', text):
            if requires == row['ref']:
                row['abilities'].append({'actions': re.findall(r'"([^"]+)"', actions), 'subjects': re.findall(r'"([^"]+)"', subjects)})
        for title, path, requires in re.findall(r'\{Title:\s*"([^"]+)"[^\n]*?Path:\s*([^,]+)[^\n]*?Requires:\s*"([^"]+)"', text):
            if requires == row['ref']:
                row['navigation'].append({'title': title, 'path_expression': path.strip()})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    data = {'modules': {}}
    for module in json.loads((ROOT / 'content/modules.json').read_text())['modules']:
        directory = args.root / module['checkout']
        paths = git(directory, 'ls-tree', '-r', '--name-only', module['commit']).splitlines()
        candidates = [p for p in paths if p.startswith('pkg/') and p.endswith('manifest.go') and '/sdk/' not in p]
        if module['id'] in ('platform', 'portal'):
            continue
        if len(candidates) != 1:
            raise ValueError(f"Ambiguous permission manifest for {module['id']}: {candidates}")
        path = candidates[0]
        text = git(directory, 'show', module['commit'] + ':' + path)
        destination = ROOT / 'content/permissions' / module['id'] / 'manifest.go'
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text)
        data['modules'][module['id']] = {'path': path, 'snapshot': str(destination.relative_to(ROOT)), 'sha256': hashlib.sha256(text.encode()).hexdigest(), 'permissions': extract(text)}
    (ROOT / 'content/permissions.json').write_text(json.dumps(data, indent=2) + '\n')
    print(f"Imported {sum(len(m['permissions']) for m in data['modules'].values())} permissions from {len(data['modules'])} recorded module revisions")


if __name__ == '__main__':
    main()
