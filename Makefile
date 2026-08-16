.PHONY: validate test

PYTHON ?= python3

validate:
	$(PYTHON) validator/vepp_validator.py schema/vepp.schema.json examples/*.json

test:
	$(PYTHON) -m pytest -q tests
