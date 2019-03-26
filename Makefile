
test:
	python -m pytest

coverage:
	python -m pytest --cov=scanner --cov-report term-missing --cov-fail-under=100

run:
	python -m scanner.core
