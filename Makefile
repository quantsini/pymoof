all: install-dev install-hooks
	@echo "=========="
	@echo "Be sure to activate your virtualenv with '. venv/bin/activate'"

install-dev: venv
	. venv/bin/activate && pip install -r requirements.txt -r requirements-dev.txt

install-hooks:
	. venv/bin/activate && pre-commit install-hooks

venv:
	virtualenv -ppython3 venv

clean:
	rm -rf venv
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
