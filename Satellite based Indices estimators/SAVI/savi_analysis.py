import ee
import geojson
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import logging
import os
import json
from pathlib import Path
import numpy as np
from typing import Dict, List, Optional, Tuple
from scipy.interpolate import CubicSpline
from scipy.sparse import csc_matrix, eye, diags
from scipy.sparse.linalg import spsolve

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('savi_analysis.log'),
        logging.StreamHandler()
    ]
)

def whittaker_smooth(x: np.ndarray, w: np.ndarray, lambda_: float = 100.0) -> np.ndarray:
    """
    Apply Whittaker smoothing to data with missing values.
    
    Args:
        x: Input data with possible NaN values
        w: Weights (0 for missing values, 1 for valid values)
        lambda_: Smoothing parameter (higher values = smoother result)
    
    Returns:
        Smoothed data array
    """
    n = len(x)
    D = diags([1, -2, 1], [0, -1, -2], shape=(n+2, n))
    W = diags(w)
    A = W + lambda_ * D.T.dot(D)
    z = spsolve(A.tocsc(), w*x)
    return z

def fill_gaps(df: pd.DataFrame, max_gap_days: int = 32) -> pd.DataFrame:
    """
    Fill temporal gaps in SAVI time series using a combination of
    Whittaker smoothing and spline interpolation.
    
    Args:
        df: Input DataFrame with date and SAVI columns
        max_gap_days: Maximum gap size to fill (default 32 days)
    
    Returns:
        DataFrame with filled gaps
    """
    if df.empty:
        return df
        
    # Sort by date and ensure date column is datetime
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Create a complete date range
    date_range = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='D')
    
    # Create a template DataFrame with all dates
    template_df = pd.DataFrame({'date': date_range})
    
    # Merge with actual data
    merged_df = template_df.merge(df, on='date', how='left')
    
    # Only fill gaps smaller than max_gap_days
    gaps = merged_df['SAVI_mean'].isnull()
    
    if not gaps.any():
        return merged_df
    
    # Find gap sizes
    gap_groups = gaps.ne(gaps.shift()).cumsum()
    gap_sizes = gaps.groupby(gap_groups).transform('size') * gaps
    
    # Create weights array (0 for gaps we want to fill, 1 for actual data)
    weights = (~gaps).astype(float)
    
    # Mark gaps that are too large with weight 0
    weights[gap_sizes > max_gap_days] = 0
    
    # Apply Whittaker smoothing to mean SAVI
    x = merged_df['SAVI_mean'].fillna(merged_df['SAVI_mean'].mean()).values
    smoothed_savi = whittaker_smooth(x, weights)
    
    # Use spline interpolation for final adjustments
    valid_idx = ~merged_df['SAVI_mean'].isnull()
    if valid_idx.sum() > 3:  # Need at least 4 points for cubic spline
        spline = CubicSpline(
            np.arange(len(merged_df))[valid_idx],
            merged_df['SAVI_mean'][valid_idx],
            bc_type='natural'
        )
        # Blend smoothed and spline results
        alpha = 0.7  # Weight for smoothed values
        merged_df.loc[merged_df['SAVI_mean'].isnull(), 'SAVI_mean'] = \
            alpha * smoothed_savi[merged_df['SAVI_mean'].isnull()] + \
            (1 - alpha) * spline(np.arange(len(merged_df))[merged_df['SAVI_mean'].isnull()])
    else:
        # If too few points, use only Whittaker smoothing
        merged_df.loc[merged_df['SAVI_mean'].isnull(), 'SAVI_mean'] = \
            smoothed_savi[merged_df['SAVI_mean'].isnull()]
    
    # Interpolate other columns
    for col in ['SAVI_min', 'SAVI_max', 'SAVI_stdDev']:
        if col in merged_df.columns:
            merged_df[col] = merged_df[col].interpolate(
                method='cubic',
                limit_direction='both',
                limit=max_gap_days
            )
    
    # Mark interpolated values
    merged_df['is_interpolated'] = gaps
    
    # Remove gaps that are too large
    merged_df = merged_df[gap_sizes <= max_gap_days]
    
    return merged_df

class ConfigurationError(Exception):
    """Custom exception for configuration errors"""
    pass

