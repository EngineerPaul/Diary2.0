#!/bin/bash

# Обновление SSL сертификатов без остановки продакшена
# Работает через API Let's Encrypt, не требует HTTP верификации, потому что ключи уже получены ранее
# Время простоя основного приложения: отсутствует (hot-reload nginx)

set -e  # Выход при любой ошибке

echo "=== SSL Factory: Обновление сертификатов ==="

# Проверяем, что мы в правильной директории
if [ ! -f "ssl-compose.yaml" ]; then
    echo "❌ Ошибка: Запустите скрипт из директории ssl-factory"
    exit 1
fi

# Проверяем наличие .env файла
if [ ! -f "./certbot/.env" ]; then
    echo "❌ Файл ./certbot/.env не найден!"
    exit 1
fi

# Загружаем переменные из .env
source ./certbot/.env

if [ -z "$DOMAIN" ]; then
    echo "❌ Ошибка: DOMAIN не указан в certbot/.env"
    exit 1
fi

echo "🌐 Домен: $DOMAIN"
echo ""

# Проверяем существование сертификатов
if [ ! -f "../nginx/ssl/cert.pem" ]; then
    echo "❌ Сертификаты не найдены. Сначала запустите первоначальную настройку:"
    echo "   ./scripts/setup-ssl.sh"
    exit 1
fi

# Проверяем срок действия сертификатов
echo "🔍 Проверяем срок действия сертификатов..."
EXPIRY_DATE=$(openssl x509 -in ../nginx/ssl/cert.pem -noout -enddate | cut -d= -f2)
EXPIRY_EPOCH=$(date -d "$EXPIRY_DATE" +%s)
NOW_EPOCH=$(date +%s)
DAYS_LEFT=$(( ($EXPIRY_EPOCH - $NOW_EPOCH) / 86400 ))

echo "📅 Срок действия: $EXPIRY_DATE"
echo "⏰ Осталось дней: $DAYS_LEFT"
echo ""

# Если сертификат действителен более 14 дней, обновление не требуется
if [ $DAYS_LEFT -gt 14 ]; then
    echo "✅ Обновление не требуется (сертификат действителен еще $DAYS_LEFT дней)"
    exit 0
fi

echo "🔄 Сертификат истекает через $DAYS_LEFT дней. Запускаем обновление..."
echo ""

# Создаем бэкап текущих сертификатов
echo "💾 Создаем резервную копию..."
BACKUP_DIR="../nginx/ssl/backup/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
# Только PEM-файлы: glob * захватывает подкаталог backup/, cp без -r падает
cp ../nginx/ssl/cert.pem ../nginx/ssl/key.pem "$BACKUP_DIR/"
echo "✅ Бэкап создан: $BACKUP_DIR"
echo ""

# Удаляем старые бэкапы (оставляем последние 5)
ls -t ../nginx/ssl/backup/ 2>/dev/null | tail -n +6 | xargs -r rm -rf

# Запускаем SSL Factory для обновления
echo "� Загружаем Docker образы..."
docker-compose -f ssl-compose.yaml pull

echo "� Запускаем контейнеры..."
docker-compose -f ssl-compose.yaml up -d

# Отслеживаем запуск сервисов
echo "⏳ Ожидаем запуска сервисов..."
MAX_START_WAIT=30  # 30 секунд на запуск контейнеров
START_TIME=0

while [ $START_TIME -lt $MAX_START_WAIT ]; do
    if docker-compose -f ssl-compose.yaml ps | grep -q "Up"; then
        echo "✅ Сервисы запущены за ${START_TIME} секунд"
        break
    fi
    
    if [ $START_TIME -eq 0 ]; then
        echo -n "🚀 Запускаем сервисы"
    else
        echo -n ". "
    fi
    
    sleep 2
    START_TIME=$((START_TIME + 2))
done

