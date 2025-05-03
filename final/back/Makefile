# Define the Docker Compose command for reusability
DOCKER_COMPOSE = docker-compose -f docker-compose.yml

# Default target (what happens when you just run `make`)
.PHONY: help
help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: dev
dev: ## Start the development server with Docker Compose (builds and runs in detached mode)
	$(DOCKER_COMPOSE) up --build -d

.PHONY: down
down: ## Stop and remove Docker containers
	$(DOCKER_COMPOSE) down

.PHONY: logs
logs: ## View logs from Docker containers
	$(DOCKER_COMPOSE) logs -f

.PHONY: build
build: ## Build Docker containers without starting them
	$(DOCKER_COMPOSE) build

.PHONY: migrate
migrate: ## Run Django database migrations inside the app container
	$(DOCKER_COMPOSE) exec app python manage.py migrate

.PHONY: makemigrations
makemigrations: ## Create new Django migrations based on model changes
	$(DOCKER_COMPOSE) exec app python manage.py makemigrations

.PHONY: shell
shell: ## Open a Django shell inside the app container
	$(DOCKER_COMPOSE) exec app python manage.py shell

.PHONY: createsuperuser
createsuperuser: ## Create a Django superuser inside the app container
	$(DOCKER_COMPOSE) exec app python manage.py createsuperuser

.PHONY: test
test: ## Run Django tests inside the app container
	$(DOCKER_COMPOSE) exec app python manage.py test

.PHONY: clean
clean: ## Remove Docker containers, networks, and volumes (be careful!)
	$(DOCKER_COMPOSE) down -v --remove-orphans

.PHONY: ps
ps: ## List running Docker containers
	$(DOCKER_COMPOSE) ps