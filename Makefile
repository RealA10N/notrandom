test-ci:
	python3 test.py | diff tests_output.txt -