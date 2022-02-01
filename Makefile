.PHONY: test all shell clean lint
test:
	poetry run tox
shell:
	poetry shell
build:
	poetry build
lint:
	poetry run pre-commit run --all
clean:
	rm -rf dist
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
