#!/bin/bash

# Генерация секретов для базы данных authserver
# Генерируем безопасный пароль для PostgreSQL
DB_PASSWORD=$(openssl rand -base64 32 | tr -d '\n\r' | head -c 24)

# Читаем константы из своего .env файла
if [ -f ".env" ]; then
    POSTGRES_DB=$(grep "^POSTGRES_DB=" .env | cut -d= -f2-)
    POSTGRES_USER=$(grep "^POSTGRES_USER=" .env | cut -d= -f2-)
else
    echo "ERROR: .env file not found in _auth_db"
    exit 1
fi

# Создание файла секретов для Docker
cat > authdb-secrets.txt << EOF
POSTGRES_DB=${POSTGRES_DB}
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_PASSWORD=${DB_PASSWORD}
EOF

echo "Authserver database secrets generated"
