.PHONY: test shell env build link clean
env:
	poetry install
test: env
	poetry run tox
shell: env
	poetry shell
build: env
	poetry build
lint: env
	poetry run pre-commit run --all
clean:
	rm -rf dist
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
