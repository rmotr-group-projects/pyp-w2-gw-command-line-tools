.PHONY: test test-cov

TAG="\n\n\033[0;32m\#\#\# "
END=" \#\#\# \033[0m\n"
PROJECT_PACKAGE=cmd_line_tools


test:
	@echo $(TAG)Running tests$(END)
	PYTHONPATH=. py.test -s tests
	
test-json:
	@echo $(TAG)Running tests just on json extension$(END)	
	PYTHONPATH=. py.test -s tests/test_mixins.py::JsonMixinTestCase

test-cov:
	@echo $(TAG)Running tests with coverage$(END)
	PYTHONPATH=. py.test --cov=$(PROJECT_PACKAGE) tests

coverage:
	@echo $(TAG)Coverage report$(END)
	@PYTHONPATH=. coverage run --source=$(PROJECT_PACKAGE) $(shell which py.test) ./tests -q --tb=no >/dev/null; true
	@coverage report
