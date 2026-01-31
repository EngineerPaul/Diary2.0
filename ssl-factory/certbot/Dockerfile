# Certbot контейнер для SSL Factory
# Основан на официальном образе certbot с дополнительными настройками

FROM certbot/certbot:v5.2.2

# Устанавливаем дополнительные зависимости
# curl нужен для проверки доступности домена
RUN apk add --no-cache curl

# Создаем необходимые директории (2 шт)
# -p создает все промежуточные директории если их нет
# /etc/letsencrypt - хранит сертификаты
# /var/www/certbot - хранит файлы для проверки домена
RUN mkdir -p /etc/letsencrypt /var/www/certbot

# Копируем entrypoint скрипт и делаем его исполняемым
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
