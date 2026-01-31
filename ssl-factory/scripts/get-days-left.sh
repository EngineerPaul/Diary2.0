#!/bin/bash

# Проверка срока действия SSL сертификатов
# Возвращает количество дней до истечения сертификата

# Путь к сертификату
CERT_FILE="../nginx/ssl/cert.pem"

# Проверяем существование сертификата
if [ ! -f "$CERT_FILE" ]; then
    echo "0"
    exit 1
fi

# Получаем дату истечения сертификата
EXPIRY_DATE=$(openssl x509 -in "$CERT_FILE" -noout -enddate | cut -d= -f2)

# Конвертируем в Unix timestamp
EXPIRY_EPOCH=$(date -d "$EXPIRY_DATE" +%s)
NOW_EPOCH=$(date +%s)

# Вычисляем количество дней
DAYS_LEFT=$(( ($EXPIRY_EPOCH - $NOW_EPOCH) / 86400 ))

# Возвращаем результат
echo $DAYS_LEFT
