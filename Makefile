
test:
	python -m pytest

coverage:
	python -m pytest --cov=scanner --cov-report term-missing

run:
	python -m scanner.core
