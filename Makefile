# App metadata
APP_NAME := MechAnalyser
APP_PATH := mech_analyser
ICON := $(APP_PATH)/ui/icons/MechAnalyser.png
ENTRY := $(APP_PATH)/mech_analyser.py

# Python interpreter (override with `make PYTHON=...`)
# Compilation programmes (override with `make PYTHON=...`, ...)
PYTHON ?= python
PYINSTALLER ?= pyinstaller

.PHONY: all clean dist

all: dist

clean:
	rm -rf build dist __pycache__ *.spec
	find . -type d -name "__pycache__" -exec rm -r {} +

dist: $(ENTRY)
	$(PYINSTALLER) \
		--windowed \
		--name "$(APP_NAME)" \
		--icon=$(ICON) \
		--paths=$(APP_PATH) \
		--collect-submodules=experiment \
		$$($(PYTHON) -c "from $(APP_PATH).config import EXPERIMENT_MODULES; print(' '.join(f'--hidden-import {m}' for m in EXPERIMENT_MODULES))") \
		$(ENTRY)
