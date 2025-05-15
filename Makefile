VENV_DIR := .venv
PYTHON := $(VENV_DIR)/bin/python
DEPS := pyfastlanes==0.1.3post2

all: run

$(VENV_DIR)/bin/activate:
	@echo "-- Creating virtual environment..."
	python3 -m venv $(VENV_DIR)

install: $(VENV_DIR)/bin/activate
	@echo "-- Installing dependencies..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install $(DEPS)

run: install
	@echo "-- Running main.py..."
	$(PYTHON) main.py

clean:
	rm -rf $(VENV_DIR)
	find . -name '__pycache__' -type d -exec rm -r {} +
	rm -f data.fls
	@for dir in kv_cache_original diff_data; do \
		rm -f $$dir/decoded.csv; \
	done

.PHONY: all install run clean
