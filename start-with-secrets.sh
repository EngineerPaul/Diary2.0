#!/bin/bash

echo "Starting containers with all secrets..."

# Остановка существующих контейнеров
# 2>/dev/null - перенаправляет ошибки в никуда (скрывает "no containers found")
# || true - если docker-compose down вернул ошибку, true вернет успех (код 0)
# Результат: скрипт продолжает работу независимо от того, были ли запущены контейнеры
echo "Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Генерация всех секретов
echo "Generating Redis secrets..."
cd _redis && ./generate-secrets.sh && cd ..

echo "Generating authserver database secrets..."
cd _auth_db && ./generate-secrets.sh && cd ..

echo "Generating backend database secrets..."
cd _back_db && ./generate-secrets.sh && cd ..

echo "Generating authserver secrets..."
cd authserver && ./generate-secrets.sh && cd ..

echo "Generating backend secrets..."
cd backend && ./generate-secrets.sh && cd ..

echo "Generating frontend secrets..."
cd frontend && ./generate-secrets.sh && cd ..

echo "Generating tg-bot secrets..."
cd tgbot && ./generate-secrets.sh && cd ..

echo "Generating tg-server secrets..."
cd tgserver && ./generate-secrets.sh && cd ..

# Альтернативный вариант для разработки (генерировать только если файла нет):
# if [ ! -f "./_redis/redis-secrets.txt" ]; then
#     echo "Generating Redis secrets..."
#     cd _redis && ./generate-secrets.sh && cd ..
# fi

# Запуск контейнеров
echo "Starting Docker Compose..."
docker-compose up -d

echo "All containers started successfully!"
echo "All secrets are stored in respective .env files"
