import os
import re
from pathlib import Path
import json
from typing import Any
from dotenv import load_dotenv

# Загружаем .env для разработки
load_dotenv()

# Файл секретов для этого приложения
_SECRETS_FILE = "backend_secrets"
# Кэш для прочитанных секретов
_secrets_cache = {}


def parse_secrets_file(file_path: str) -> dict:
    """ Парсит файл секретов в формате KEY=VALUE с поддержкой многострочных
    значений. Использует регулярные выражения для надежного определения
    ключей.
    При копировании секретов внутрь контейнера docker может разорвать
    строки на несколько частей. """

    secrets = {}
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Паттерн для определения ключа: только заглавные буквы, цифры и _
        key_pattern = re.compile(r'^[A-Z_][A-Z0-9_]*=')

        lines = content.split('\n')
        current_key = None
        current_parts = []

        for line in lines:
            line = line.rstrip('\r')

            if not line.strip():
                continue

            # Если строка соответствует формату ключа=значение
            if key_pattern.match(line):
                # Сохраняем предыдущую пару
                if current_key is not None:
                    secrets[current_key] = ''.join(current_parts).strip()

                # Начинаем новую пару
                key, value = line.split('=', 1)
                current_key = key.strip()
                current_parts = [value]
            elif current_key is not None:
                # Продолжение текущего значения
                current_parts.append(line.strip())

        # Сохраняем последнюю пару
        if current_key is not None:
            secrets[current_key] = ''.join(current_parts).strip()

    except Exception as e:
        print(f"Warning: Could not parse secrets file {file_path}: {e}")

    return secrets


def get_secret(secret_name: str, default: Any = None) -> Any:
    """ Функция для чтения секретов:
    - В production: читает из Docker secrets (/run/secrets/)
    - В development: читает из переменных окружения (.env файл)
    """

    # Проверяем кэш
    if secret_name in _secrets_cache:
        return _secrets_cache[secret_name]

    # Проверяем Docker secrets (production)
    secret_file = Path(f"/run/secrets/{_SECRETS_FILE}")
    if secret_file.exists():
        secrets = parse_secrets_file(secret_file)
        if secret_name in secrets:
            _secrets_cache[secret_name] = secrets[secret_name]
            return secrets[secret_name]

    # Если Docker secrets не найдены, используем переменные окружения (development)
    value = os.getenv(secret_name, default)
    _secrets_cache[secret_name] = value
    return value


def get_json_secret(secret_name: str, default: Any = None) -> Any:
    """ Читает секрет в формате JSON и парсит его
    Returns: Parsed JSON object or default """

    secret_value = get_secret(secret_name)
    if secret_value is None or secret_value == '':
        return default

    try:
        return json.loads(secret_value)
    except json.JSONDecodeError as e:
        msg = f"Warning: Could not parse JSON secret {secret_name}: {e}"
        print(msg)
        return default
