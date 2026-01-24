#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# python3 manage.py flush --no-input
python3 manage.py makemigrations
python3 manage.py migrate

# ========================================
# Настройка прав доступа для media файлов
# ========================================
echo "Setting up media directory permissions..."
mkdir -p /home/backendapp/back/root/mediafiles/uploads
# Даем права на запись для пользователя контейнера (UID 1000)
chown -R 1000:1000 /home/backendapp/back/root/mediafiles
chmod -R 755 /home/backendapp/back/root/mediafiles
echo "Media permissions configured successfully"

exec "$@"
