# WinFi Router Dashboard

## Overview

This is a Streamlit-based web application that simulates a WiFi router dashboard. The application provides a user-friendly interface for monitoring and managing connected devices on a WiFi network. It displays real-time device information including signal strength, bandwidth usage, and connection details across different WiFi bands (2.4GHz, 5GHz, and 6GHz).

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit - chosen for rapid development and built-in web interface capabilities
- **Visualization**: Plotly for interactive charts and graphs
- **Data Processing**: Pandas for device data manipulation
- **Layout**: Wide layout with expandable sidebar for controls

### Backend Architecture
- **Application Type**: Single-page web application with real-time updates
- **State Management**: Streamlit session state for maintaining device information between interactions
- **Data Simulation**: Mock data generation for device metrics and network statistics
- **Real-time Updates**: Simulated signal fluctuations and bandwidth changes

## Key Components

### Device Management System
- Device data structure includes: ID, name, IP, MAC address, WiFi band, priority, status, signal strength, bandwidth, and connection time
- Support for three WiFi bands: 2.4GHz, 5GHz, and 6GHz
- Priority levels: High, Medium, Low
- Enable/disable functionality for individual devices

### Data Visualization
- Real-time signal strength monitoring
- Bandwidth usage tracking
- Device connection statistics
- Interactive charts using Plotly

### User Interface
- Clean, modern dashboard design
- Router-themed branding (WiNFi v2.0)
- Responsive layout for different screen sizes
- Intuitive controls for device management

## Data Flow

1. **Initialization**: Application starts with empty device list in session state
2. **Device Generation**: Mock devices are created with randomized but realistic network parameters
3. **Real-time Updates**: Device metrics (signal strength, bandwidth) are periodically updated with simulated fluctuations
4. **User Interactions**: Users can view, add, remove, and modify device settings through the web interface
5. **State Persistence**: All changes are maintained in session state throughout the user session

## External Dependencies

### Core Dependencies
- **Streamlit (>=1.46.0)**: Web application framework for the dashboard interface
- **Pandas (>=2.3.0)**: Data manipulation and analysis for device information
- **Plotly (>=6.1.2)**: Interactive visualization library for charts and graphs

### Additional Libraries
- **Altair**: Alternative visualization library (auto-installed with Streamlit)
- **Blinker**: Signal/event handling for Streamlit
- **Cachetools**: Caching utilities for performance optimization

## Deployment Strategy

### Replit Configuration
- **Runtime**: Python 3.11 environment
- **Deployment Target**: Autoscale deployment for handling variable traffic
- **Port Configuration**: Application runs on port 5000
- **Process Management**: Streamlit server with custom configuration

### Server Configuration
- Headless server mode for production deployment
- Configured to accept connections from any address (0.0.0.0)
- Custom port binding for Replit environment compatibility

### Workflow Automation
- Parallel workflow execution
- Automated Streamlit server startup
- Port monitoring for service availability

## Changelog
- June 20, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.