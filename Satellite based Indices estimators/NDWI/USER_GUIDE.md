# NDWI Analysis Tool - User Guide

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

The NDWI (Normalized Difference Water Index) Analysis Tool is designed to process Sentinel-2 satellite imagery using Google Earth Engine to calculate and analyze water content and moisture stress in vegetation and landscapes. The tool handles temporal data gaps, cloud cover, and provides comprehensive visualization of results.

### Key Features
- Automated NDWI calculation from Sentinel-2 imagery
- Cloud cover filtering and quality control
- Temporal gap filling using advanced interpolation
- Time series visualization with cloud cover analysis
- Statistical analysis and reporting
- Data export in multiple formats

## Repository Structure

```
ndwi_analysis/
├── config.json                 # Configuration settings
├── requirements.txt           # Python dependencies
├── ndwi_analysis.py          # Main analysis script
├── sample_field_germany.geojson # Sample field geometry
├── README.md                 # Basic repository information
├── USER_GUIDE.md            # This comprehensive guide
├── LICENSE                  # MIT License
└── output/                 # Generated results
    ├── ndwi_results_*.csv     # NDWI values and statistics
    ├── ndwi_timeseries_*.png  # Visualization plots
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
   cd ndwi-analysis
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
    "scale_meters": 10,             # Output resolution in meters (10m for Sentinel-2 Green/NIR)
    "max_pixels": 1e9,             # Maximum pixels per image
    "output_directory": "output"    # Results directory
}
```

### Parameter Details
- `cloud_cover_threshold`: Lower values mean stricter filtering (range: 0-100)
- `chunk_size_days`: Smaller chunks mean more precise processing but slower execution
- `scale_meters`: Set to 10m to match Sentinel-2 Green and NIR band resolution

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
  - B3 (Green)
  - B8 (NIR)
- Resolution: 10m for both bands

## Running the Analysis

### Basic Usage
```bash
python ndwi_analysis.py
```

### Advanced Usage
```python
from ndwi_analysis import NDWIAnalyzer

analyzer = NDWIAnalyzer('custom_config.json')
results = analyzer.run_analysis(
    'field.geojson',
    '2023-01-01',
    '2023-12-31'
)
```

## Understanding the Output

### 1. CSV Results (`ndwi_results_*.csv`)
- Contains daily NDWI values and statistics
- Columns:
  - `date`: Observation date
  - `NDWI_mean`: Average NDWI value
  - `NDWI_min`: Minimum NDWI value
  - `NDWI_max`: Maximum NDWI value
  - `NDWI_stdDev`: Standard deviation
  - `cloud_cover`: Cloud coverage percentage
  - `is_interpolated`: Flag for interpolated values

### 2. Time Series Plot (`ndwi_timeseries_*.png`)
- Visual representation of NDWI values over time
- Features:
  - Upper plot:
    - Blue line: Mean NDWI values
    - Shaded area: Confidence interval (±1 StdDev)
    - Red/Green lines: Min/Max NDWI values
    - Points: Actual observations and interpolated values
  - Lower plot:
    - Bar chart: Cloud cover percentage
    - Value labels for each observation

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
- NDWI value range validation (-1 to 1)
- Statistical validation
- Temporal consistency checks

## Advanced Usage

### Custom Analysis

```python
analyzer = NDWIAnalyzer()

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

3. **NDWI Calculation**
   - Band selection (Green and NIR)
   - Index computation: (Green - NIR)/(Green + NIR)
   - Statistical reduction

4. **Post-processing**
   - Gap filling
   - Interpolation
   - Quality control

5. **Output Generation**
   - Data export
   - Enhanced visualization
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
   - Validate NDWI ranges

2. **Processing**
   - Use consistent time periods
   - Monitor interpolation quality
   - Review cloud cover statistics
   - Validate results against ground truth

3. **Interpretation**
   - NDWI values typically range from -1 to 1
   - Higher positive values indicate higher water content
   - Lower negative values suggest drier conditions
   - Consider seasonal patterns
   - Account for land cover type

### NDWI Value Interpretation

| NDWI Range | Interpretation |
|------------|---------------|
| > 0.3      | Open water or very high moisture content |
| 0.0 to 0.3 | High vegetation water content |
| -0.1 to 0.0| Moderate vegetation water content |
| -0.3 to -0.1| Low vegetation water content |
| < -0.3     | Very dry vegetation or bare soil |

## References

1. Sentinel-2 User Handbook
2. Google Earth Engine Documentation
3. Scientific papers on NDWI applications in vegetation and water monitoring
4. McFeeters, S.K. (1996) The use of Normalized Difference Water Index (NDWI) in the delineation of open water features 