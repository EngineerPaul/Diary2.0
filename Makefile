# Управление проектом через Docker Compose.
# Запуск: Git Bash / WSL / Linux / macOS (нужны make и docker compose).

DOCKER_COMPOSE ?= docker compose
COMPOSE_FILE   = -f docker-compose.yaml
TEST_COMPOSE   = $(DOCKER_COMPOSE) -p diary-tests $(COMPOSE_FILE) -f docker-compose.test.yaml

.PHONY: help start secrets up up-build down restart ps logs test

TEST_SERVICES = back authserver front botapi bot

help: ## Показать список команд
	@echo "Diary 2.0 — команды Make"
	@echo ""
	@grep -E '^[a-zA-Z0-9_-]+:.*##' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

# --- Проект ---

start: ## Первый запуск: секреты, сборка, up (start-with-secrets.sh)
	bash start-with-secrets.sh

secrets: ## Перегенерировать все *-secrets.txt
	@for dir in _redis _auth_db _back_db authserver backend frontend tgbot tgserver; do \
		echo "==> $$dir"; \
		(cd $$dir && ./generate-secrets.sh) || exit 1; \
	done
	@echo "Secrets generated."

up: ## Поднять стек (без пересборки)
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) up -d

up-build: ## Поднять стек с пересборкой образов
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) up -d --build

down: ## Остановить и удалить контейнеры
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) down

restart: ## Перезапустить все сервисы
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) restart

ps: ## Статус контейнеров
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) ps

logs: ## Логи (follow): make logs | make logs SERVICES="bot botapi"
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) logs -f --tail=100 $(SERVICES)

# --- Тесты (docker-compose.test.yaml, без venv) ---

test: ## Unit-тесты: make test | make test SERVICES="bot". Сервисы: back, authserver, front, botapi, bot
	@for svc in $(if $(SERVICES),$(SERVICES),$(TEST_SERVICES)); do \
		echo "==> Testing $$svc"; \
		$(TEST_COMPOSE) run --rm --no-deps $$svc || exit 1; \
	done
