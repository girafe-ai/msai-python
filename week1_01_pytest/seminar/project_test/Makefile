REQUIREMENTS_DEV="requirements-dev.txt"
REQUIREMENTS="requirements.txt"
PACKAGE_NAME="project-test"


test:
	@py.test tests

clean:
	@rm -rf `find . -name __pycache__`
	@rm -f `find . -type f -name '*.py[co]' `
	@rm -f `find . -type f -name '*~' `
	@rm -f `find . -type f -name '.*~' `
	@rm -f `find . -type f -name '@*' `
	@rm -f `find . -type f -name '#*#' `
	@rm -f `find . -type f -name '*.orig' `
	@rm -f `find . -type f -name '*.rej' `
	@rm -rf `find . -type d -name '.pytest_cache' `
	@rm -f .coverage
	@rm -rf htmlcov
	@rm -rf build
	@rm -rf cover
	@python setup.py clean
	@rm -rf .tox
	@rm -f .develop
	@rm -f .flake

uninstall:
	@pip uninstall ${PACKAGE_NAME} -y

install-dev: uninstall
	@pip install -r ${REQUIREMENTS_DEV}
	@pip install -e .

install: uninstall
	@pip install -r ${REQUIREMENTS}
	@echo "Done"

install-pre-commit: install-dev
	@pre-commit install

.PHONY: all install-dev uninstall clean test
