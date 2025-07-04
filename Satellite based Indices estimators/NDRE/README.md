# NDRE Analysis Tool

This tool performs Normalized Difference Red Edge (NDRE) analysis using Google Earth Engine and Sentinel-2 satellite imagery. NDRE is particularly useful for monitoring crop health and nitrogen content in vegetation.

## Developer
**Muhammad Arslan**

## Features

- Calculates NDRE for specified field geometries
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

## NDRE Formula and Background

The Normalized Difference Red Edge (NDRE) index is calculated using the following formula:

NDRE = (NIR - RedEdge) / (NIR + RedEdge)

Where:
- NIR = Near-infrared reflectance (Sentinel-2 Band 8)
- RedEdge = Red Edge reflectance (Sentinel-2 Band 5)

### Data Scaling and Interpretation

#### Sentinel-2 Data Scaling
- Raw Sentinel-2 bands are scaled from 0 to 10000
- Bands are normalized to 0-1 scale by dividing by 10000 before NDRE calculation
- This scaling ensures proper NDRE value ranges and comparability with scientific literature

#### NDRE Value Ranges
- Theoretical range: -1 to +1
- Typical ranges for different vegetation conditions:
  * > 0.4: Very healthy vegetation with high nitrogen content
  * 0.3 - 0.4: Good vegetation health and nitrogen status
  * 0.2 - 0.3: Moderate vegetation health
  * 0.1 - 0.2: Poor vegetation health or possible nitrogen stress
  * < 0.1: Severe stress or non-vegetated surfaces
  * < 0: Water, shadows, or non-vegetated surfaces

#### Interpretation Guidelines
- Higher values indicate better plant health and nitrogen content
- Values vary throughout the growing season
- Consider growth stage when interpreting values
- Local calibration may be needed for specific crops
- Compare with historical data when possible
- Account for environmental conditions

## Requirements

- Python 3.x
- Google Earth Engine account
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ndre-analysis
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
python ndre_analysis.py
```

### Setting Time Span for Analysis

In the Python script (ndre_analysis.py), locate the time configuration section at the end of the file and modify the following parameters according to your needs:

```python
start_date = '2023-04-01'  # Format: YYYY-MM-DD
end_date = '2023-09-30'    # Format: YYYY-MM-DD
```

## Configuration

Edit `config.json` to customize:
- Cloud cover threshold
- Processing chunk size
- Output resolution
- Output directory

## Output Structure

The tool generates an `output` folder containing three main components:

### 1. Visualizations
- Time series plots of NDRE values
- Trend analysis graphs
- Spatial distribution maps
- Cloud cover statistics

### 2. Results
- `ndre_results.csv`: Contains daily NDRE calculations
- `summary_statistics.csv`: Statistical analysis of NDRE values
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

## References

1. Sentinel-2 MSI User Guide - European Space Agency
2. Barnes, E.M., et al. (2000). "Coincident Detection of Crop Water Stress, Nitrogen Status and Canopy Density Using Ground-Based Multispectral Data."
3. Eitel, J.U.H., et al. (2011). "Combined Spectral Index to Improve Ground-Based Estimates of Nitrogen Status in Dryland Wheat." 