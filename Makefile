lint:
	ruff check --fix *.py
	ruff format *.py

typecheck:
	mypy *.py
	pyright *.py
