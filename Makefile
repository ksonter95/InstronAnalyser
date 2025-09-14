# App metadata
APP_NAME := MechAnalyser
APP_PATH := mech_analyser
ICON := $(APP_PATH)/ui/icons/MechAnalyser.png
ENTRY := $(APP_PATH)/mech_analyser.py

# Python interpreter (override with `make PYTHON=...`)
# Compilation programmes (override with `make PYTHON=...`, ...)
PYTHON ?= python
PYINSTALLER ?= pyinstaller

# Platform-specific pyinstaller options
ifeq ($(shell uname -s),Darwin)
	PYINSTALLER_OPTIONS := --windowed
else
	PYINSTALLER_OPTIONS := --windowed --onefile
endif

.PHONY: all clean dist test

all: dist

clean:
	rm -rf build dist __pycache__ *.spec
	find . -type d -name "__pycache__" -exec rm -r {} +

dist: $(ENTRY)
	$(PYINSTALLER) \
		$(PYINSTALLER_OPTIONS) \
		--name "$(APP_NAME)" \
		--icon=$(ICON) \
		--paths=$(APP_PATH) \
		--collect-submodules=experiment \
		$$($(PYTHON) -c "from $(APP_PATH).config import EXPERIMENT_MODULES; print(' '.join(f'--hidden-import {m} --hidden-import {m}.analyser --hidden-import {m}.collation --hidden-import {m}.data --hidden-import {m}.phase --hidden-import {m}.ui' for m in EXPERIMENT_MODULES))") \
		$(ENTRY)

test:
	$(PYTHON) -m unittest tests/experiment/test_data.py
	$(PYTHON) -m unittest tests/experiment/test_phase.py
	$(PYTHON) -m unittest tests/experiment/test_analyser.py
	$(PYTHON) -m unittest tests/study/test_sample.py
	$(PYTHON) -m unittest tests/study/test_study.py
	$(PYTHON) -m unittest tests/util/test_serialiser.py
