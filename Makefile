PYTHON ?= python3

.PHONY: build check test serve import compose-bundles
build:
	$(PYTHON) scripts/build.py
check: build
	$(PYTHON) scripts/check.py
	$(PYTHON) scripts/check_compose.py
test: check
	$(PYTHON) -m unittest discover -s tests -v
serve: build
	$(PYTHON) -m http.server 8000 --bind 127.0.0.1 --directory dist
import:
	$(PYTHON) scripts/import_sources.py --root ..
compose-bundles:
	$(PYTHON) scripts/create_compose.py --root ..
	$(PYTHON) scripts/write_module_content.py
