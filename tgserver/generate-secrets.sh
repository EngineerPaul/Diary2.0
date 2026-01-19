#!/bin/bash

# Генерация секретов для Telegram Server
# Проверяем наличие .env файла
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found"
    exit 1
fi

# Проверяем что все необходимые переменные есть в .env
PROJECT_HOSTS=$(grep "^PROJECT_HOSTS=" .env | head -n1 | cut -d= -f2-)
TGTOKEN=$(grep "^TGTOKEN=" .env | head -n1 | cut -d= -f2-)
MY_TG_ID=$(grep "^MY_TG_ID=" .env | cut -d= -f2-)
REDIS_WORKS=$(grep "^REDIS_WORKS=" .env | cut -d= -f2-)
REDIS_HOST=$(grep "^REDIS_HOST=" .env | cut -d= -f2-)
REDIS_PORT=$(grep "^REDIS_PORT=" .env | cut -d= -f2-)

if [ -z "$PROJECT_HOSTS" ] || [ -z "$TGTOKEN" ] || [ -z "$MY_TG_ID" ] || [ -z "$REDIS_WORKS" ] || [ -z "$REDIS_HOST" ] || [ -z "$REDIS_PORT" ]; then
    echo "ERROR: Required variables not found in .env file"
    echo "Missing: PROJECT_HOSTS, TGTOKEN, MY_TG_ID, REDIS_WORKS, REDIS_HOST, REDIS_PORT"
    exit 1
fi

# Читаем Redis пароли из общего файла секретов
if [ -f "../_redis/redis-secrets.txt" ]; then
    REDIS_USER_FROM_FILE=$(grep "^REDIS_USER=" ../_redis/redis-secrets.txt | cut -d= -f2-)
    REDIS_USER_PASSWORD_FROM_FILE=$(grep "^REDIS_USER_PASSWORD=" ../_redis/redis-secrets.txt | cut -d= -f2-)
else
    echo "ERROR: Redis secrets file not found"
    exit 1
fi

if [ -z "$REDIS_USER_FROM_FILE" ] || [ -z "$REDIS_USER_PASSWORD_FROM_FILE" ]; then
    echo "ERROR: Redis user or password not found in redis-secrets.txt"
    exit 1
fi

# Создаем файл секретов, заменяя Redis учетные данные на те что из redis-secrets.txt
sed "s/^REDIS_USER=.*/REDIS_USER=${REDIS_USER_FROM_FILE}/" .env | \
sed "s/^REDIS_USER_PASSWORD=.*/REDIS_USER_PASSWORD=${REDIS_USER_PASSWORD_FROM_FILE}/" > tgserver-secrets.txt

echo "Server secrets generated"
