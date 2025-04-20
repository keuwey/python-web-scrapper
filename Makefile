lint:
	ruff check --fix .
	ruff format .

typecheck:
	mypy .
	pyright .
