#!/bin/bash

echo "Starting containers with all secrets..."

# Остановка существующих контейнеров
# 2>/dev/null - перенаправляет ошибки в никуда (скрывает "no containers found")
# || true - если docker-compose down вернул ошибку, true вернет успех (код 0)
# Результат: скрипт продолжает работу независимо от того, были ли запущены контейнеры
echo "Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Генерация всех секретов
# разбито на отдельные строчки, потому что при ошибке в одном скрипте cd .. не сработает и весь дальнейший скрипт сломается
echo "Generating Redis secrets..."
cd _redis && ./generate-secrets.sh
cd ..

echo "Generating authserver database secrets..."
cd _auth_db && ./generate-secrets.sh
cd ..

echo "Generating backend database secrets..."
cd _back_db && ./generate-secrets.sh
cd ..

echo "Generating authserver secrets..."
cd authserver && ./generate-secrets.sh
cd ..

echo "Generating backend secrets..."
cd backend && ./generate-secrets.sh
cd ..

echo "Generating frontend secrets..."
cd frontend && ./generate-secrets.sh
cd ..

echo "Generating tg-bot secrets..."
cd tgbot && ./generate-secrets.sh
cd ..

echo "Generating tg-server secrets..."
cd tgserver && ./generate-secrets.sh
cd ..

# Запуск контейнеров
echo "Starting Docker Compose..."
docker-compose up -d
 
# Ожидание запуска всех контейнеров
echo "Waiting for all containers to start..."
MAX_WAIT=60
WAIT_TIME=0
while [ $WAIT_TIME -lt $MAX_WAIT ]; do
    if docker-compose ps | grep -q "Up"; then
        echo "✅ All containers are running"
        break
    fi
    
    if [ $WAIT_TIME -eq 0 ]; then
        echo -n "⏳ Waiting for containers"
    else
        echo -n ". "
    fi
    
    sleep 2
    WAIT_TIME=$((WAIT_TIME + 2))
done
 
if [ $WAIT_TIME -ge $MAX_WAIT ]; then
    echo ""
    echo "❌ Error: Containers did not start within ${MAX_WAIT} seconds"
    exit 1
fi
 
# Настройка прав mediafiles
# Права необходимо настроить, чтобы контейнер мог записывать в папку mediafiles
# это необходимо сделать не только для целевой папки, но и для родительской
# передача папки в пользование пользователю контейнера - нормальная практика при работе с томами
# сделать это в entrypoint нельзя (говорит, что недостаточно прав для этого)
echo "Setting up mediafiles permissions..."
BACK_UID=1001
BACK_GID=1001
mkdir -p ./_media/data
sudo chown $BACK_UID:$BACK_GID ./_media
sudo chown -R $BACK_UID:$BACK_GID ./_media/data
sudo chmod -R 755 ./_media/data
echo "✅ Mediafiles permissions configured successfully"
