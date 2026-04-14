.PHONY: help install setup test lint format clean run docker-build docker-up docker-down

help:
	@echo "Shipsmart Make Commands"
	@echo "=================="
	@echo "install    - Install all dependencies"
	@echo "setup     - Run full setup (creates venv, installs deps)"
	@echo "test      - Run tests"
	@echo "lint     - Run linting"
	@echo "format   - Format code"
	@echo "clean    - Clean build artifacts"
	@echo "run      - Run API server"
	@echo "docker-build - Build Docker images"
	@echo "docker-up   - Start Docker services"
	@echo "docker-down - Stop Docker services"

install:
	pip install -r requirements.txt

setup: install
	python -m venv venv
	./venv/Scripts/pip install -r requirements.txt

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=src --cov-report=html

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	mypy src/ --ignore-missing-imports

format:
	black .
	isort .

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache
	rm -rf build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run:
	uvicorn src.api.main:app --reload

docker-build:
	docker build -t shipsmart:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

	  