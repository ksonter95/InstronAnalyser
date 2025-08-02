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
		$$($(PYTHON) -c "from $(APP_PATH).config import EXPERIMENT_MODULES; print(' '.join(f'--hidden-import {m}' for m in EXPERIMENT_MODULES))") \
		$(ENTRY)

test:
	python -m unittest tests/experiment/test_data.py
	python -m unittest tests/experiment/test_phase.py
	python -m unittest tests/experiment/test_analyser.py
	python -m unittest tests/study/test_sample.py
	python -m unittest tests/study/test_study.py
	python -m unittest tests/util/test_serialiser.py
