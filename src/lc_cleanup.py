#!/usr/bin/env python3
"""
Land Cover CSV Cleanup Script

Takes land cover csv files from existing City Scan tabular output and cleans up:
- Column A: Land Cover Type
- Column B: Pixel Count (with apostrophes to remove)

and also calculates and adds columns for total pixels and percentage of each land cover type, returning a clean land cover csv file, lc.csv.
"""

import pandas as pd
import sys

def clean_land_cover_csv(input_file, output_file=None):
    """
    clean up the land cover csv file.
    
    parameters:
    -----------
    input_file : str
        Path to the input csv file
    output_file : str, optional
        Path for output.
    """
    
    # read tabular output csv - no headers, so add them
    df = pd.read_csv(input_file, header=None, names=['land_cover_type', 'pixel_count'])
    
    # remove the apostrophes from "pixel_count" and convert to numeric
    df['pixel_count'] = df['pixel_count'].astype(str).str.replace("'", "").astype(float).astype(int)
    
    # calculate "total_pixels" and "percentage"
    total_pixels = df['pixel_count'].sum()
    df['percentage'] = round((df['pixel_count'] / total_pixels) * 100, 2)
    
    # create output filename if not provided
    if output_file is None:
        output_file = 'lc.csv' # renames output file to lc.csv
            
    # save the cleaned data
    df.to_csv(output_file, index=False)
    
    print(f"Cleaned data saved to: {output_file}")
    print(f"Total pixels: {total_pixels:,}")
    print(f"Number of land cover types: {len(df)}")
    
    return df

# Command line usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lc_cleanup.py input_file.csv [output_file.csv]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    clean_land_cover_csv(input_file, output_file)