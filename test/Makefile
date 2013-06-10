testrunner=./runtest.py

test:
	$(testrunner)

coverage_run:
	coverage run $(testrunner)

coverage_report:
	coverage report -m

coverage_erase:
	coverage erase

coverage: coverage_erase coverage_run coverage_report
	@echo "DONE"

.PHONY: test coverage_report coverage_erase coverage
