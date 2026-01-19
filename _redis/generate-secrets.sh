#!/bin/bash

# Генерация случайных паролей для Redis
# Генерируем только пароли, имя пользователя копируем из .env
REDIS_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
REDIS_USER_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)

# Читаем существующее имя пользователя из .env
if [ -f ".env" ]; then
    REDIS_USER=$(grep "^REDIS_USER=" .env | cut -d= -f2-)
    
    # Проверяем что REDIS_USER найден и не пустой
    if [ -z "$REDIS_USER" ]; then
        echo "ERROR: REDIS_USER not found or empty in .env file"
        exit 1
    fi
else
    echo "ERROR: .env file not found"
    exit 1
fi

# Создание файла секретов (по шаблону ниже)
cat > redis-secrets.txt << EOF
REDIS_PASSWORD=${REDIS_PASSWORD}
REDIS_USER=${REDIS_USER}
REDIS_USER_PASSWORD=${REDIS_USER_PASSWORD}
EOF

echo "Redis secrets generated"
