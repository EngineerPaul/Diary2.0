#!/bin/bash

# Генерация секретов для Django frontend
# Генерируем только SECRET_KEY, остальное копируем из .env
SECRET_KEY=$(openssl rand -base64 50 | tr -d "=+/" | cut -c1-50)

# Читаем существующие значения из .env
if [ -f ".env" ]; then
    ACCESS_TOKEN_LIFETIME=$(grep "^ACCESS_TOKEN_LIFETIME=" .env | cut -d= -f2-)
    REFRESH_TOKEN_LIFETIME=$(grep "^REFRESH_TOKEN_LIFETIME=" .env | cut -d= -f2-)
    PROJECT_HOSTS=$(grep "^PROJECT_HOSTS=" .env | cut -d= -f2-)
    DEBUG=$(grep "^DEBUG=" .env | cut -d= -f2-)
    SINGLE_USER=$(grep "^SINGLE_USER=" .env | cut -d= -f2-)
    
    # Проверяем что все переменные найдены
    if [ -z "$ACCESS_TOKEN_LIFETIME" ] || [ -z "$REFRESH_TOKEN_LIFETIME" ] || [ -z "$PROJECT_HOSTS" ] || [ -z "$DEBUG" ] || [ -z "$SINGLE_USER" ]; then
        echo "ERROR: Required variables not found in .env file"
        echo "Missing: ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME, PROJECT_HOSTS, DEBUG, or SINGLE_USER"
        exit 1
    fi
else
    echo "ERROR: .env file not found"
    exit 1
fi

# Создание файла секретов для Docker
cat > frontend-secrets.txt << EOF
SECRET_KEY=${SECRET_KEY}
DEBUG=${DEBUG}
ACCESS_TOKEN_LIFETIME=${ACCESS_TOKEN_LIFETIME}
REFRESH_TOKEN_LIFETIME=${REFRESH_TOKEN_LIFETIME}
PROJECT_HOSTS=${PROJECT_HOSTS}
SINGLE_USER=${SINGLE_USER}
EOF

echo "Frontend secrets generated"
