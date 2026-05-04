import sys
import os
import rasterio
import numpy as np
import csv

def normalize_elevation_data(file_path):
    dataset = rasterio.open(file_path)
    elevation_data = dataset.read(1)
    min_elevation = np.min(elevation_data)
    max_elevation = np.max(elevation_data)
    normalized_data = (elevation_data - min_elevation) / (max_elevation - min_elevation)
    return normalized_data

def write_normalized_data_to_csv(normalized_data, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in normalized_data:
            writer.writerow(row)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python converter.py <file_name>")
        sys.exit(1)

    file_name = sys.argv[1]
    input_dir = 'elevation_tifs'
    output_dir = 'elevation_csvs'

    input_file_path = os.path.join(input_dir, file_name)
    output_file_path = os.path.join(output_dir, file_name.replace('.tif', '.csv'))

    normalized_data = normalize_elevation_data(input_file_path)
    write_normalized_data_to_csv(normalized_data, output_file_path)