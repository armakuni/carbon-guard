format:
	poetry run python -m ruff check . --fix
	poetry run python -m isort .
	poetry run python -m black . 


lint:
	poetry run python -m ruff check .
	poetry run python -m isort . --check
	poetry run python -m black . --check
	poetry run python -m mypy .

test:
	poetry run python -m pytest tests

integration:
	specdown run README.md