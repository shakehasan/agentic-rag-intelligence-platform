.PHONY: install seed ingest api eval test lint format safety docker-up

install:
	python -m pip install -e ".[dev]"

seed:
	python scripts/seed_synthetic_docs.py

ingest:
	python scripts/ingest_docs.py

api:
	uvicorn backend.app.main:app --reload

eval:
	python scripts/run_eval.py

test:
	pytest

lint:
	ruff check .

format:
	black .
	ruff check . --fix

safety:
	python scripts/public_safety_scan.py

docker-up:
	docker-compose up --build

