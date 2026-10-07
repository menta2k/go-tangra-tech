#!/bin/sh
set -eu
umask 077
export VAULT_TOKEN=$(sed -n 's/^[[:space:]]*"root_token":[[:space:]]*"\([^"]*\)".*/\1/p' /vault-bootstrap/init.json)
[ -n "$VAULT_TOKEN" ] || { echo "Cannot read Vault bootstrap token" >&2; exit 1; }
sh /vault-approle.sh
chmod 600 /vault-creds/role_id /vault-creds/secret_id
