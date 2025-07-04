# SAVI Analysis Tool

This tool performs Soil Adjusted Vegetation Index (SAVI) analysis using Google Earth Engine and Sentinel-2 satellite imagery.

## Developer
**Muhammad Arslan**

## Features

- Calculates SAVI for specified field geometries
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

## SAVI Formula and Background

The Soil Adjusted Vegetation Index (SAVI) is calculated using the following formula:

SAVI = ((NIR - RED) * (1 + L)) / (NIR + RED + L)

Where:
- NIR = Near-infrared reflectance (Sentinel-2 Band 8)
- RED = Red reflectance (Sentinel-2 Band 4)
- L = Soil brightness correction factor (typically 0.5)

### Scaling and Interpretation

#### Data Scaling
- Raw Sentinel-2 bands are scaled from 0 to 10000
- Bands are normalized to 0-1 scale by dividing by 10000 before SAVI calculation
- This scaling ensures proper SAVI value ranges and comparability with scientific literature

#### SAVI Value Ranges
- Theoretical range: -1 to +1
- Typical ranges for different vegetation conditions:
  * > 0.5: Dense, healthy vegetation
  * 0.2 - 0.5: Moderate vegetation cover
  * 0.1 - 0.2: Sparse vegetation
  * < 0.1: Very sparse vegetation or bare soil
  * < 0: Water or non-vegetated surfaces

#### Interpretation Guidelines
- Higher values indicate greater vegetation density and health
- Values are less sensitive to soil background than NDVI
- Soil brightness factor (L) adjusts for soil influence:
  * L = 0.5 (default): Works well for most vegetation densities
  * L = 1.0: Areas with very low vegetation cover
  * L = 0.25: Areas with higher vegetation cover

Reference:
Huete, A.R. (1988). A soil-adjusted vegetation index (SAVI). Remote Sensing of Environment, 25(3), 295-309.
https://doi.org/10.1016/0034-4257(88)90106-X

## Requirements

- Python 3.x
- Google Earth Engine account
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd savi-analysis
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
python savi_analysis.py
```

### Setting Time Span for Analysis

In the Python script (savi_analysis.py), locate the time configuration section at the end of the file and modify the following parameters according to your needs:

```python
start_date = '2023-04-01'  # Format: YYYY-MM-DD
end_date = '2023-09-30'    # Format: YYYY-MM-DD
```

## Configuration

Edit `config.json` to customize:
- Cloud cover threshold
- Processing chunk size
- Output resolution
- Soil brightness factor
- Output directory

## Output Structure

The tool generates an `output` folder containing three main components:

### 1. Visualizations
- Time series plots of SAVI values
- Trend analysis graphs
- Spatial distribution maps
- Cloud cover statistics

### 2. Results
- `savi_values.csv`: Contains daily SAVI calculations
- `summary_statistics.csv`: Statistical analysis of SAVI values
- `quality_metrics.csv`: Data quality indicators

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
