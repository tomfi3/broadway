# Airly Indoor Air Quality Monitor

## Overview

This is a Streamlit-based web application for monitoring and visualizing indoor air quality data from Airly sensors. The application provides real-time analysis of particulate matter (PM1, PM2.5, PM10) measurements with comparison against WHO guidelines. It focuses on monitoring 4 Broadway Market sensor locations in Wandsworth (BM1-BM4).

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web framework for rapid prototyping and data visualization
- **Authentication**: Simple password-based access control with session management
- **Visualization**: Plotly Express and Plotly Graph Objects for interactive charts and graphs
- **Layout**: Wide layout configuration optimized for dashboard-style data presentation
- **Caching**: Streamlit's @st.cache_data decorator for performance optimization

### Backend Architecture
- **Language**: Python
- **Data Processing**: Pandas for data manipulation and analysis
- **Mathematical Operations**: NumPy for numerical computations
- **File System**: Local CSV file reading with OS path validation

## Key Components

### Data Layer
- **Data Source**: CSV file containing Airly sensor measurements
- **Data Format**: Time-series data with From/Till timestamps and PM measurements
- **File Location**: `attached_assets/Airly_Report_London_Borough_of_Wandsworth_2025_07_07_10_35_27_1751881436832.csv`

### Processing Layer
- **Data Loading**: Cached data loading function with error handling
- **Time Processing**: DateTime parsing and time component extraction for pattern analysis
- **Sensor Mapping**: Dictionary-based mapping of sensor IDs to human-readable location names

### Visualization Layer
- **Chart Types**: Interactive plots using Plotly for time-series and comparative analysis
- **Health Guidelines**: WHO air quality standards integration for health assessment
- **Multi-location Support**: Support for 4 Broadway Market sensor locations (BM1-BM4) in Wandsworth

## Data Flow

1. **Data Ingestion**: CSV file is loaded from the attached_assets directory
2. **Data Processing**: Timestamps are parsed and time components extracted
3. **Data Validation**: File existence and data format validation
4. **Sensor Mapping**: Sensor IDs are mapped to readable location names
5. **Visualization**: Processed data is rendered through Streamlit interface with Plotly charts
6. **Health Assessment**: Measurements are compared against WHO guidelines

## Security Features
- **Password Protection**: SHA-256 hashed password authentication
- **Environment Variable Security**: Password stored in APP_PASSWORD environment variable (not in source code)
- **Session Management**: Streamlit session state for login persistence
- **Logout Functionality**: Complete session clearing on logout
- **Fallback Password**: "mertonair" (only used if environment variable not set)

## External Dependencies

### Python Packages
- `streamlit`: Web application framework
- `pandas`: Data manipulation and analysis
- `plotly`: Interactive visualization library
- `numpy`: Numerical computing
- `hashlib`: Password hashing for authentication
- `os`: Operating system interface

### Data Dependencies
- Airly sensor CSV export file
- WHO air quality guidelines (hardcoded reference values)

## Deployment Strategy

### Local Development
- Standard Python environment with pip-installed dependencies
- Direct execution via `streamlit run app.py`
- Local file system access for CSV data

### Production Considerations
- Streamlit Cloud or similar platform deployment
- Environment variable configuration for file paths
- Data file upload mechanism for new reports
- Potential database integration for persistent storage

## User Preferences

Preferred communication style: Simple, everyday language.

## Changelog

Changelog:
- July 07, 2025. Initial setup
- July 07, 2025. Added password authentication system with environment variable security (APP_PASSWORD)