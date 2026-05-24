# Diary 2.0

Веб-дневник с иерархией папок, заметками, напоминаниями и интеграцией с Telegram. Проект развёрнут как набор микросервисов в Docker: отдельные сервисы аутентификации, бизнес-логики, UI, Telegram-бота и планировщика уведомлений.

---

## Возможности

- **Записи (records)** — папки, карточки записей, текстовые заметки и изображения внутри записи
- **Напоминания (notices)** — отдельное дерево папок, периодические напоминания (день / неделя / месяц / год), расчёт следующей даты срабатывания
- **Файловая система в UI** — drag-and-drop, смена порядка, перенос между папками
- **Аутентификация** — регистрация и вход, JWT в HttpOnly-cookies, refresh с ротацией и blacklist
- **Telegram** — привязка аккаунта к боту, создание напоминаний из чата, доставка по расписанию (Celery + Redis)
- **Часовые пояса** — напоминания хранятся в UTC, отображение и ввод — в timezone пользователя
- **Production-ready инфраструктура** — Nginx, HTTPS, Docker secrets, Gunicorn, PostgreSQL

---

## Архитектура

Ниже две схемы одного и того же: **Mermaid** (графика) и **ASCII** (текст).

**Mermaid** — разметка для диаграмм в Markdown. На [GitHub](https://github.com) и в предпросмотре Cursor/VS Code блок ниже отображается как рисунок. Если видите только код — откройте README на GitHub или включите Markdown Preview.

### Схема (Mermaid)

```mermaid
flowchart TB
    Browser[Браузер]
    TG[Telegram]

    Nginx[Nginx :80 / :443]

    Front[frontend]
    Auth[authserver]
    Back[backend]

    Bot[tgbot]
    TgAPI[tgserver / botapi]
    Celery[Celery worker + beat]

    AuthDB[(auth_db)]
    BackDB[(back_db)]
    Redis[(redis)]

    Browser --> Nginx
    Nginx --> Front
    Nginx --> Auth
    Nginx --> Back

    Front -. JWT cookies .-> Auth
    Front --> Back
    Back --> Auth

    TG --> Bot
    Bot --> TgAPI
    TgAPI --> Back
    TgAPI --> Auth
    TgAPI --> Celery
    Celery --> Redis
    Celery --> Bot

    Auth --> AuthDB
    Back --> BackDB
```

### Схема (ASCII)

Та же логика в текстовом виде — читается в любом редакторе без предпросмотра:

```
Браузер
   │
   ▼
 Nginx  :80 / :443
   ├── /              →  frontend      (HTML, статика)
   ├── /auth/         →  authserver    (регистрация, JWT)
   ├── /api/          →  backend       (записи, напоминания, медиа)
   ├── /static/       →  том static_volume
   └── /media/        →  _media/data

frontend  ──cookies JWT──►  authserver
frontend  ──REST──────────►  backend  ──verify/refresh──►  authserver

Telegram
   │
   ▼
 tgbot  ──►  tgserver (botapi)  ──►  backend, authserver
                  │
                  ├──  celery_worker / celery_beat
                  └──  redis

authserver  ──►  auth_db   (PostgreSQL)
backend     ──►  back_db   (PostgreSQL)
```

Через Nginx в браузере всё доступно с одного origin: `/` — UI, `/auth/` — auth API, `/api/` — backend API. Сервисы `bot` и `botapi` работают во внутренней сети Docker и напрямую не проксируются Nginx.

Внутренние вызовы между `back`, `authserver` и `botapi` защищены общим секретом `INTERNAL_SERVICE_TOKEN` (заголовок `X-Service-Token`). Публичный JWT для браузера с этим не связан.

### Сервисы

- **nginx**
  - Reverse proxy, раздача static/media, SSL. Порт: **80**, **443**.

- **front** (контейнер `diary_frontend`)
  - HTML-страницы и UI. Стек: Django 5, Gunicorn. Порт: **8000**.

- **authserver** (контейнер `diary_authserver`)
  - Регистрация, вход, JWT, привязка Telegram. Стек: Django 5, DRF, SimpleJWT. Порт: **8001**.

- **back** (контейнер `diary_backend`)
  - REST API записей, напоминаний и загрузки файлов. Стек: Django 5, DRF, Pillow. Порт: **8002**.

- **botapi** (сервис `botapi` в compose)
  - HTTP API для бота и Celery. Стек: FastAPI, Uvicorn. Порт: **8003**.

- **bot** (контейнер `diary_bot`)
  - Telegram-бот, общается с пользователем и tgserver. Стек: pyTelegramBotAPI. Порт наружу не пробрасывается.

- **celery_worker** / **celery_beat**
  - Планировщик и фоновая отправка напоминаний. Стек: Celery 5. Только внутренняя сеть Docker.

- **auth_db** / **back_db**
  - Две отдельные базы PostgreSQL 16 (пользователи и данные дневника). Только внутренняя сеть Docker.

- **redis**
  - Очередь и хранилище для tgserver/Celery. Redis 8. Только внутренняя сеть Docker.

---

## Стек технологий

- **Backend**: Python 3.12, Django 5.2, Django REST Framework
- **Auth**: djangorestframework-simplejwt, token blacklist
- **Telegram API**: FastAPI, aiohttp, Celery, Redis
- **Frontend**: Django templates, vanilla JavaScript
- **Инфраструктура**: Docker Compose, Docker secrets, Gunicorn, Nginx
- **БД**: PostgreSQL 16 (prod), SQLite (локальная разработка при `DEBUG=true`)

---

## Структура репозитория

```
.
├── frontend/          # UI (Django SSR)
├── authserver/        # Аутентификация и профиль пользователя
├── backend/           # Основной REST API и медиафайлы
├── tgserver/          # FastAPI + Celery для напоминаний
├── tgbot/             # Telegram-бот
├── nginx/             # Конфигурация reverse proxy
├── ssl-factory/       # Получение SSL-сертификатов Let's Encrypt (отдельно)
├── _auth_db/          # Секреты и данные PostgreSQL (auth)
├── _back_db/          # Секреты и данные PostgreSQL (backend)
├── _redis/            # Секреты и данные Redis
├── _media/            # Загруженные пользовательские файлы
├── docker-compose.yaml
└── start-with-secrets.sh   # Генерация секретов и запуск стека
```

---

## Требования

- [Docker](https://docs.docker.com/get-docker/) и Docker Compose v2
- Bash (для скриптов генерации секретов): **Git Bash** или **WSL** на Windows, обычный shell на Linux/macOS
- Для production с HTTPS: домен, указывающий на сервер, и настроенный [`ssl-factory`](ssl-factory/README.md)

> **Python 3.12** используется в Docker-образах. Файл `python-version.txt` (3.11) — ориентир для локальной разработки без Docker; при расхождении приоритет у версии в `dockerfile.prod`.

---

## Быстрый старт (Docker)

### 1. Подготовить `.env` в каждом сервисе

Файлы `.env` **не коммитятся** (см. `.gitignore`). Перед первым запуском создайте их по шаблонам ниже. Скрипты `generate-secrets.sh` читают `.env` и формируют `*-secrets.txt` для Docker.

Минимальный набор каталогов с `.env`:

| Каталог | Файл секретов (генерируется) |
|---------|------------------------------|
| `_redis/` | `_redis/redis-secrets.txt` |
| `_auth_db/` | `_auth_db/authdb-secrets.txt` |
| `_back_db/` | `_back_db/backdb-secrets.txt` |
| `authserver/` | `authserver/authserver-secrets.txt` |
| `backend/` | `backend/backend-secrets.txt` |
| `frontend/` | `frontend/frontend-secrets.txt` |
| `tgbot/` | `tgbot/bot-secrets.txt` |
| `tgserver/` | `tgserver/tgserver-secrets.txt` |

**Общий секрет для микросервисов** — в `.env` трёх сервисов должен быть **один и тот же** `INTERNAL_SERVICE_TOKEN` (длинная случайная строка; для dev и prod — разные значения):

| Сервис | Нужен `INTERNAL_SERVICE_TOKEN` | Нужен `DEBUG` |
|--------|-------------------------------|---------------|
| `authserver/` | да | да |
| `backend/` | да | да |
| `tgserver/` | да | да |
| `frontend/`, `tgbot/` | нет | по необходимости |

### 2. Примеры `.env` для локальной разработки

**`_auth_db/.env`**

```env
POSTGRES_DB=diary_auth
POSTGRES_USER=diary_auth_user
POSTGRES_PASSWORD=change_me_strong_password
```

**`_back_db/.env`** — аналогично, свои `POSTGRES_*`.

**`_redis/.env`**

```env
REDIS_USER=diary_redis
```

**`authserver/.env`** (фрагмент; `SQL_PASSWORD` подставится из `_auth_db` при генерации)

```env
DEBUG=true
SSL=false
INTERNAL_SERVICE_TOKEN=change_me_same_in_backend_and_tgserver
DATABASE=postgres
DJANGO_ALLOWED_HOSTS=["localhost","127.0.0.1"]
CORS_ALLOWED_ORIGINS=["http://localhost","http://127.0.0.1"]
CORS_ALLOW_CREDENTIALS=true
ACCESS_TOKEN_LIFETIME=30
REFRESH_TOKEN_LIFETIME=10080
PROJECT_HOSTS={"frontend":"http://localhost/","auth_server":"http://authserver:8000/","backend":"http://back:8000/","tg_server":"http://botapi:8000/"}
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=diary_auth
SQL_USER=diary_auth_user
SQL_HOST=auth_db
SQL_PORT=5432
```

**`backend/.env`** — те же `DEBUG`, `SSL`, `INTERNAL_SERVICE_TOKEN` (как в authserver), `CORS_*`, `PROJECT_HOSTS`, токены; `SQL_*` указывают на `back_db` и свою БД.

**`frontend/.env`**

```env
DEBUG=true
SSL=false
SINGLE_USER=false
DJANGO_ALLOWED_HOSTS=["localhost","127.0.0.1"]
ACCESS_TOKEN_LIFETIME=30
REFRESH_TOKEN_LIFETIME=10080
PROJECT_HOSTS={"frontend":"http://localhost/","auth_server":"http://authserver:8000/","backend":"http://back:8000/","tg_server":"http://botapi:8000/"}
```

**`tgbot/.env`**

```env
TOKEN=your_telegram_bot_token
ID=your_telegram_user_id
SITELINK=http://localhost/
PROJECT_HOSTS={"tg_server":"http://botapi:8000/"}
DEBUG=true
```

**`tgserver/.env`**

```env
DEBUG=true
INTERNAL_SERVICE_TOKEN=change_me_same_in_authserver_and_backend
PROJECT_HOSTS={"backend":"http://back:8000/","auth_server":"http://authserver:8000/","tg_server":"http://botapi:8000/"}
TGTOKEN=your_telegram_bot_token
MY_TG_ID=your_telegram_user_id
REDIS_WORKS=true
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_USER=diary_redis
REDIS_USER_PASSWORD=will_be_overwritten_from_redis_secrets
```

JSON в `PROJECT_HOSTS` и списках хостов должен быть **валидным** (двойные кавычки, без лишних запятых).

### 3. Запуск

**Вариант A — один скрипт (Linux / WSL / Git Bash):**

```bash
chmod +x start-with-secrets.sh */generate-secrets.sh _*/generate-secrets.sh
./start-with-secrets.sh
```

Скрипт: останавливает старые контейнеры → генерирует все `*-secrets.txt` → `docker compose up -d` → настраивает права на `_media/data` (нужен `sudo` на Linux).

**Вариант B — вручную:**

```bash
cd _redis && ./generate-secrets.sh && cd ..
cd _auth_db && ./generate-secrets.sh && cd ..
cd _back_db && ./generate-secrets.sh && cd ..
cd authserver && ./generate-secrets.sh && cd ..
cd backend && ./generate-secrets.sh && cd ..
cd frontend && ./generate-secrets.sh && cd ..
cd tgbot && ./generate-secrets.sh && cd ..
cd tgserver && ./generate-secrets.sh && cd ..

docker compose up -d --build
```

### 4. Открыть приложение

| Режим | URL | Nginx config |
|-------|-----|--------------|
| Локально (HTTP) | http://localhost | `nginx/conf.d/local.conf` |
| Production (HTTPS) | https://your-domain.com | `nginx/conf.d/prod.conf` |

Для локальной разработки в `docker-compose.yaml` заменить монтирование конфига:

```yaml
# вместо prod.conf:
- ./nginx/conf.d/local.conf:/etc/nginx/conf.d/default.conf
```

Прямой доступ к сервисам (без Nginx): frontend `:8000`, auth `:8001`, backend `:8002`, tgserver `:8003`.

### 5. Первый пользователь

1. Открыть http://localhost/registration  
2. Зарегистрировать аккаунт (при регистрации на backend создаются корневые папки `root`)  
3. Войти через http://localhost/login  

Для Telegram: в настройках приложения запустить привязку бота (flow `tg-auth/*` на authserver).

---

## API (кратко)

Префиксы через Nginx:

| Префикс | Сервис | Примеры |
|---------|--------|---------|
| `/auth/` | authserver | `registration`, `obtain`, `refresh`, `logout`, `verify` |
| `/api/` | backend | `file-system/record-content/`, `records/`, `file-system/notice-content/`, `notices/` |

Аутентификация в браузере: JWT в cookies `access_token` / `refresh_token` (HttpOnly). Backend проверяет токены через authserver (`AuthMiddleware`).

---

## Тесты

Периодический расчёт дат (ключевая бизнес-логика напоминаний):

```bash
cd backend/root
python manage.py test main.tests.TestOfTestDateAPI
```

Для запуска нужны зависимости из `backend/requirements.txt` и переменные окружения (как минимум `SECRET_KEY`, `DEBUG=true`, `INTERNAL_SERVICE_TOKEN`, `PROJECT_HOSTS`, lifetimes токенов). В GitHub Actions те же переменные заданы в `.github/workflows/ci-cd.yml`. Тестовые URL `/api/tests/` доступны при `DEBUG=true` или при `manage.py test`.

---

## Production и SSL

1. Настроить `prod.conf`: заменить `server_name` на нужный домен.  
2. Получить сертификаты через [`ssl-factory`](ssl-factory/README.md) и положить `cert.pem` / `key.pem` в `nginx/ssl/`.  
3. В `.env` сервисов: `DEBUG=false`, `SSL=true`, актуальные `DJANGO_ALLOWED_HOSTS` и `CORS_ALLOWED_ORIGINS`; **один prod-`INTERNAL_SERVICE_TOKEN`** в `authserver`, `backend`, `tgserver`.  
4. Перегенерировать секреты и перезапустить стек.

Подробности обновления сертификатов без простоя — в `ssl-factory/README.md`.

---

## Безопасность

- Не коммитим `*.env`, `*-secrets.txt`, `credentials.txt`, токены бота и пароли БД.  
- Файлы `*-secrets.txt` и `credentials.txt` в `.gitignore`.  
- В production: `DEBUG=false`, `SSL=true` — тестовые API (`/api/tests/`, `set-test/`, тестовые маршруты tgserver) не регистрируются.  
- Внутренние эндпоинты (`api/tg-server/*`, `api/auth/create-roots/`, часть `auth/users/*`, `tgapi/set-notice-list/`) требуют заголовок `X-Service-Token` с `INTERNAL_SERVICE_TOKEN`.  

---

## Автор

Пет-проект для демонстрации backend-разработки: микросервисы, JWT, Docker, PostgreSQL, Celery, Telegram API, работа с timezone и периодическими задачами.
