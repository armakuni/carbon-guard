format:
	uv run ruff check . --fix
	uv run ruff format .


lint:
	uv run ruff check .
	uv run ruff format . --check
	uv run mypy .

test:
	uv run pytest tests

integration:
	specdown run README.md --add-path ${PWD}/tests/scripts --env DATA_SOURCE=file --env CO2_SIGNAL_API_KEY=$(shell cat .co2_api_key)

