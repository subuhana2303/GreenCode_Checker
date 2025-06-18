# Green Code Checker - Replit Project Guide

## Overview

Green Code Checker is a Streamlit-based web application that analyzes Python code for sustainability and efficiency patterns. The application provides a "Green Score" out of 100 and offers intelligent suggestions to help developers write more eco-friendly, efficient code. This tool promotes Green AI and eco-conscious coding practices, making it ideal for students, open-source projects, and professional portfolios.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web framework for rapid prototyping and deployment
- **Layout**: Wide layout with sidebar configuration for settings and quick actions
- **User Interface**: Clean, intuitive design with emoji-based visual elements and markdown formatting
- **Interactivity**: Real-time code analysis with downloadable reports

### Backend Architecture
- **Language**: Python 3.11
- **Architecture Pattern**: Modular design with separate components for analysis, suggestions, and reporting
- **Core Components**: 
  - Code analyzer using AST (Abstract Syntax Tree) parsing
  - Suggestion engine for generating improvement recommendations
  - Report generator for creating downloadable analysis summaries

### Processing Pipeline
1. Code input validation and syntax checking
2. AST-based code analysis for structural patterns
3. Regex-based pattern detection for inefficiencies
4. Scoring algorithm calculation
5. Suggestion generation based on findings
6. Report compilation and formatting

## Key Components

### 1. Code Analyzer (`analyzer.py`)
- **Purpose**: Core analysis engine that examines Python code for inefficient patterns
- **Technology**: Uses Python's `ast` module for syntax tree analysis and regex for pattern matching
- **Key Features**:
  - Function and import counting
  - Loop analysis (for/while loops)
  - Inefficient pattern detection
  - Unused import identification
  - Complexity scoring

### 2. Suggestion Engine (`suggestions.py`)
- **Purpose**: Generates actionable recommendations based on analysis results
- **Approach**: Rule-based system that provides specific suggestions for different code issues
- **Categories**: General efficiency, issue-specific recommendations, and best practices

### 3. Report Generator (`report_generator.py`)
- **Purpose**: Creates comprehensive downloadable reports
- **Output Format**: Structured text reports with timestamps and user attribution
- **Sections**: Score summary, code statistics, issues identified, and recommendations

### 4. Streamlit Application (`streamlit_app.py`)
- **Purpose**: Main web interface for the application
- **Features**: Code input, real-time analysis, sample code loading, and report downloading
- **Layout**: Sidebar for settings and main area for code analysis

### 5. Sample Code (`sample_code.py`)
- **Purpose**: Provides example inefficient code for testing and demonstration
- **Content**: Contains various Python anti-patterns like inefficient loops and unused imports

## Data Flow

1. **Input**: User provides Python code through Streamlit interface
2. **Parsing**: Code is validated and parsed using AST
3. **Analysis**: Multiple analyzers examine code for various inefficiency patterns
4. **Scoring**: Results are compiled into a Green Score (0-100)
5. **Suggestions**: Recommendation engine generates improvement suggestions
6. **Output**: Results displayed in web interface with option to download report

## External Dependencies

### Core Dependencies
- **Streamlit**: Web framework for creating the user interface
- **Python Standard Library**: `ast`, `re`, `datetime`, `io` for core functionality

### Development Dependencies
- **Python 3.11**: Runtime environment
- **Nix**: Package management and environment setup

### Deployment Dependencies
- **Replit**: Cloud-based development and hosting platform
- **Streamlit Server**: Built-in web server for application hosting

## Deployment Strategy

### Environment Setup
- **Runtime**: Python 3.11 with Nix package management
- **Configuration**: Streamlit server configured to run on port 5000
- **Deployment Target**: Autoscale deployment for handling variable traffic

### Application Startup
- **Primary Command**: `streamlit run streamlit_app.py --server.port 5000`
- **Fallback Command**: `streamlit run app.py --server.port 5000`
- **Server Configuration**: Headless mode with public address binding

### Workflow Configuration
- **Run Button**: Executes "Project" workflow
- **Parallel Execution**: Supports multiple workflow tasks
- **Port Management**: Automatically waits for port 5000 availability

## Changelog

```
Changelog:
- June 18, 2025. Initial setup
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```