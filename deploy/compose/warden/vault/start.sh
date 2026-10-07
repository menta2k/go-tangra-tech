#!/bin/sh
set -eu
# Persistent single-node development Vault. Recovery material stays private.
vault server -config=/etc/vault/config.hcl &
server_pid=$!
trap 'kill "$server_pid"; wait "$server_pid"' TERM INT
attempt=0
while ! vault status -format=json >/tmp/vault-status.json 2>/dev/null; do
  if [ -s /tmp/vault-status.json ]; then break; fi
  attempt=$((attempt + 1))
  [ "$attempt" -lt 60 ] || exit 1
  sleep 1
done
if [ ! -s /vault-bootstrap/init.json ]; then
  umask 077
  vault operator init -key-shares=1 -key-threshold=1 -format=json > /vault-bootstrap/init.json.tmp
  mv /vault-bootstrap/init.json.tmp /vault-bootstrap/init.json
fi
# Parse the two JSON string fields without installing an extra CLI at startup.
unseal_key=$(sed -n '/"unseal_keys_b64"/,$ { /"[A-Za-z0-9+\/=]*"/ { s/^[[:space:]]*"\([A-Za-z0-9+\/=]*\)".*/\1/p; } }' /vault-bootstrap/init.json | head -n 1)
[ -n "$unseal_key" ] || { echo "Cannot read Vault unseal key" >&2; exit 1; }
vault operator unseal "$unseal_key" >/dev/null
wait "$server_pid"
