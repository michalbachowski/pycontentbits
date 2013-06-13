testrunner=./runtest.py

test:
	$(testrunner)

coverage_run:
	export PYTHONPATH="`readlink -f '../src/'`:$$PYTHONPATH" && python -mcoverage run $(testrunner)

coverage_report:
	python -mcoverage report -m

coverage_erase:
	python -mcoverage erase

coverage: coverage_erase coverage_run coverage_report
	@echo "DONE"

.PHONY: test coverage_report coverage_erase coverage