if [ $START_TIME -ge $MAX_START_WAIT ]; then
    echo ""
    echo "❌ Ошибка: Сервисы не запустились за ${MAX_START_WAIT} секунд"
    echo "Проверьте логи: docker-compose -f ssl-compose.yaml logs"
    echo "Возможные причины:"
    echo "- Проблемы с конфигурацией"
    echo "- Недостаточно ресурсов системы"
    echo "- Конфликты портов"
    echo "После устранения проблемы запустите скрипт заново"
    docker-compose -f ssl-compose.yaml down
    exit 1
fi

# Обновляем сертификаты
echo "🔑 Обновляем сертификаты..."
# Контейнеры уже запущены, ждем выполнения entrypoint certbot
echo "⏳ Ожидаем выполнения entrypoint certbot..."
MAX_CERTBOT_WAIT=120  # 2 минуты на выполнение certbot
CERTBOT_TIME=0

while [ $CERTBOT_TIME -lt $MAX_CERTBOT_WAIT ]; do
    # Проверяем, завершился ли certbot контейнер (certbot контейнер после выполнения закрывается)
    if ! docker-compose -f ssl-compose.yaml ps | grep -q "certbot.*Up"; then
        echo "✅ Certbot завершил работу за ${CERTBOT_TIME} секунд"
        break
    fi
    
    if [ $CERTBOT_TIME -eq 0 ]; then
        echo -n "🔑 Выполняется certbot"
    elif [ $CERTBOT_TIME -eq 30 ]; then
        echo ""
        echo "⏳ Обновление сертификатов может занять время..."
        echo -n "🔑 Продолжаем ожидание"
    else
        echo -n ". "
    fi
    
    sleep 3
    CERTBOT_TIME=$((CERTBOT_TIME + 3))
done

if [ $CERTBOT_TIME -ge $MAX_CERTBOT_WAIT ]; then
    echo ""
    echo "❌ Ошибка: Certbot не завершил работу за ${MAX_CERTBOT_WAIT} секунд"
    echo "Проверьте логи: docker-compose -f ssl-compose.yaml logs certbot"
    echo "Возможные причины:"
    echo "- Проблемы с доступностью домена"
    echo "- Проблемы с Let's Encrypt"
    echo "После устранения проблемы запустите скрипт заново"
    docker-compose -f ssl-compose.yaml down
    exit 1
fi

# Останавливаем SSL Factory
docker-compose -f ssl-compose.yaml down

# Проверяем, обновились ли сертификаты
echo "🔍 Проверяем результат обновления..."
if [ "../nginx/ssl/cert.pem" -nt "$BACKUP_DIR/cert.pem" ]; then
    echo "✅ Сертификаты успешно обновлены!"
    
    # Показываем информацию о новых сертификатах
    echo "📄 Информация о новых сертификатах:"
    openssl x509 -in ../nginx/ssl/cert.pem -noout -dates
    echo ""
    
    # Выполняем hot-reload основного nginx без остановки
    echo "🔄 Выполняем hot-reload основного nginx..."
    cd ..
    
    if docker-compose exec nginx nginx -s reload; then
        echo "✅ Nginx успешно перезагружен через hot-reload"
        echo "🌐 HTTPS продолжает работать без простоя"
    else
        echo "⚠️ Не удалось выполнить hot-reload, пробуем перезапуск..."
        docker-compose restart nginx
    fi
    
    cd ssl-factory
    
    # Логируем успешное обновление
    echo "$(date '+%Y-%m-%d %H:%M:%S') - SSL сертификаты для $DOMAIN успешно обновлены" >> ./logs/renewal.log
    
    echo ""
    echo "🎉 Обновление SSL сертификатов завершено успешно!"
    echo "📋 Сайт продолжает работать по HTTPS://$DOMAIN"
    
else
    echo "ℹ️ Обновление не потребовалось (сертификаты не изменились)"
    echo "📋 Сертификаты действительны до: $EXPIRY_DATE"
fi

echo ""
echo "✅ Процесс обновления завершен"
