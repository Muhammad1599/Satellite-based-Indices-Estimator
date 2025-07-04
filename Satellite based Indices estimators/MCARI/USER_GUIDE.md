# MCARI Analysis Tool - User Guide

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

The MCARI (Modified Chlorophyll Absorption Ratio Index) Analysis Tool is designed to process Sentinel-2 satellite imagery using Google Earth Engine to calculate and analyze vegetation indices for agricultural fields. MCARI is particularly effective for assessing chlorophyll content and early stress detection in vegetation. The tool handles temporal data gaps, cloud cover, and provides comprehensive visualization of results.

### Key Features
- Automated MCARI calculation from Sentinel-2 imagery
- Cloud cover filtering and quality control
- Temporal gap filling using advanced interpolation
- Time series visualization with cloud cover analysis
- Statistical analysis and reporting
- Data export in multiple formats

## Repository Structure

```
mcari_analysis/
├── config.json                 # Configuration settings
├── requirements.txt           # Python dependencies
├── mcari_analysis.py         # Main analysis script
├── sample_field_germany.geojson # Sample field geometry
├── README.md                 # Basic repository information
├── USER_GUIDE.md            # This comprehensive guide
├── LICENSE                  # MIT License
└── output/                 # Generated results
    ├── mcari_results_*.csv     # MCARI values and statistics
    ├── mcari_timeseries_*.png  # Visualization plots
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
   cd mcari-analysis
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
    "output_directory": "output"    # Results directory
}
```

### Parameter Details
- `cloud_cover_threshold`: Lower values mean stricter filtering (range: 0-100)
- `chunk_size_days`: Smaller chunks mean more precise processing but slower execution
- `scale_meters`: Matches Sentinel-2 resolution (10m, 20m, or 30m)

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
  - B4 (Red)
  - B5 (Red Edge)
- Resolution: 
  - Green (B3): 10m
  - Red (B4): 10m
  - Red Edge (B5): 20m (resampled based on configuration)

## Running the Analysis

### Basic Usage
```bash
python mcari_analysis.py
```

### Advanced Usage
```python
from mcari_analysis import MCARIAnalyzer

analyzer = MCARIAnalyzer('custom_config.json')
results = analyzer.run_analysis(
    'field.geojson',
    '2023-01-01',
    '2023-12-31'
)
```

## Understanding the Output

### 1. CSV Results (`mcari_results_*.csv`)
- Contains daily MCARI values and statistics
- Columns:
  - `date`: Observation date
  - `MCARI_mean`: Average MCARI value
  - `MCARI_min`: Minimum MCARI value
  - `MCARI_max`: Maximum MCARI value
  - `MCARI_stdDev`: Standard deviation
  - `cloud_cover`: Cloud coverage percentage
  - `is_interpolated`: Flag for interpolated values

### 2. Time Series Plot (`mcari_timeseries_*.png`)
- Visual representation of MCARI values over time
- Features:
  - Upper plot:
    - Blue line: Mean MCARI values
    - Shaded area: Confidence interval (±1 StdDev)
    - Red/Green lines: Min/Max MCARI values
    - Points: Actual observations and interpolated values
  - Lower plot:
    - Bar chart: Cloud cover percentage
    - Value labels for each observation

### 3. Metadata (`analysis_metadata_*.json`)
- Analysis configuration and summary
- Quality control information
- Processing statistics
- Timestamp and version information

### MCARI Value Interpretation

| MCARI Range | Interpretation |
|------------|---------------|
| > 0.6      | Very high chlorophyll content, healthy vegetation |
| 0.4 - 0.6  | Good chlorophyll content |
| 0.2 - 0.4  | Moderate chlorophyll content |
| 0.1 - 0.2  | Low chlorophyll content, possible stress |
| < 0.1      | Very low chlorophyll content or non-vegetated |

### Understanding MCARI
- MCARI is sensitive to chlorophyll content variations
- Less affected by atmospheric and soil background effects
- Useful for:
  * Early stress detection
  * Chlorophyll content estimation
  * Crop health monitoring
  * Nitrogen deficiency assessment

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
- MCARI value range validation
- Statistical validation
- Temporal consistency checks

## Advanced Usage

### Custom Analysis

```python
analyzer = MCARIAnalyzer()

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

3. **MCARI Calculation**
   - Band selection (Green, Red, Red Edge)
   - Index computation
   - Statistical reduction

4. **Post-processing**
   - Gap filling
   - Interpolation
   - Quality control

5. **Output Generation**
   - Data export
   - Enhanced visualization
   - Metadata creation

### Best Practices

1. **Data Quality**
   - Verify field boundaries
   - Check for seasonal variations
   - Monitor cloud cover impact
   - Validate MCARI ranges

2. **Processing**
   - Use consistent time periods
   - Monitor interpolation quality
   - Review cloud cover statistics
   - Validate results against ground truth

3. **Interpretation**
   - Consider growth stage
   - Account for crop type
   - Compare with historical data
   - Validate with field measurements

### Seasonal Considerations

1. **Growing Season**
   - Higher MCARI values expected
   - More reliable measurements
   - Better for stress detection

2. **Off Season**
   - Lower values normal
   - Higher uncertainty
   - Consider soil effects

### Validation Methods

1. **Ground Truth**
   - Chlorophyll meter readings
   - Leaf sampling
   - Visual inspection

2. **Cross-Validation**
   - Compare with other indices
   - Historical data analysis
   - Statistical validation

## References

1. Sentinel-2 User Handbook
2. Google Earth Engine Documentation
3. Scientific papers on MCARI applications in agriculture
4. Daughtry, C.S.T., et al. (2000) - Original MCARI development
5. Wu, C., et al. (2008) - MCARI applications in agriculture 