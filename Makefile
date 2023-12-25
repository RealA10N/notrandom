PY ?= python3

.PHONY: test build upload

test:
	python3 test.py | diff tests_output.txt -

build: test
	rm -rf dist build
	$(PY) -m pip install -U build
	$(PY) -m build -n

upload: build
	$(PY) -m pip install -U twine
	$(PY) -m twine upload dist/*
