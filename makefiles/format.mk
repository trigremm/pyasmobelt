# format-ruff.mk - Ruff-based Python formatting and linting

.PHONY: format-lint format-ruff f format

format-lint:
	ruff check --fix . || true

format-ruff:
	ruff format .

format: format-lint format-ruff

f: format
