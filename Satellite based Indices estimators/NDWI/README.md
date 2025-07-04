# NDWI Analysis Tool

This tool performs Normalized Difference Water Index (NDWI) analysis using Google Earth Engine and Sentinel-2 satellite imagery.

## Developer
**Muhammad Arslan**

## Features

- Calculates NDWI for specified field geometries
- Processes Sentinel-2 satellite imagery
- Handles cloud cover and data gaps
- Generates time series visualizations
- Provides quality control and validation
- Outputs results in CSV format with metadata

## Sentinel-2 Data Specifications

### Temporal Resolution
- 5-day revisit time at the equator with two satellites combined (Sentinel-2A & 2B)
- Individual satellite revisit: 10 days
- Sentinel-2A launch: June 23, 2015
- Sentinel-2B launch: March 7, 2017
- Data availability: From June 2015 to present

### Spatial Resolution
- 10m: RGB and NIR bands (Bands 2, 3, 4, and 8)
- 20m: Red edge and SWIR bands (Bands 5, 6, 7, 8A, 11, and 12)
- 60m: Atmospheric bands (Bands 1, 9, and 10)

### Coverage
- Global coverage between latitudes 84°N and 56°S
- 290km swath width
- 100x100 km tile size

## NDWI Formula and Background

The Normalized Difference Water Index (NDWI) is calculated using the following formula:

NDWI = (GREEN - NIR) / (GREEN + NIR)

Where:
- GREEN = Green reflectance (Sentinel-2 Band 3)
- NIR = Near-infrared reflectance (Sentinel-2 Band 8)

### Data Scaling and Interpretation

#### Sentinel-2 Data Scaling
- Raw Sentinel-2 bands are scaled from 0 to 10000
- Bands are normalized to 0-1 scale by dividing by 10000 before NDWI calculation
- This scaling ensures proper NDWI value ranges and comparability with scientific literature

#### NDWI Value Ranges
- Theoretical range: -1 to +1
- Typical ranges for different conditions:
  * > 0.3: Open water or very high moisture content
  * 0.0 to 0.3: High vegetation water content
  * -0.1 to 0.0: Moderate vegetation water content
  * -0.3 to -0.1: Low vegetation water content
  * < -0.3: Very dry vegetation or bare soil

#### Interpretation Guidelines
- Higher values indicate higher water content or open water
- Values vary with:
  * Vegetation type and density
  * Seasonal changes
  * Soil moisture conditions
  * Recent precipitation
- Consider local conditions when interpreting values
- Compare with historical data when possible
- Account for environmental factors

Reference: McFeeters, S.K. (1996). The use of the Normalized Difference Water Index (NDWI) in the delineation of open water features. International Journal of Remote Sensing, 17(7), 1425-1432.

## Requirements

- Python 3.x
- Google Earth Engine account
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Muhammad1599/NDWI_time-series-satellite-data-calculator-.git
cd NDWI_time-series-satellite-data-calculator-
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
python ndwi_analysis.py
```

### Setting Time Span for Analysis

In the Python script (ndwi_analysis.py), locate the time configuration section at the end of the file and modify the following parameters according to your needs:

```python
start_date = '2023-04-01'  # Format: YYYY-MM-DD
end_date = '2023-09-30'    # Format: YYYY-MM-DD
```

## Configuration

Edit `config.json` to customize:
- Cloud cover threshold
- Processing chunk size
- Output resolution (10m for both GREEN and NIR bands)
- Output directory

## Output Structure

The tool generates an `output` folder containing three main components:

### 1. Visualizations
- Time series plots of NDWI values with:
  - Mean NDWI trend line
  - Confidence intervals
  - Cloud cover statistics
  - Interpolated values marked
- Cloud cover percentage bar charts

### 2. Results
- `ndwi_results_[timestamp].csv`: Contains daily NDWI calculations with:
  - Date
  - Mean NDWI
  - Min/Max NDWI
  - Standard deviation
  - Cloud cover percentage
  - Interpolation flags

### 3. Metadata
- Processing parameters used
- Data acquisition details:
  - Satellite pass dates
  - Cloud coverage percentages
  - Quality flags
- Field geometry information
- Version information and processing timestamps

## Sample Data

A sample field geometry (`sample_field_germany.geojson`) is provided for testing.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 