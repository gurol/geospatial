#!/usr/bin/env python3
"""
GeoJSON File Content Analyzer
=============================

This script analyzes the content of a given GeoJSON file, providing statistics
on the number of features, geometry types, property fields, and their values.
The results are displayed on the screen and also written to a text file in the
same directory as the GeoJSON file.

Usage:
------
Run the script from the command line with the following parameters:

  python geojson_analyzer.py <geojson_file_path> [--exclude <exclude_fields>] [--combination <combination_fields>]

Parameters:
-----------
<geojson_file_path>   : Path to the GeoJSON file to analyze.
--exclude             : (Optional) Comma-separated list of properties to exclude
                        from the analysis. For example: 'id,style,extra.id,extra.name'
--combination         : (Optional) Comma-separated list of field names to
                        combine and count occurrences of their values.
                        For example: 'code,extra.category,extra.type' or 'code, extra.category, extra.type'

Output:
-------
- Number of features in the GeoJSON file.
- Number of features per geometry type.
- Aggregated list of all field names under 'properties' (including excluded fields).
- Count of occurrences of each field under 'properties' (sorted from maximum to minimum).
- Count of occurrences of specified combination of fields under 'properties'
  (if the combination parameter is provided, sorted from maximum to minimum).

The results are written to a text file with the same name as the GeoJSON file
with a '.txt' extension.

Example:
--------
  python geojson_analyzer.py /path/to/your/file.geojson --exclude 'id,style,extra.id,extra.name' --combination 'code, extra.category, extra.room-type'

Author:
-------
Gürol Canbek, https://github.com/gurol/geospatial
Version: 1.0, July 2024
"""

import json
import argparse
import os
from collections import defaultdict, Counter
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
# from shapely import topology

def parse_arguments():
    parser = argparse.ArgumentParser(description='Analyze GeoJSON file.')
    parser.add_argument('geojson_path', type=str, help='Path to the GeoJSON file')
    parser.add_argument('--exclude', type=str, help="Comma separated list of properties to exclude (e.g., --exclude 'id,style,extra.id,extra.name,extra.name'')")
    parser.add_argument('--combination', type=str, help="Comma separated list of field names to combine and count (e.g., --combination 'code, extra.category, extra.room-type')")
    return parser.parse_args()