class SAVIAnalyzer:
    """Class to handle SAVI analysis operations"""
    
    def __init__(self, config_path: str = 'config.json'):
        """Initialize the analyzer with configuration"""
        self.config = self._load_config(config_path)
        self.output_dir = Path(self.config.get('output_directory', 'output'))
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize Earth Engine
        self._initialize_gee()
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file or use defaults"""
        default_config = {
            'cloud_cover_threshold': 30,
            'chunk_size_days': 15,
            'scale_meters': 30,
            'max_pixels': 1e9,
            'output_directory': 'output',
            'soil_brightness_factor': 0.5
        }
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults, keeping user values
                    return {**default_config, **config}
            else:
                logging.warning(f"Config file {config_path} not found. Using defaults.")
                return default_config
        except json.JSONDecodeError as e:
            raise ConfigurationError(f"Error parsing config file: {e}")

    def _initialize_gee(self):
        """Initialize Google Earth Engine with error handling"""
        try:
            ee.Initialize(project='ee-muhammad15')
        except Exception as e:
            logging.info("Initial initialization failed, attempting authentication...")
            try:
                ee.Authenticate()
                ee.Initialize(project='ee-muhammad15')
            except Exception as auth_error:
                raise ConfigurationError(f"Failed to initialize Earth Engine: {auth_error}")

    def load_geometry(self, geojson_path: str) -> ee.Geometry:
        """Load and validate field geometry from GeoJSON file"""
        try:
            with open(geojson_path, 'r') as f:
                geojson_data = geojson.load(f)
            
            # Validate GeoJSON structure
            if 'features' not in geojson_data or not geojson_data['features']:
                raise ValueError("Invalid GeoJSON: No features found")
            
            coords = geojson_data['features'][0]['geometry']['coordinates']
            return ee.Geometry.Polygon(coords)
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            raise ConfigurationError(f"Error loading geometry file: {e}")

    def calculate_savi(self, image):
        """Calculate SAVI for a single image with input validation"""
        try:
            L = self.config['soil_brightness_factor']
            
            # Select bands and normalize to 0-1 scale (Sentinel-2 data is in 0-10000 scale)
            NIR = image.select('B8').divide(10000)  # NIR band
            RED = image.select('B4').divide(10000)  # Red band
            
            # Calculate SAVI: ((NIR - RED) * (1 + L)) / (NIR + RED + L)
            savi = NIR.subtract(RED).multiply(1 + L).divide(NIR.add(RED).add(L))
            
            return savi.rename('SAVI')
        except Exception as e:
            logging.error(f"Error calculating SAVI: {e}")
            raise

    def process_date_chunk(self, geometry: ee.Geometry, start_date: str, end_date: str) -> List[Dict]:
        """Process a chunk of dates with quality checks"""
        try:
            # Get Sentinel-2 collection
            s2_collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
                .filterDate(start_date, end_date) \
                .filterBounds(geometry) \
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', self.config['cloud_cover_threshold']))
            
            # Verify we have images
            image_count = s2_collection.size().getInfo()
            if image_count == 0:
                logging.warning(f"No valid images found for period {start_date} to {end_date}")
                return []
            
            def process_image(image):
                # Calculate SAVI
                savi = self.calculate_savi(image)
                
                # Calculate statistics
                stats = savi.reduceRegion(
                    reducer=ee.Reducer.mean().combine(
                        ee.Reducer.stdDev(), '', True
                    ).combine(
                        ee.Reducer.min(), '', True
                    ).combine(
                        ee.Reducer.max(), '', True
                    ),
                    geometry=geometry,
                    scale=self.config['scale_meters'],
                    maxPixels=self.config['max_pixels']
                )
                
                # Get the date
                date = image.date().format('YYYY-MM-dd')
                
                # Return a feature with properties
                return ee.Feature(None, {
                    'date': date,
                    'SAVI_mean': stats.get('SAVI_mean'),
                    'SAVI_stdDev': stats.get('SAVI_stdDev'),
                    'SAVI_min': stats.get('SAVI_min'),
                    'SAVI_max': stats.get('SAVI_max'),
                    'cloud_cover': image.get('CLOUDY_PIXEL_PERCENTAGE')
                })
            
            # Process all images
            features = s2_collection.map(process_image).getInfo()['features']
            
            # Extract properties
            results = []
            for feature in features:
                if feature['properties']['SAVI_mean'] is not None:
                    results.append(feature['properties'])
            
            return results
            
        except Exception as e:
            logging.error(f"Error processing chunk {start_date} to {end_date}: {e}")
            return []

    def plot_time_series(self, df: pd.DataFrame, output_file: str):
        """Create enhanced time series visualization"""
        if df.empty:
            logging.warning("No data to plot")
            return
            
        # Create two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), height_ratios=[3, 1])
        
        # Convert date strings to datetime if needed
        if not pd.api.types.is_datetime64_any_dtype(df['date']):
            df['date'] = pd.to_datetime(df['date'])
        
        # Sort by date
        df = df.sort_values('date')
        
        # Plot SAVI values
        # Plot interpolated values with different style
        if 'is_interpolated' in df.columns:
            # Plot actual observations
            actual = df[~df['is_interpolated']]
            interp = df[df['is_interpolated']]
            
            # Plot actual data
            ax1.plot(actual['date'], actual['SAVI_mean'], 'b-', 
                    label='Mean SAVI (Observed)', linewidth=2, alpha=0.7)
            ax1.scatter(actual['date'], actual['SAVI_mean'], 
                       color='blue', s=100, zorder=5, label='Observation')
            
            # Plot interpolated data
            if not interp.empty:
                ax1.plot(interp['date'], interp['SAVI_mean'], 'b--', 
                        label='Mean SAVI (Interpolated)', linewidth=1, alpha=0.5)
                ax1.scatter(interp['date'], interp['SAVI_mean'], 
                          color='lightblue', s=50, zorder=4, 
                          label='Interpolated', alpha=0.5)
        else:
            # Original plotting code for non-interpolated data
            ax1.plot(df['date'], df['SAVI_mean'], 'b-', 
                    label='Mean SAVI', linewidth=2, alpha=0.7)
            ax1.scatter(df['date'], df['SAVI_mean'], 
                       color='blue', s=100, zorder=5, label='Observation')
        
        # Add error bands
        ax1.fill_between(df['date'], 
                        df['SAVI_mean'] - df['SAVI_stdDev'],
                        df['SAVI_mean'] + df['SAVI_stdDev'],
                        alpha=0.2, color='blue', label='±1 StdDev')
        
        # Add min/max as points with connecting lines
        ax1.plot(df['date'], df['SAVI_min'], 'r--', alpha=0.5, linewidth=1, label='Min SAVI')
        ax1.plot(df['date'], df['SAVI_max'], 'g--', alpha=0.5, linewidth=1, label='Max SAVI')
        ax1.scatter(df['date'], df['SAVI_min'], color='red', s=50, alpha=0.5, zorder=4)
        ax1.scatter(df['date'], df['SAVI_max'], color='green', s=50, alpha=0.5, zorder=4)
        
        # Add count of observations
        obs_count = (~df['is_interpolated']).sum() if 'is_interpolated' in df.columns else len(df)
        interp_count = df['is_interpolated'].sum() if 'is_interpolated' in df.columns else 0
        
        stats_text = f'Total Points: {len(df)}\n'
        stats_text += f'Observations: {obs_count}\n'
        if interp_count > 0:
            stats_text += f'Interpolated: {interp_count}'
        
        ax1.text(0.02, 0.98, stats_text,
                transform=ax1.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # Customize first subplot
        ax1.set_title('SAVI Time Series Analysis', pad=20, fontsize=14)
        ax1.set_ylabel('SAVI Value', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        
        # Set y-axis limits with some padding
        ymin = df['SAVI_min'].min() - 0.1
        ymax = df['SAVI_max'].max() + 0.1
        ax1.set_ylim(ymin, ymax)
        
        # Plot cloud cover (only for actual observations)
        if 'is_interpolated' in df.columns:
            actual_data = df[~df['is_interpolated']]
        else:
            actual_data = df
            
        bars = ax2.bar(actual_data['date'], actual_data['cloud_cover'], 
                      alpha=0.5, color='gray', label='Cloud Cover %')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom', rotation=0,
                    fontsize=8)
        
        ax2.set_ylabel('Cloud Cover %', fontsize=12)
        ax2.set_xlabel('Date', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        
        # Set better date formatting for x-axis
        for ax in [ax1, ax2]:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Save the plot with high DPI
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()

    def validate_results(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Validate results and return quality flags"""
        if df.empty:
            return False, ["No valid data found"]
            
        issues = []
        
        # Check for missing values
        if df.isnull().any().any():
            issues.append("Missing values detected in the data")
        
        # Convert date column to datetime if it's not already
        df['date'] = pd.to_datetime(df['date'])
        
        # Check for unrealistic SAVI values (typically between -1 and 1)
        if (df['SAVI_mean'] > 2).any() or (df['SAVI_mean'] < -1).any():
            issues.append("Unrealistic SAVI values detected")
        
        # Check for sufficient temporal coverage
        date_range = (df['date'].max() - df['date'].min()).days
        if date_range < 30:
            issues.append(f"Short temporal coverage: {date_range} days")
        
        # Check for large gaps in time series
        df_sorted = df.sort_values('date')
        gaps = df_sorted['date'].diff().dt.days
        if (gaps > 30).any():
            issues.append("Large temporal gaps detected (>30 days)")
        
        return len(issues) == 0, issues

    def run_analysis(self, geojson_path: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Run the complete analysis pipeline"""
        try:
            # Create timestamp for this run
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Load geometry
            logging.info("Loading field geometry...")
            geometry = self.load_geometry(geojson_path)
            
            # Process in chunks
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            chunk_size = timedelta(days=self.config['chunk_size_days'])
            
            all_results = []
            current_start = start
            
            logging.info("Processing data in chunks...")
            while current_start < end:
                current_end = min(current_start + chunk_size, end)
                logging.info(f"Processing {current_start.strftime('%Y-%m-%d')} to {current_end.strftime('%Y-%m-%d')}...")
                
                chunk_results = self.process_date_chunk(
                    geometry,
                    current_start.strftime('%Y-%m-%d'),
                    current_end.strftime('%Y-%m-%d')
                )
                all_results.extend(chunk_results)
                current_start = current_end
            
            # Convert to DataFrame
            df = pd.DataFrame(all_results)
            
            if df.empty:
                logging.warning("No valid data found for the entire period")
                return df
            
            # Fill gaps in the time series
            logging.info("Filling temporal gaps...")
            df_filled = fill_gaps(df)
            
            # Validate results
            is_valid, issues = self.validate_results(df_filled)
            if not is_valid:
                for issue in issues:
                    logging.warning(f"Quality issue detected: {issue}")
            
            # Save results
            csv_file = self.output_dir / f'savi_results_{timestamp}.csv'
            plot_file = self.output_dir / f'savi_timeseries_{timestamp}.png'
            
            df_filled.to_csv(csv_file, index=False)
            self.plot_time_series(df_filled, str(plot_file))
            
            # Save analysis metadata
            metadata = {
                'timestamp': timestamp,
                'start_date': start_date,
                'end_date': end_date,
                'config': self.config,
                'quality_issues': issues,
                'total_observations': len(df),
                'interpolated_points': len(df_filled) - len(df),
                'mean_savi': float(df_filled['SAVI_mean'].mean()) if not df_filled.empty else None,
                'mean_cloud_cover': float(df['cloud_cover'].mean()) if not df.empty else None
            }
            
            metadata_file = self.output_dir / f'analysis_metadata_{timestamp}.json'
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logging.info(f"Analysis complete. Results saved to {self.output_dir}")
            return df_filled
            
        except Exception as e:
            logging.error(f"Analysis failed: {e}")
            raise

def main():
    """Main execution function"""
    try:
        # Initialize analyzer
        analyzer = SAVIAnalyzer()
        
        # Run analysis for 6 months
        df = analyzer.run_analysis(
            geojson_path='sample_field_germany.geojson',
            start_date='2023-04-01',
            end_date='2023-09-30'
        )
        
        if not df.empty:
            # Display summary
            logging.info("\nAnalysis Summary:")
            logging.info("\n" + str(df.describe()))
        else:
            logging.warning("No valid data found for analysis")
        
    except Exception as e:
        logging.error(f"Error in main execution: {e}")
        raise

if __name__ == '__main__':
    main() 