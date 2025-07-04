# SAVI Analysis Tool - User Guide

## Table of Contents
1. [Overview](#overview)
2. [Repository Structure](#repository-structure)
3. [Installation Guide](#installation-guide)
4. [Configuration](#configuration)
5. [Data Requirements](#data-requirements)
6. [Running the Analysis](#running-the-analysis)
7. [Understanding the Output](#understanding-the-output)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Usage](#advanced-usage)

## Overview

The SAVI (Soil Adjusted Vegetation Index) Analysis Tool is designed to process Sentinel-2 satellite imagery using Google Earth Engine to calculate and analyze vegetation indices for agricultural fields. The tool handles temporal data gaps, cloud cover, and provides comprehensive visualization of results.

### Key Features
- Automated SAVI calculation from Sentinel-2 imagery
- Cloud cover filtering and quality control
- Temporal gap filling using advanced interpolation
- Time series visualization
- Statistical analysis and reporting
- Data export in multiple formats

## Repository Structure

```
savi_analysis/
├── config.json                 # Configuration settings
├── requirements.txt           # Python dependencies
├── savi_analysis.py          # Main analysis script
├── savi_analysis_organized.py # Organized version of the script
├── sample_field_germany.geojson # Sample field geometry
├── README.md                 # Basic repository information
├── USER_GUIDE.md            # This comprehensive guide
├── LICENSE                  # MIT License
├── .gitignore              # Git ignore rules
└── output/                 # Generated results
    ├── savi_results_*.csv     # SAVI values and statistics
    ├── savi_timeseries_*.png  # Visualization plots
    └── analysis_metadata_*.json # Analysis metadata
```

## Installation Guide

### Prerequisites
- Python 3.x
- Google Earth Engine account
- Git (for version control)

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd savi-analysis
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Google Earth Engine Authentication**
   ```bash
   earthengine authenticate
   ```
   Follow the prompts to complete authentication.

## Configuration

The `config.json` file controls the analysis parameters:

```json
{
    "cloud_cover_threshold": 30,     # Maximum acceptable cloud cover percentage
    "chunk_size_days": 15,          # Days per processing chunk
    "scale_meters": 30,             # Output resolution in meters
    "max_pixels": 1e9,             # Maximum pixels per image
    "output_directory": "output",   # Results directory
    "soil_brightness_factor": 0.5   # SAVI soil brightness parameter
}
```

### Parameter Details
- `cloud_cover_threshold`: Lower values mean stricter filtering (range: 0-100)
- `chunk_size_days`: Smaller chunks mean more precise processing but slower execution
- `scale_meters`: Matches Sentinel-2 resolution (10m, 20m, or 30m)
- `soil_brightness_factor`: Typically 0.5, adjust based on soil conditions

## Data Requirements

### Field Geometry
- Format: GeoJSON
- Required properties:
  - Polygon geometry
  - Valid coordinate system
- Example provided: `sample_field_germany.geojson`

### Satellite Data
- Source: Sentinel-2 (accessed automatically via Google Earth Engine)
- Bands used:
  - B4 (RED)
  - B8 (NIR)
- Resolution: 10m native, resampled based on configuration

## Running the Analysis

### Basic Usage
```bash
python savi_analysis.py
```

### Advanced Usage
```python
from savi_analysis import SAVIAnalyzer

analyzer = SAVIAnalyzer('custom_config.json')
results = analyzer.run_analysis(
    'field.geojson',
    '2023-01-01',
    '2023-12-31'
)
```

## Understanding the Output

### 1. CSV Results (`savi_results_*.csv`)
- Contains daily SAVI values and statistics
- Columns:
  - `date`: Observation date
  - `SAVI_mean`: Average SAVI value
  - `SAVI_min`: Minimum SAVI value
  - `SAVI_max`: Maximum SAVI value
  - `SAVI_stdDev`: Standard deviation
  - `cloud_cover`: Cloud coverage percentage
  - `is_interpolated`: Flag for interpolated values

### 2. Time Series Plot (`savi_timeseries_*.png`)
- Visual representation of SAVI values over time
- Features:
  - Blue line: Mean SAVI values
  - Shaded area: SAVI range (min to max)
  - Red dots: Interpolated values
  - Grid lines for reference
  - Date-formatted x-axis

### 3. Metadata (`analysis_metadata_*.json`)
- Analysis configuration and summary
- Quality control information
- Processing statistics
- Timestamp and version information

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   ```
   Solution: Re-run 'earthengine authenticate'
   ```

2. **Missing Data Periods**
   - Check cloud cover threshold
   - Verify date range
   - Ensure field geometry is valid

3. **Memory Issues**
   - Reduce chunk_size_days
   - Decrease max_pixels
   - Process smaller areas

### Quality Control

The tool performs automatic quality checks:
- Cloud cover filtering
- Gap detection and interpolation
- Outlier identification
- Statistical validation

## Advanced Usage

### Custom Analysis

```python
analyzer = SAVIAnalyzer()

# Custom date range
results = analyzer.run_analysis(
    geojson_path='field.geojson',
    start_date='2023-01-01',
    end_date='2023-12-31'
)

# Custom visualization
analyzer.plot_time_series(
    results,
    'custom_plot.png'
)
```

### Data Processing Pipeline

1. **Initialization**
   - Load configuration
   - Authenticate GEE
   - Validate inputs

2. **Data Collection**
   - Filter Sentinel-2 collection
   - Apply cloud mask
   - Chunk processing

3. **SAVI Calculation**
   - Band selection
   - Index computation
   - Statistical reduction

4. **Post-processing**
   - Gap filling
   - Interpolation
   - Quality control

5. **Output Generation**
   - Data export
   - Visualization
   - Metadata creation

### Performance Optimization

- Use appropriate chunk sizes
- Adjust cloud cover threshold
- Optimize resolution for your needs
- Consider temporal resolution requirements

### Best Practices

1. **Data Quality**
   - Verify field boundaries
   - Check for seasonal variations
   - Monitor cloud cover impact

2. **Processing**
   - Start with sample data
   - Monitor memory usage
   - Keep logs for tracking

3. **Results**
   - Validate outputs
   - Compare with ground truth
   - Document anomalies

## Support and Contribution

For issues, questions, or contributions:
1. Check existing documentation
2. Review closed issues
3. Open new issues with:
   - Configuration used
   - Error messages
   - Sample data (if possible)
   - Expected behavior 