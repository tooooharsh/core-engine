.PHONY: format lint lint-fix typecheck check-all test

format:
	uv run ruff format src/ tests/

lint:
	uv run ruff check src/ tests/

lint-fix:
	uv run ruff check src/ tests/ --fix

typecheck:
	uv run mypy src/ tests/

test:
	uv run python -m pytest

check-all: format lint-fix typecheck test
