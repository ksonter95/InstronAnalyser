# **Technical Design Document (TDD): MechAnalyser 2.0.0**

## 1. Overview

### 1.1 Purpose
This document outlines the technical design for MechAnalyser 2.0.0, focusing on the architecture, modules, and implementation details for the new features.

### 1.2 Scope
The design covers the implementation of multi-experiment support, session management, advanced plotting, statistical analysis, enhanced data organization, bidirectional queries, PDF generation, and searchable help/documentation sections.

---

## 2. System Architecture

### 2.1 High-Level Architecture
- **Core Modules:**
  - `experiment/`: Handles experiment-specific logic.
  - `ui/`: Manages the graphical user interface.
  - `util/`: Provides utility functions for data processing.
- **New Modules:**
  - `session/`: Manages session saving and reopening.
  - `study/`: Handles grouping of experiments into studies.
  - `laboratory/`: Manages grouping of studies into laboratories.
  - `plot/`: Provides advanced plotting capabilities.
  - `statistics/`: Conducts statistical analysis on summary results.
  - `sample/`: Provides example datasets and pre-configured session files for testing and demonstration purposes. This module ensures seamless integration with other modules, such as `experiment/` and `ui/`, to load and validate sample data.
  - `query/`: Implements bidirectional database-style queries for samples and associations.
  - `pdf/`: Handles the generation of PDF reports with tables, plots, and statistical significance.
  - `help/`: Manages the searchable help section within the application.
  - `documentation/`: Manages the searchable documentation section for instruments and experiments.

---

## 3. Module Design

### 3.1 Session Management
- **Purpose:** Save and reopen application state.
- **Implementation:**
  - Serialize session data (configurations, plots, analysis) to a file.
  - Deserialize session data to restore state.

### 3.2 Multi-Experiment Support
- **Purpose:** Configure and analyze multiple experiments.
- **Implementation:**
  - Extend `experiment/` module to support multiple instances.
  - Introduce `study/` module for grouping experiments.

### 3.3 Advanced Plotting
- **Purpose:** Provide customizable and diverse plotting options.
- **Implementation:**
  - Use a plotting library (e.g., Matplotlib) for scatter, column, box, and pie charts.
  - Add configuration options for plot appearance and data selection.

### 3.4 Statistical Analysis
- **Purpose:** Conduct statistical tests on summary results.
- **Implementation:**
  - Use a statistical library (e.g., SciPy) for significance testing.
  - Integrate results into reports and visualizations.

### 3.5 Enhanced Data Organization
- **Purpose:** Support properties like region, specimen, and group.
- **Implementation:**
  - Extend data models to include new properties.
  - Update UI and processing logic to handle these properties.

### 3.6 Bidirectional Queries
- **Purpose:** Enable database-style queries for samples and associations.
- **Implementation:**
  - Develop a `query/` module to handle bidirectional queries.
  - Use in-memory data structures or a lightweight database (e.g., SQLite) for efficient querying.

### 3.7 PDF Generation
- **Purpose:** Generate PDF reports of analysis results.
- **Implementation:**
  - Use a Python library like ReportLab or FPDF to create PDF documents.
  - Include tables, plots, and statistical significance in the reports.

### 3.8 Help Section
- **Purpose:** Provide a searchable help section within the application.
- **Implementation:**
  - Develop a `help/` module to manage help content.
  - Use a search algorithm to enable keyword-based search functionality.

### 3.9 Documentation Section
- **Purpose:** Provide a searchable documentation section for instruments and experiments.
- **Implementation:**
  - Develop a `documentation/` module to manage documentation content.
  - Use a search algorithm to enable keyword-based search functionality.

### 3.10 JSON Import/Export
- **Purpose:** Enable data interoperability with external tools.
- **Implementation:**
  - Use Python's `json` module for serialization and deserialization.
  - Extend the `experiment/` module to support exporting processed data and summaries to JSON.
  - Add functionality in the `ui/` module for importing JSON files to restore configurations and data.

---

## 4. Data Flow
- **Input:** CSV files containing raw data.
- **Processing:** Data is analyzed, grouped, and visualized.
- **Output:** Plots, reports, session files, and PDF documents.

---

## 5. Appendices
- **Version:** 2.0.0
- **Author:** Kez Development Team
- **Date:** 18 April 2025