# Makefile for managing the Dockerized FastAPI application

.PHONY: help build up down logs restart shell clean rebuild dev prod status

# Default target
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build the Docker images
	docker-compose build

up: ## Start the services in detached mode
	docker-compose up -d

down: ## Stop and remove the services
	docker-compose down

logs: ## Follow the logs of all services
	docker-compose logs -f

logs-backend: ## Follow the logs of the backend service only
	docker-compose logs -f backend

restart: ## Restart all services
	docker-compose restart

restart-backend: ## Restart only the backend service
	docker-compose restart backend

shell: ## Open an interactive shell in the backend container
	docker-compose exec backend /bin/bash

status: ## Show the status of all services
	docker-compose ps

clean: ## Stop services and remove containers, networks, and volumes
	docker-compose down -v --remove-orphans

rebuild: ## Rebuild and restart all services
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d

dev: ## Start development environment with live reloading
	docker-compose up --build

prod: ## Start production environment in detached mode
	docker-compose up -d --build

stop: ## Stop all services without removing them
	docker-compose stop

start: ## Start existing services
	docker-compose start

pull: ## Pull the latest images
	docker-compose pull

# Development helpers
test: ## Run tests inside the backend container
	docker-compose exec backend python -m pytest

lint: ## Run linting inside the backend container
	docker-compose exec backend python -m flake8 app/

format: ## Format code using black inside the backend container
	docker-compose exec backend python -m black app/

# Monitoring
top: ## Show running processes in containers
	docker-compose top

stats: ## Show container resource usage statistics
	docker stats $(shell docker-compose ps -q)