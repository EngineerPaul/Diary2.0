#!/usr/bin/env bash
set -euo pipefail

# Default matches your server path; can be overridden by env.
DEPLOY_PATH="${DEPLOY_PATH:-/var/www/Diary-project/Diary2.0}"
DEPLOY_BRANCH="${DEPLOY_BRANCH:-master}"

cd "$DEPLOY_PATH"

if [[ ! -f docker-compose.yaml ]]; then
  echo "docker-compose.yaml not found in DEPLOY_PATH=$DEPLOY_PATH" >&2
  exit 2
fi

echo "==> Updating repo in $DEPLOY_PATH (branch: $DEPLOY_BRANCH)"
git fetch --prune origin
git reset --hard "origin/${DEPLOY_BRANCH}"

echo "==> Checking required secret files"
required_files=(
  "_redis/redis-secrets.txt"
  "frontend/frontend-secrets.txt"
  "tgbot/bot-secrets.txt"
  "tgserver/tgserver-secrets.txt"
  "authserver/authserver-secrets.txt"
  "backend/backend-secrets.txt"
  "_auth_db/authdb-secrets.txt"
  "_back_db/backdb-secrets.txt"
)

missing=0
for f in "${required_files[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "Missing: $DEPLOY_PATH/$f" >&2
    missing=1
  fi
done

if [[ "$missing" -ne 0 ]]; then
  echo "One or more required secret files are missing. Aborting deploy." >&2
  exit 3
fi

echo "==> Deploying with docker compose"
docker compose up -d --build

echo "==> Showing status"
docker compose ps
