# **Software Requirements Specification (SRS): MechAnalyser 2.0.0**

## 1. Introduction

### 1.1 Purpose
The purpose of this document is to define the software requirements for MechAnalyser 2.0.0. This version introduces significant upgrades, including support for multiple experiments, session saving, advanced plotting, statistical analysis, and enhanced data organization.

### 1.2 Scope
MechAnalyser 2.0.0 is a desktop application designed for analyzing mechanical testing data. It supports multiple experiment types, advanced data visualization, and statistical analysis, enabling researchers to organize experiments into studies and laboratories.

### 1.3 Definitions, Acronyms, and Abbreviations
- **Session:** A saved state of the application, including configurations, plots, and analysis.
- **Study:** A collection of multiple experiments grouped together.
- **Laboratory:** A collection of multiple studies grouped together.
- **Region:** A specific area from which samples are taken.
- **Specimen:** An individual unit containing multiple regions.
- **Group:** A collection of samples for comparison.

### 1.4 References
- Product Requirements Document (PRD) for MechAnalyser 2.0.0

---

## 2. Overall Description

### 2.1 Product Perspective
MechAnalyser 2.0.0 builds upon the existing application by introducing new features for multi-experiment analysis, session management, and advanced plotting. It is designed to be extensible and user-friendly.

### 2.2 Product Functions
- Configure and analyze multiple experiments.
- Save and reopen sessions.
- Group experiments into studies and laboratories.
- Advanced plotting and statistical analysis.

### 2.3 User Characteristics
- **Researchers:** Require advanced analysis and visualization tools.
- **Lab Technicians:** Need efficient data organization and reporting.
- **Developers:** Require extensibility for adding new experiments.

### 2.4 Constraints
- Must run on Windows.
- Must run on macOS.
- Must handle large datasets efficiently.

---

## 3. Specific Requirements

### 3.1 Functional Requirements
Refer to the PRD for detailed functional requirements.

### 3.2 Non-Functional Requirements
- Performance: Ensure efficient handling of large datasets, querying, and PDF generation.
- Usability: Intuitive interface for non-technical users, including searchable help and documentation sections.
- Extensibility: Easy to add new experiments or instruments.

### 3.3 Data Interoperability
- The system must support exporting analysis results to JSON format for integration with external tools.
- The system must support importing JSON files containing experiment configurations and data.

### 3.4 Cross-Platform Consistency
- The application must provide identical functionality and appearance on macOS and Windows platforms.

---

## 4. Appendices
- **Version:** 2.0.0
- **Author:** Kez Development Team
- **Date:** 18 April 2025