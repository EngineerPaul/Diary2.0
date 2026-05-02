#!/bin/bash

# Резервное копирование SSL сертификатов
# Создает бэкап перед обновлением или изменениями

set -e  # Выход при любой ошибке

echo "=== SSL Factory: Резервное копирование ==="

# Проверяем существование сертификатов
if [ ! -f "../nginx/ssl/cert.pem" ]; then
    echo "❌ Сертификаты не найдены, нечего бэкапить"
    exit 1
fi

# Создаем директорию для бэкапов
BACKUP_DIR="../nginx/ssl/backup/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Копируем сертификаты (не трогаем подкаталог backup/ — cp без -r не копирует каталоги)
cp ../nginx/ssl/cert.pem ../nginx/ssl/key.pem "$BACKUP_DIR/"

echo "✅ Сертификаты забэкаплены в: $BACKUP_DIR"

# Удаляем старые бэкапы (оставляем последние 5)
echo "🧹 Удаляем старые бэкапы..."
ls -t ../nginx/ssl/backup/ 2>/dev/null | tail -n +6 | xargs -r rm -rf

# Показываем количество бэкапов
BACKUP_COUNT=$(ls ../nginx/ssl/backup/ 2>/dev/null | wc -l)
echo "📦 Всего бэкапов: $BACKUP_COUNT"

echo "✅ Резервное копирование завершено"
