#!/bin/bash

# Генерация секретов для базы данных authserver
if [ -f ".env" ]; then
    POSTGRES_DB=$(grep "^POSTGRES_DB=" .env | cut -d= -f2-)
    POSTGRES_USER=$(grep "^POSTGRES_USER=" .env | cut -d= -f2-)
    POSTGRES_PASSWORD=$(grep "^POSTGRES_PASSWORD=" .env | cut -d= -f2-)
else
    echo "ERROR: .env file not found in _auth_db"
    exit 1
fi

# Создание файла секретов для Docker
cat > authdb-secrets.txt << EOF
POSTGRES_DB=${POSTGRES_DB}
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
EOF

echo "Authserver database secrets generated"
