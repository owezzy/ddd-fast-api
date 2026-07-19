.PHONY: help sync run test lint format type-check hooks commit clean

help:
	@printf "Available targets:\n"
	@printf "  sync        Install runtime and development dependencies via uv\n"
	@printf "  run         Start the current scaffold application\n"
	@printf "  test        Run pytest\n"
	@printf "  lint        Run Ruff checks\n"
	@printf "  format      Apply Ruff fixes and formatting\n"
	@printf "  type-check  Run mypy against src\n"
	@printf "  hooks       Install local Husky git hooks\n"
	@printf "  commit      Open an interactive Commitizen conventional commit prompt\n"
	@printf "  clean       Remove local caches and test artifacts\n"

sync:
	uv sync --group dev

run:
	uv run python main.py

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff check . --fix
	uv run ruff format .

type-check:
	uv run mypy src

hooks:
	npm install

commit:
	uv run cz commit

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov build dist
	rm -f .coverage coverage.xml
