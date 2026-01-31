#!/bin/bash

# Генерация секретов для Django authserver
# Генерируем только SECRET_KEY, остальное копируем из .env
# Читаем существующие значения из .env в той же последовательности
if [ -f ".env" ]; then
    # Читаем пароль из .env файла базы данных
    if [ -f "../_auth_db/.env" ]; then
        DB_PASSWORD=$(grep "^POSTGRES_PASSWORD=" ../_auth_db/.env | cut -d= -f2-)
    else
        echo "ERROR: Database .env file not found. Check ../_auth_db/.env"
        exit 1
    fi
    
    # Читаем переменные в той же последовательности что в .env
    SECRET_KEY=$(openssl rand -base64 64 | tr -d '\n\r' | dd bs=50 count=1 2>/dev/null)
    DEBUG=$(grep "^DEBUG=" .env | cut -d= -f2-)
    SSL=$(grep "^SSL=" .env | cut -d= -f2-)
    CORS_ALLOWED_ORIGINS=$(grep "^CORS_ALLOWED_ORIGINS=" .env | cut -d= -f2-)
    CORS_ALLOW_CREDENTIALS=$(grep "^CORS_ALLOW_CREDENTIALS=" .env | cut -d= -f2-)
    ACCESS_TOKEN_LIFETIME=$(grep "^ACCESS_TOKEN_LIFETIME=" .env | cut -d= -f2-)
    REFRESH_TOKEN_LIFETIME=$(grep "^REFRESH_TOKEN_LIFETIME=" .env | cut -d= -f2-)
    PROJECT_HOSTS=$(grep "^PROJECT_HOSTS=" .env | cut -d= -f2-)
    DJANGO_ALLOWED_HOSTS=$(grep "^DJANGO_ALLOWED_HOSTS=" .env | cut -d= -f2-)
    SQL_ENGINE=$(grep "^SQL_ENGINE=" .env | cut -d= -f2-)
    SQL_DATABASE=$(grep "^SQL_DATABASE=" .env | cut -d= -f2-)
    SQL_USER=$(grep "^SQL_USER=" .env | cut -d= -f2-)
    SQL_PASSWORD=$DB_PASSWORD
    SQL_HOST=$(grep "^SQL_HOST=" .env | cut -d= -f2-)
    SQL_PORT=$(grep "^SQL_PORT=" .env | cut -d= -f2-)
    DATABASE=$(grep "^DATABASE=" .env | cut -d= -f2-)
else
    echo "ERROR: .env file not found"
    exit 1
fi

# Создание файла секретов для Docker
cat > authserver-secrets.txt << EOF
SECRET_KEY=${SECRET_KEY}
DEBUG=${DEBUG}
SSL=${SSL}
CORS_ALLOWED_ORIGINS=${CORS_ALLOWED_ORIGINS}
CORS_ALLOW_CREDENTIALS=${CORS_ALLOW_CREDENTIALS}
ACCESS_TOKEN_LIFETIME=${ACCESS_TOKEN_LIFETIME}
REFRESH_TOKEN_LIFETIME=${REFRESH_TOKEN_LIFETIME}
PROJECT_HOSTS=${PROJECT_HOSTS}
DJANGO_ALLOWED_HOSTS=${DJANGO_ALLOWED_HOSTS}
SQL_ENGINE=${SQL_ENGINE}
SQL_DATABASE=${SQL_DATABASE}
SQL_USER=${SQL_USER}
SQL_PASSWORD=${SQL_PASSWORD}
SQL_HOST=${SQL_HOST}
SQL_PORT=${SQL_PORT}
DATABASE=${DATABASE}
EOF

echo "Authserver secrets generated"
