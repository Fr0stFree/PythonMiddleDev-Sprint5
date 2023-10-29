MOVIES_INDEX := http://localhost:9200/movies
PERSONS_INDEX := http://localhost:9200/persons
GENRES_INDEX := http://localhost:9200/genres
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
	@echo "$(COLOR_GREEN)Be patient, it could take some time$(COLOR_RESET)"

	@echo "$(COLOR_GREEN)Uploading movies...$(COLOR_RESET)"
	@elasticdump \
	  --input=$(DUMP_DIR)/movies_analyzer.json \
	  --output=$(MOVIES_INDEX) \
	  --type=analyzer

	@elasticdump \
	  --input=$(DUMP_DIR)/movies_mapping.json \
	  --output=$(MOVIES_INDEX) \
	  --type=mapping

	@elasticdump \
	  --input=$(DUMP_DIR)/movies.json \
	  --output=$(MOVIES_INDEX) \
	  --type=data

	@echo "$(COLOR_GREEN)Uploading persons...$(COLOR_RESET)"
	@elasticdump \
	  --input=$(DUMP_DIR)/persons_analyzer.json \
	  --output=$(PERSONS_INDEX) \
	  --type=analyzer

	@elasticdump \
	  --input=$(DUMP_DIR)/persons_mapping.json \
	  --output=$(PERSONS_INDEX) \
	  --type=mapping

	@elasticdump \
	  --input=$(DUMP_DIR)/persons.json \
	  --output=$(PERSONS_INDEX) \
	  --type=data

		@echo "$(COLOR_GREEN)Uploading genres...$(COLOR_RESET)"
	@elasticdump \
	  --input=$(DUMP_DIR)/genres_analyzer.json \
	  --output=$(GENRES_INDEX) \
	  --type=analyzer

	@elasticdump \
	  --input=$(DUMP_DIR)/genres_mapping.json \
	  --output=$(GENRES_INDEX) \
	  --type=mapping

	@elasticdump \
	  --input=$(DUMP_DIR)/genres.json \
	  --output=$(GENRES_INDEX) \
	  --type=data