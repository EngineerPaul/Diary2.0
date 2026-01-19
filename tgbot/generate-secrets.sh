#!/bin/bash

# Копирование констант для Telegram Bot в секрет
# Проверяем наличие .env файла
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found"
    exit 1
fi

# Проверяем что все необходимые переменные есть в .env
TOKEN=$(grep "^TOKEN=" .env | cut -d= -f2-)
ID=$(grep "^ID=" .env | cut -d= -f2-)
SITELINK=$(grep "^SITELINK=" .env | cut -d= -f2-)
TGSERVERHOST=$(grep "^TGSERVERHOST=" .env | cut -d= -f2-)
PROJECT_HOSTS=$(grep "^PROJECT_HOSTS=" .env | cut -d= -f2-)
DEBUG=$(grep "^DEBUG=" .env | cut -d= -f2-)

if [ -z "$TOKEN" ] || [ -z "$ID" ] || [ -z "$SITELINK" ] || [ -z "$TGSERVERHOST" ] || [ -z "$PROJECT_HOSTS" ] || [ -z "$DEBUG" ]; then
    echo "ERROR: Required variables not found in .env file"
    echo "Missing: TOKEN, ID, SITELINK, TGSERVERHOST, PROJECT_HOSTS, or DEBUG"
    exit 1
fi

# Копируем .env в bot-secrets.txt для Docker
cp .env bot-secrets.txt

echo "Bot secrets created from existing .env"
