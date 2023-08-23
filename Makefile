test-ci:
	python3.11 test.py | diff tests_output.txt -