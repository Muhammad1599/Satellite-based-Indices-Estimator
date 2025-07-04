# BSI Analysis Tool

This tool performs Bare Soil Index (BSI) analysis using Google Earth Engine and Sentinel-2 satellite imagery.

## Developer
**Muhammad Arslan**

## Features

- Calculates BSI for specified field geometries
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

## BSI Formula and Background

The Bare Soil Index (BSI) is calculated using the following formula:

BSI = ((SWIR + RED) - (NIR + BLUE)) / ((SWIR + RED) + (NIR + BLUE))

Where:
- SWIR = Short-wave Infrared reflectance (Sentinel-2 Band 11)
- RED = Red reflectance (Sentinel-2 Band 4)
- NIR = Near-infrared reflectance (Sentinel-2 Band 8)
- BLUE = Blue reflectance (Sentinel-2 Band 2)

### Data Scaling and Interpretation

#### Sentinel-2 Data Scaling
- Raw Sentinel-2 bands are scaled from 0 to 10000
- Bands are normalized to 0-1 scale by dividing by 10000 before BSI calculation
- This scaling ensures proper BSI value ranges and comparability with scientific literature

#### BSI Value Ranges
- Theoretical range: -1 to +1
- Typical ranges for different conditions:
  * > 0.3: High bare soil exposure or built-up areas
  * 0.0 to 0.3: Moderate soil exposure or mixed surfaces
  * -0.3 to 0.0: Low soil exposure, moderate vegetation
  * < -0.3: Dense vegetation or water bodies

#### Interpretation Guidelines
- Higher values indicate more exposed soil or built-up areas
- Values vary with:
  * Soil type and moisture content
  * Vegetation cover
  * Urban development
  * Seasonal changes
- Consider local conditions when interpreting values
- Compare with historical data when possible
- Account for environmental factors

Reference: Chen, X., et al. (2004). Remote sensing of urban environments. Progress in Physical Geography, 28(2), 283-302.

## Requirements

- Python 3.x
- Google Earth Engine account
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/BSI_time-series-satellite-data-calculator.git
cd BSI_time-series-satellite-data-calculator
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
python bsi_analysis.py
```

### Setting Time Span for Analysis

In the Python script (bsi_analysis.py), locate the time configuration section at the end of the file and modify the following parameters according to your needs:

```python
start_date = '2023-04-01'  # Format: YYYY-MM-DD
end_date = '2023-09-30'    # Format: YYYY-MM-DD
```

## Configuration

Edit `config.json` to customize:
- Cloud cover threshold
- Processing chunk size
- Output resolution (20m due to SWIR band resolution)
- Output directory

## Output Structure

The tool generates an `output` folder containing three main components:

### 1. Visualizations
- Time series plots of BSI values with:
  - Mean BSI trend line
  - Confidence intervals
  - Cloud cover statistics
  - Interpolated values marked
- Cloud cover percentage bar charts

### 2. Results
- `bsi_results_[timestamp].csv`: Contains daily BSI calculations with:
  - Date
  - Mean BSI
  - Min/Max BSI
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