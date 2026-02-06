SHELL := /bin/bash

IMAGE_NAME ?= project-chimera
IMAGE_TAG  ?= dev
IMAGE      := $(IMAGE_NAME):$(IMAGE_TAG)

.PHONY: help setup test test-local docker-build docker-test spec-check clean

help:
	@echo "Targets:"
	@echo "  make setup       - Install deps locally using uv"
	@echo "  make test-local  - Run pytest locally (no Docker)"
	@echo "  make docker-build- Build Docker image"
	@echo "  make test        - Run tests in Docker (CI uses this)"
	@echo "  make spec-check  - Basic repo structure check"
	@echo "  make clean       - Remove local caches"

setup:
	uv sync

test-local:
	uv run pytest -q

docker-build:
	docker build -t $(IMAGE) .

docker-test:
	docker run --rm $(IMAGE)

test: docker-build docker-test

spec-check:
	@test -d specs || (echo "specs/ folder missing" && exit 1)
	@test -d tests || (echo "tests/ folder missing" && exit 1)
	@echo "Spec-check OK: specs/ and tests/ exist."

clean:
	rm -rf .pytest_cache **/__pycache__ .ruff_cache .mypy_cache
