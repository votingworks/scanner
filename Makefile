
test:
	python -m pytest

coverage:
	python -m pytest --cov=scanner

run:
	python -m scanner.core
