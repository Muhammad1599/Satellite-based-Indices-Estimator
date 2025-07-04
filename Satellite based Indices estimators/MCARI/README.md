# MCARI Analysis Tool

This tool performs Modified Chlorophyll Absorption Ratio Index (MCARI) analysis using Google Earth Engine and Sentinel-2 satellite imagery.

## Developer
**Muhammad Arslan**

## Features

- Calculates MCARI for specified field geometries
- Processes Sentinel-2 satellite imagery
- Advanced gap filling using Whittaker smoothing and spline interpolation
- Handles cloud cover and data quality
- Generates enhanced time series visualizations
- Provides comprehensive quality control and validation
- Outputs results in CSV format with detailed metadata

## Sentinel-2 Data Specifications

### Temporal Resolution
- 5-day revisit time at the equator with two satellites combined (Sentinel-2A & 2B)
- Individual satellite revisit: 10 days
- Sentinel-2A launch: June 23, 2015
- Sentinel-2B launch: March 7, 2017
- Data availability: From June 2015 to present

### Spatial Resolution
- 10m: RGB bands (Bands 2, 3, and 4)
- 20m: Red edge bands (Bands 5, 6, 7, and 8A)
- 60m: Atmospheric bands (Bands 1, 9, and 10)

### Coverage
- Global coverage between latitudes 84°N and 56°S
- 290km swath width
- 100x100 km tile size

## MCARI Formula and Background

The Modified Chlorophyll Absorption Ratio Index (MCARI) is calculated using the following formula:

MCARI = [(B5 - B4) - 0.2 * (B5 - B3)] * (B5/B4)

Where:
- B3 = Green reflectance (Sentinel-2 Band 3)
- B4 = Red reflectance (Sentinel-2 Band 4)
- B5 = Red Edge reflectance (Sentinel-2 Band 5)

Reference:
Daughtry, C.S.T., et al. (2000). Estimating Corn Leaf Chlorophyll Concentration from Leaf and Canopy Reflectance. Remote Sensing of Environment, 74(2), 229-239.

### Value Interpretation
- > 0.12: Very high chlorophyll content
- 0.08-0.12: Good chlorophyll content
- 0.04-0.08: Moderate chlorophyll content
- 0.02-0.04: Low chlorophyll content
- < 0.02: Very low chlorophyll or non-vegetated

## Requirements

- Python 3.x
- Google Earth Engine account
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Muhammad1599/MCARI_time-series-satellite-data-calculator-.git
cd MCARI_time-series-satellite-data-calculator
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Authenticate with Google Earth Engine:
```bash
earthengine authenticate
```

## Usage

1. Prepare your field geometry in GeoJSON format
2. Configure analysis parameters in config.json
3. Run the analysis:
```bash
python mcari_analysis.py
```

### Setting Time Span for Analysis

In the Python script (mcari_analysis.py), modify the time configuration in the main() function:

```python
start_date = '2023-04-01'  # Format: YYYY-MM-DD
end_date = '2023-09-30'    # Format: YYYY-MM-DD
```

## Configuration

Edit `config.json` to customize:
```json
{
    "cloud_cover_threshold": 30,
    "chunk_size_days": 15,
    "scale_meters": 30,
    "max_pixels": 1e9,
    "output_directory": "output"
}
```

## Output Structure

The tool generates an `output` folder containing three main components:

### 1. Visualizations (`mcari_timeseries_[timestamp].png`)
- Dual subplot visualization
  - Upper plot: MCARI time series with:
    * Mean MCARI values
    * Standard deviation bands
    * Min/Max indicators
    * Interpolated values marked
  - Lower plot: Cloud cover percentage

### 2. Results (`mcari_results_[timestamp].csv`)
- Daily MCARI values including:
  * Mean MCARI
  * Standard deviation
  * Minimum and maximum values
  * Cloud cover percentage
  * Interpolation flags

### 3. Metadata (`analysis_metadata_[timestamp].json`)
- Processing parameters
- Data acquisition details:
  * Satellite pass dates
  * Cloud coverage statistics
  * Quality flags
- Field geometry information
- Statistical summaries
- Version information and timestamps

## Advanced Features

### Gap Filling
- Whittaker smoothing for primary interpolation
- Cubic spline for fine adjustments
- Configurable maximum gap size
- Quality flags for interpolated values

### Quality Control
- Cloud cover filtering
- Unrealistic value detection
- Temporal consistency checks
- Gap size monitoring
- Statistical validation

## Sample Data

A sample field geometry (`sample_field_germany.geojson`) is provided for testing.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 