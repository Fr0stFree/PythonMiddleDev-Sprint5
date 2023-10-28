ELASTIC_URL := http://localhost:9200/movies
COMPOSE_FILE_PATH := ./docker-compose.dev.yml
ENV_FILE_PATH := ./.env
DUMP_DIR := ./dumps

COLOR_RESET = \033[0m
COLOR_GREEN = \033[32m
COLOR_YELLOW = \033[33m
COLOR_WHITE = \033[00m


.PHONY: build
build:
	@docker compose -f $(COMPOSE_FILE_PATH) --env-file $(ENV_FILE_PATH) up -d --build

.PHONY: logs
logs:
	@docker compose -f $(COMPOSE_FILE_PATH) --env-file $(ENV_FILE_PATH) logs -f

.PHONY: clean
clean:
	@docker compose -f $(COMPOSE_FILE_PATH) --env-file $(ENV_FILE_PATH) down -v --remove-orphans

.PHONY: loaddata
loaddata:
	@echo "$(COLOR_GREEN)Uploading...\nBe patient, it could take some time$(COLOR_RESET)"
	@elasticdump \
	  --input=$(DUMP_DIR)/movies_analyzer.json \
	  --output=$(ELASTIC_URL) \
	  --type=analyzer

	@elasticdump \
	  --input=$(DUMP_DIR)/movies_mapping.json \
	  --output=$(ELASTIC_URL) \
	  --type=mapping

	@elasticdump \
	  --input=$(DUMP_DIR)/movies.json \
	  --output=$(ELASTIC_URL) \
	  --type=data

.PHONY: dumpdata
dumpdata:
	@elasticdump \
	  --input=$(ELASTIC_URL) \
	  --output=$(DUMP_DIR)/movies_analyzer.json \
	  --type=analyzer
	@elasticdump \
	  --input=$(ELASTIC_URL) \
	  --output=$(DUMP_DIR)/movies_mapping.json \
	  --type=mapping
	@elasticdump \
	  --input=$(ELASTIC_URL) \
	  --output=$(DUMP_DIR)/movies.json \
	  --type=data

