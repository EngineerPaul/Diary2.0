# Управление проектом через Docker Compose.
# Запуск: Git Bash / WSL / Linux / macOS (нужны make и docker compose).

DOCKER_COMPOSE ?= docker compose
COMPOSE_FILE   = -f docker-compose.yaml
PROD_COMPOSE   = $(COMPOSE_FILE) -f docker-compose.prod.yaml
TEST_COMPOSE   = $(DOCKER_COMPOSE) -p diary-tests $(COMPOSE_FILE) -f docker-compose.test.yaml

# GnuWin32 make на Windows по умолчанию вызывает cmd.exe (нет grep/awk и bash-for).
ifeq ($(OS),Windows_NT)
SHELL := bash
endif

.PHONY: help start secrets up up-build up-prod up-build-prod down down-prod restart restart-prod ps ps-prod logs test

TEST_SERVICES = back authserver front botapi bot

help: ## Показать список команд
	@echo "Diary 2.0 — команды Make"
	@echo ""
	@echo "  help           Показать список команд"
	@echo "  start          Первый запуск (dev): секреты, сборка, up"
	@echo "  secrets        Перегенерировать все *-secrets.txt"
	@echo "  up             Поднять стек dev (HTTP, local.conf)"
	@echo "  up-build       Поднять dev с пересборкой образов"
	@echo "  up-prod        Поднять стек prod (HTTPS, prod.conf + ssl)"
	@echo "  up-build-prod  Поднять prod с пересборкой образов"
	@echo "  down           Остановить dev-стек"
	@echo "  down-prod      Остановить prod-стек"
	@echo "  restart        Перезапустить dev-стек"
	@echo "  restart-prod   Перезапустить prod-стек"
	@echo "  ps             Статус dev-контейнеров"
	@echo "  ps-prod        Статус prod-контейнеров"
	@echo "  logs           Логи dev: make logs SERVICES=\"bot botapi\""
	@echo "  test           Unit-тесты: make test SERVICES=\"bot\""

# --- Проект (dev — docker-compose.yaml) ---

start: ## Первый запуск: секреты, сборка, up (start-with-secrets.sh)
	bash start-with-secrets.sh

secrets: ## Перегенерировать все *-secrets.txt
	@for dir in _redis _auth_db _back_db authserver backend frontend tgbot tgserver; do \
		echo "==> $$dir"; \
		(cd $$dir && ./generate-secrets.sh) || exit 1; \
	done
	@echo "Secrets generated."

up: ## Поднять dev-стек (без пересборки)
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) up -d

up-build: ## Поднять dev-стек с пересборкой образов
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) up -d --build

down: ## Остановить dev-стек
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) down

restart: ## Перезапустить dev-стек
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) restart

ps: ## Статус dev-контейнеров
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) ps

logs: ## Логи dev (follow): make logs | make logs SERVICES="bot botapi"
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) logs -f --tail=100 $(SERVICES)


# --- Production (docker-compose.prod.yaml) ---

up-prod: ## Поднять prod-стек (без пересборки)
	$(DOCKER_COMPOSE) $(PROD_COMPOSE) up -d

up-build-prod: ## Поднять prod-стек с пересборкой образов
	$(DOCKER_COMPOSE) $(PROD_COMPOSE) up -d --build

down-prod: ## Остановить prod-стек
	$(DOCKER_COMPOSE) $(PROD_COMPOSE) down

restart-prod: ## Перезапустить prod-стек
	$(DOCKER_COMPOSE) $(PROD_COMPOSE) restart

ps-prod: ## Статус prod-контейнеров
	$(DOCKER_COMPOSE) $(PROD_COMPOSE) ps


# --- Тесты (docker-compose.test.yaml, без venv) ---

test: ## Unit-тесты: make test | make test SERVICES="bot". Сервисы: back, authserver, front, botapi, bot
	@for svc in $(if $(SERVICES),$(SERVICES),$(TEST_SERVICES)); do \
		echo "==> Testing $$svc"; \
		$(TEST_COMPOSE) run --rm --no-deps $$svc || exit 1; \
	done
