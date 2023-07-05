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
	specdown run README.md --add-path ${PWD}/tests/scripts --env DATA_SOURCE=file --env CO2_SIGNAL_API_KEY=$(shell cat .co2_api_key)

