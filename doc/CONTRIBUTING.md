# Contributing to MechAnalyser

Thank you for your interest in contributing to MechAnalyser! This document provides
guidelines and instructions for contributors.

## Table of Contents

- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Adding New Features](#adding-new-features)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Building and Distribution](#building-and-distribution)
- [Submitting Contributions](#submitting-contributions)

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/MechAnalyser.git
   cd MechAnalyser
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Running the Application

Launch the GUI application:
```bash
python -m mech_analyser.mech_analyser
```

### Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make changes
3. Run tests: `make test`
4. Commit changes: `git commit -m "Description of changes"`
5. Push to the branch: `git push origin feature/your-feature-name`
6. Create a pull request

## Project Structure

MechAnalyser follows a modular architecture:

```
mech_analyser/
├── experiment/                 # Experiment analysis modules
│   ├── analyser.py            # Base analyser classes
│   ├── data.py                # Base data processing logic
│   ├── phase.py               # Base phase detection logic
│   ├── ui.py                  # Base UI components
│   └── [instrument]/          # Instrument-specific modules
│       ├── __init__.py        # Instrument module definition
│       ├── analyser.py        # Instrument base analyser
│       ├── data.py            # Instrument base data classes
│       ├── phase.py           # Instrument base phase classes
│       └── ui.py              # Instrument base UI components
│       └── [experiment]/      # Experiment-specific implementations
│           ├── __init__.py    # Experiment module definition
│           ├── analyser.py    # Experiment analyser
│           ├── collation.py   # Result collation
│           ├── data.py        # Data processing
│           ├── phase.py       # Phase detection
│           ├── ui.py          # UI components
│           ├── view.py        # UI view logic (generated from view.ui)
│           └── view.ui        # Qt Designer UI file
├── study/                     # Sample and study management
├── ui/                        # General UI components
└── util/                      # Utility modules
```

## Adding New Features

### Adding New Instruments

To add support for a new mechanical testing instrument:

1. Create a new directory under `mech_analyser/experiment/` named after the instrument
   (e.g., `new_instrument`)

2. Use the provided
   [VS Code snippets](https://code.visualstudio.com/docs/editing/userdefinedsnippets) to
   create the files in this order:
    - Use "new module (instrument)" snippet for `__init__.py`
    - Use "new data (instrument)" snippet for `data.py`
    - Use "new phase (instrument)" snippet for `phase.py`
    - Use "new analyser (instrument)" snippet for `analyser.py`
    - Use "new ui (instrument)" snippet for `ui.py`

   Fill out each snippet placeholder by hitting TAB to jump to the next one.

3. Implement the specific logic for the instrument's data format and analysis
   requirements. Refer to the corresponding file in already implemented instruments for an
   understanding of what should go in the placeholders.

4. Update the README.md file to document the new instrument support, including its
   capabilities and any specific requirements.

### Adding New Experiments

To add a new type of mechanical experiment:

1. Within an existing instrument directory, create a new experiment subdirectory (e.g.,
   `new_experiment`)

2. Use the provided
   [VS Code snippets](https://code.visualstudio.com/docs/editing/userdefinedsnippets) to
   create the files in this order:
    - Use "new module (experiment)" snippet for `__init__.py`
    - Use "new data (experiment)" snippet for `data.py`
    - Use "new phase (experiment)" snippet for `phase.py`
    - Use "new analyser (experiment)" snippet for `analyser.py`
    - Use "new ui (experiment)" snippet for `ui.py`
    - Use "new horizontal collation (experiment)" or "new vertical collation (experiment)"
      snippet for `collation.py`
    - Use "new widget" snippet for `view.ui`

   Fill out each snippet placeholder by hitting TAB to jump to the next one.

3. Implement the specific logic for the experiment's data format and analysis
   requirements. Refer to the corresponding file in already implemented experiments for an
   understanding of what should go in the placeholders.

4. Populate the UI layout file `view.ui` using Qt Designer:
   ```bash
   pyside6-designer mech_analyser/experiment/new_instrument/new_experiment/view.ui
   ```

5. Generate the `view.py` file from `view.ui`:
   ```bash
   pyside6-uic mech_analyser/experiment/new_instrument/new_experiment/view.ui \
       -o mech_analyser/experiment/new_instrument/new_experiment/view.py
   ```

6. Add the new experiment module to `EXPERIMENT_MODULES` in `mech_analyser/config.py`:
   ```python
   EXPERIMENT_MODULES = [
       # ... existing modules
       "mech_analyser.experiment.new_instrument.new_experiment",
   ]
   ```

7. Update the README.md file to document the new experiment type, including its data
   processing, phase detection, and output details.

## Coding Standards

### Python Style

- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Use dataclasses for parameter and data structures
- Use descriptive variable and method names
- Add docstrings to all classes and methods

### Code Organization

- Keep classes focused on single responsibilities
- Use inheritance from base classes appropriately
- Separate data processing from UI logic
- Use the established naming conventions (ma_ prefix for imports)

### Documentation

- Add comprehensive docstrings explaining purpose, parameters, and return values
- Include type information in docstrings
- Document any assumptions or limitations

## Testing

### Running Tests

Run the complete test suite:
```bash
make test
```

Run specific test modules:
```bash
python -m unittest tests.experiment.test_data
python -m unittest tests.experiment.test_analyser
```

### Writing Tests

- Add unit tests for new classes and methods
- Place tests in corresponding directories under `tests/`
- Test both success and failure cases
- Use realistic test data when possible

### Test Coverage

Ensure changes maintain or improve test coverage. Run tests before submitting pull
requests.

## Building and Distribution

### Creating Executables

Build standalone executables using PyInstaller:

```bash
make dist
```

The executable will be created in `dist/MechAnalyser/`.

### Distribution

- Separate executables can be created for Windows and macOS
- Include all dependencies in the build
- Test the built executable on target platforms

## Submitting Contributions

### Pull Request Process

1. Ensure code follows the coding standards
2. Add or update tests as necessary
3. Update documentation if needed
4. Run the full test suite
5. Create a pull request with a clear description of changes

### Commit Guidelines

- Use clear, descriptive commit messages
- Keep commits focused on single changes
- Reference issue numbers when applicable

### Code Review

- All contributions require review before merging
- Address review feedback promptly
- Contributors should be open to suggestions for improvement

### Reporting Issues

- Use GitHub issues for bug reports and feature requests
- Provide detailed descriptions including steps to reproduce
- Include relevant system information and error messages

Thank you for contributing to MechAnalyser!