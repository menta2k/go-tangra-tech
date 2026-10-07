#!/bin/sh
set -eu
umask 077
for directory in /keys/*; do
  [ -d "$directory" ] || continue
  if [ ! -s "$directory/kek" ]; then
    head -c 32 /dev/urandom | base64 > "$directory/kek.tmp"
    mv "$directory/kek.tmp" "$directory/kek"
  fi
  chmod 600 "$directory/kek"
done
echo "Private keys ready (existing keys preserved)."
