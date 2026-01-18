# MechAnalyser

A Python-based application for automated analysis of mechanical testing data from
biological tissues, providing standardized processing and reproducible results across
experiments.

## Overview

MechAnalyser manages the analysis of mechanical testing data using a modular,
experiment-type-driven architecture. It provides:

- **Automated analysis pipelines** for three experiment types: compression-to-failure,
  stepwise compression, and microindentation
- **Batch processing capabilities** for consistent analysis across multiple samples
- **Interactive visualization** with real-time plotting for quality assessment
- **Modular experiment architecture** allowing easy extension to new test types
- **Cross-platform compatibility** with Windows and macOS support

The configuration philosophy emphasizes:
- Explicit parameter specification with user verification
- Declarative analysis workflows that are reproducible
- Clear separation between raw data processing and result generation
- Standardized output formats for downstream statistical analysis

## Repository Structure

```
.
├── datasets/                       # Datasets for processing
│   └── example/                    # Example dataset
│       ├── properties/             # Example sample physical properties
|       |   └ properties.csv        # Example sample physical properties database
|       |
│       ├── sample1.csv             # Example sample 1 compression data
│       ├── sample2.csv             # Example sample 2 compression data
│       └── sample3.csv             # Example sample 3 compression data
│
├── doc/                            # Documentation
├── mech_analyser/                  # Main application package
│   ├── __init__.py
│   ├── config.py                   # Experiment module configuration
│   ├── mech_analyser.py            # Main GUI application
│   ├── version.py                  # Version information
│   │
│   ├── experiment/                 # Experiment analysis modules
│   │   ├── analyser.py             # Base analyser classes
│   │   ├── collation.py            # Base result collation logic
│   │   ├── data.py                 # Base data processing logic
│   │   ├── instron_68tm/           # Instron 68TM instrument support
│   │   │   ├── failure/            # Compression-to-failure analysis
│   │   │   └── stepwise/           # Stepwise compression analysis
│   │   ├── microtester_g2/         # Microtester G2 instrument support
│   │   │   └── microindentation/   # Microindentation analysis
│   │   ├── phase.py                # Base phase detection logic
│   │   ├── registry.py             # Experiment registration
│   │   └── ui.py                   # Base UI components for experiments
│   │
│   ├── study/                      # Sample and study management
│   ├── ui/                         # User interface components
│   └── util/                       # Utility modules
│
├── tests/                          # Unit tests
|   ├── experiment/                 # Experiment analysis unit tests
|   ├── study/                      # Sample and study unit tests
|   └── util/                       # Utility unit tests
│
├── README.md                       # This file
├── LICENSE                         # MIT license
├── Makefile                        # Build and test automation
└── requirements.txt                # Python dependencies
```

## Quick Start

### Installation

See the Installation section below for complete setup instructions.

### Running the Application

1. Install dependencies: `pip install -r requirements.txt`
2. Launch the GUI: `python -m mech_analyser.mech_analyser`
3. Import CSV data files from your mechanical testing instrument
4. Configure analysis parameters and sample properties
5. Process samples and export results

### Example Dataset

For testing and demonstration purposes, example datasets are provided in
`datasets/example/`:

- **Data Files**: 
  - `sample1.csv` - Baseline compression-to-failure test data
  - `sample2.csv` - Stiffer material (higher forces for same displacement)
  - `sample3.csv` - Softer material (lower forces for same displacement)
- **Properties File**: `properties/properties.csv` - Contains sample properties for all
  three samples

Use these files to familiarize yourself with batch processing and comparing results across
multiple samples.

### Adding a New Experiment Type

1. Create a new module directory under `mech_analyser/experiment/`
2. Implement analyser, data, phase, ui, and collation modules
3. Add the module path to `EXPERIMENT_MODULES` in `config.py`

## Experiment Types

### Compression-to-Failure Analysis (Instron 68TM)

Compression-to-failure experiments determine fundamental mechanical properties:

- **Data Processing**: Force-displacement to stress-strain conversion with tare removal
- **Young's Modulus**: Linear regression using fixed range, anchor point, or
  R²-maximization methods
- **Ultimate Properties**: Maximum stress/strain identification
- **Toughness**: Numerical integration under the stress-strain curve
- **Output**: Stress-strain plots with regression overlays and mechanical property
  summaries

### Stepwise Compression Analysis (Instron 68TM)

Stepwise compression characterizes viscoelastic behavior:

- **Phase Detection**: Automatic identification of relaxation periods at target strains
- **Relaxation Modeling**: Exponential decay fitting (σ(t) = a·exp(-t/τ) + b)
- **Time Constants**: Quantification of relaxation rates via τ parameter
- **Output**: Stress-time curves with fitted models and goodness-of-fit metrics

### Microindentation Analysis (Microtester G2)

Microindentation measures localized properties using contact mechanics:

- **Hertzian Modeling**: Nonlinear regression of force-displacement data
- **Reduced Modulus**: Extraction of E/(1-ν²) from F = (4/3)·E/(1-ν²)·√R·(δ-a)^1.5 + b
- **Energy Dissipation**: Calculation using Gauss's area formula on hysteresis loops
- **Output**: Force-displacement plots with modulus values and dissipation metrics

## Key Features

### Automated Analysis Pipelines

Each experiment type includes a complete analysis workflow:
- Raw data import with configurable column mapping
- Automatic unit conversion to SI units via Pint
- Parameter scaling for numerical stability in regressions
- Goodness-of-fit assessment with R² reporting

### Batch Processing and Collation

Multiple samples can be analyzed consistently:
- Identical parameter application across samples
- Automatic result aggregation into summary tables
- Excel export with multi-row headers and unit labels
- Group and specimen name tracking for statistical analysis

### Interactive Visualization

Real-time quality assessment capabilities:
- PyQtGraph-based plotting with hardware acceleration
- Visual indicators showing regression data ranges
- Interactive inspection of fitted models
- Automatic axis labeling with units

### Modular Architecture

Extensible design for new experiment types:
- Independent modules for each experiment
- Shared base classes and utilities
- Declarative configuration via config.py
- GUI integration through registry system

## Development

### Building a Standalone Application

Create distributable executables using PyInstaller:

**Using Makefile (Recommended):**
```bash
make dist
```

The executable appears in `dist/MechAnalyser/`.

### Testing

Run the complete test suite:
```bash
make test
```

Or run individual test modules:
```bash
python -m unittest tests/experiment/test_data.py
python -m unittest tests/experiment/test_phase.py
python -m unittest tests/experiment/test_analyser.py
python -m unittest tests/study/test_sample.py
python -m unittest tests/study/test_study.py
python -m unittest tests/util/test_serialiser.py
```

### Configuration Changes

1. Edit analysis parameters in experiment modules
2. Update GUI components in ui/ directory
3. Test changes: `make test`
4. Rebuild application: `make dist`

## Design Principles

1. **Reproducible**: Same input data and parameters produce identical results
2. **Modular**: Experiment types are independent and easily extensible
3. **Validated**: Numerical stability checks and goodness-of-fit reporting
4. **User-Centric**: Interactive GUI with real-time feedback
5. **Standards-Based**: Uses established scientific computing libraries
6. **Open-Source**: MIT licensed for academic and commercial use

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for
details.

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull
requests. For major changes, please open an issue first to discuss the proposed
modifications.