def nested_field_names(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(nested_field_names(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def calculate_statistics(values):
    if not values:
        return {'mean': None, 'median': None, 'std': None}
    return {
        'mean': np.mean(values),
        'median': np.median(values),
        'std': np.std(values)
    }

def visualize_distribution(data, title, output_file):
    if not data:
        print(f"No data to visualize for {title}.")
        return

    labels, counts = zip(*data.items()) if data else ([], [])
    
    # Convert counts to numeric type and labels to string type
    try:
        counts = [float(count) for count in counts]
        labels = [str(label) for label in labels]
    except ValueError as e:
        print(f"Error processing data for {title}: {e}")
        return

    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts)
    plt.title(title)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

def make_hashable(value):
    if isinstance(value, list):
        return tuple(make_hashable(v) for v in value)
    elif isinstance(value, dict):
        return tuple((k, make_hashable(v)) for k, v in sorted(value.items()))
    else:
        return value
    
def analyze_geojson(file_path, exclude_fields=None, combination_fields=None):
    if exclude_fields is None:
        exclude_fields = []
    try:
        with open(file_path, 'r') as f:
            geojson_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading GeoJSON file: {e}")
        return None, None, None, None, None, None, None, None
    
    feature_count = 0
    geometry_counts = defaultdict(int)
    property_field_names = set()
    property_field_value_counts = defaultdict(Counter)
    combination_counts = Counter()
    numeric_values = defaultdict(list)
    geometries = []

    for feature in geojson_data.get('features', []):
        feature_count += 1
        geometry = feature.get('geometry', None)
        if geometry:
            try:
                geom = shape(geometry)
                if geom.is_valid:
                    geometry_counts[geometry['type']] += 1
                    geometries.append(geom)
            except Exception as e:
                print(f"Error processing geometry: {e}")
        
        properties = feature.get('properties', {})
        nested_properties = nested_field_names(properties)
        
        for field, value in nested_properties.items():
            # Aggregate field names and count values
            property_field_names.add(field)
            if not any(field.startswith(exclude_field) for exclude_field in exclude_fields):
                hashable_value = make_hashable(value)
                property_field_value_counts[field][hashable_value] += 1
                if isinstance(value, (int, float)):
                    numeric_values[field].append(value)
        
        if combination_fields:
            # Count combinations
            combination_key = tuple(nested_properties.get(field, None) for field in combination_fields)
            combination_counts[combination_key] += 1

    bounding_box = None
    centroid = None
    
    # Handle invalid geometries gracefully
    if geometries:
        try:
            union_geom = unary_union(geometries)
            if union_geom.is_valid:
                bounding_box = union_geom.bounds  # tuple representing bounding box
                centroid = union_geom.centroid  # Shapely geometry object for centroid
        except TopologicalError as e:  # Updated exception class
            print(f"Error with unary_union operation: {e}")
        except Exception as e:
            print(f"Unexpected error during geometry union or centroid calculation: {e}")
    
    return geojson_data, feature_count, geometry_counts, sorted(property_field_names), property_field_value_counts, combination_counts, numeric_values, bounding_box, centroid

def write_output(file_path, feature_count, geometry_count, field_names, field_value_count, combination_count, combination_fields, numeric_statistics, bounding_box, centroid):
    base_path, _ = os.path.splitext(file_path)
    output_file = f"{base_path}.txt"
    
    with open(output_file, 'w') as f:
        f.write(f"Number of features: {feature_count}\n")
        f.write("Number of features per geometry type:\n")
        for geom_type, count in geometry_count.items():
            f.write(f"  {geom_type}: {count}\n")
        f.write("Aggregated list of all field names under 'properties':\n")
        for field in field_names:
            f.write(f"  {field}\n")
        f.write("Count of occurrences of each field under 'properties':\n")
        for field, value_count in field_value_count.items():
            value_str = format_value_counts(value_count)
            f.write(f"  {field}: {value_str}\n")
        
        if combination_fields:
            f.write(f"Count of occurrences of '{', '.join(combination_fields)}' fields under 'properties':\n")
            sorted_combinations = sorted(combination_count.items(), key=lambda x: (-x[1], x[0]))
            for combination, count in sorted_combinations:
                f.write(f"  {', '.join(map(str, combination))} ({count})\n")

        f.write("Numeric field statistics:\n")
        for field, stats in numeric_statistics.items():
            f.write(f"  {field}: mean={stats['mean']}, median={stats['median']}, std={stats['std']}\n")

        if bounding_box:
            f.write(f"Bounding Box: {bounding_box}\n")  # bounding_box is a tuple
        if centroid:
            f.write(f"Centroid: {mapping(centroid)}\n")  # centroid is a Shapely geometry object
    
    return output_file

def format_value_counts(value_counts):
    sorted_values = sorted(value_counts.items(), key=lambda x: (-x[1], str(x[0]) if x[0] is not None else ""))
    value_str = ', '.join(f"{value} ({count})" for value, count in sorted_values)
    return value_str

def main():
    args = parse_arguments()
    
    file_path = args.geojson_path
    exclude_fields = args.exclude.split(',') if args.exclude else []
    exclude_fields = [field.strip() for field in exclude_fields]

    combination_fields = args.combination.split(',') if args.combination else []
    combination_fields = [field.strip() for field in combination_fields]

    geojson_data, feature_count, geometry_counts, field_names, field_value_counts, combination_counts, numeric_values, bounding_box, centroid = analyze_geojson(file_path, exclude_fields, combination_fields)
    
    if feature_count is None:
        print("Failed to analyze the GeoJSON file.")
        return
    
    print(f"Number of features: {feature_count}")
    print("Number of features per geometry type:")
    for geom_type, count in geometry_counts.items():
        print(f"  {geom_type}: {count}")
    print("Aggregated list of all field names under 'properties':")
    for field in field_names:
        print(f"  {field}")
    print("Count of occurrences of each field under 'properties':")
    for field, value_count in field_value_counts.items():
        value_str = format_value_counts(value_count)
        print(f"  {field}: {value_str}")
    
    if combination_fields:
        print(f"Count of occurrences of '{', '.join(combination_fields)}' fields under 'properties':")
        # Combination counts are sorted from maximum to minimum
        sorted_combinations = sorted(combination_counts.items(), key=lambda x: (-x[1], x[0]))
        for combination, count in sorted_combinations:
            print(f"  {', '.join(map(str, combination))} ({count})")

    numeric_statistics = {field: calculate_statistics(values) for field, values in numeric_values.items()}

    output_file = write_output(file_path, feature_count, geometry_counts, field_names, field_value_counts, combination_counts, combination_fields, numeric_statistics, bounding_box, centroid)
    
    print(f"Output written to {output_file}")

    visualize_distribution(geometry_counts, 'Geometry Type Distribution', f"{os.path.splitext(output_file)[0]}_geometry_distribution.png")
    for field, value_counts in field_value_counts.items():
        visualize_distribution(value_counts, f'{field} Value Distribution', f"{os.path.splitext(output_file)[0]}_{field}_value_distribution.png")

if __name__ == "__main__":
    main()
