.PHONY: run
run:
	python eat_prediction/main.py

.PHONY: test
test:
	pytest test/