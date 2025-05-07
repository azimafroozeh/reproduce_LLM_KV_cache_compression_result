VENV_DIR := venv
PYTHON := $(VENV_DIR)/bin/python
DATASETS := kv_cache_original diff_data

all: run

$(VENV_DIR)/bin/activate:
	@echo "-- Creating virtual environment..."
	python3 -m venv $(VENV_DIR)

install: $(VENV_DIR)/bin/activate
	@echo "-- Installing pyfastlanes..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install pyfastlanes==0.1.3

run: install
	@for dataset in $(DATASETS); do \
		echo "-- Running main.py on dataset '$$dataset'..."; \
		$(PYTHON) main.py $$dataset; \
	done

clean:
	rm -rf $(VENV_DIR)
	find . -name '__pycache__' -type d -exec rm -r {} +
	rm -f data.fls
	@for dataset in $(DATASETS); do \
		rm -f $$dataset/decoded.csv; \
	done

.PHONY: all install run clean
