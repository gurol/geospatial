"""
analyzedxf.py - A Python script for analyzing DXF (Drawing Exchange Format) files.

Author: Gürol Canbek
Date: 24 August 2023
Version: 1.0

Description:
This script analyzes a DXF file, providing a summary of the entities per layer, including common entity types and block information. The results are displayed on the console and saved to a tab-separated text file.

Usage:
python analyzedxf.py <path_to_dxf_file>

Example:
python analyzedxf.py path/to/your/dxf/file.dxf

Note:
- Make sure you have Python installed.
- This script expects a valid DXF file as input.
- It counts and categorizes entities by layer, including INSERT entities (blocks).
- The script shows the counts for "Other types".
- The output includes total counts, entity types, and block information for each layer.

For more information and updates, visit the GitHub repository:
https://github.com/gurol/geospatial


License:
CC BY-NC 4.0.
This script is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. See the LICENSE file for details.
"""

import sys
import ezdxf

def analyze_dxf(file_path):
    try:
        doc = ezdxf.readfile(file_path)
        
        layer_entities = {}  # Dictionary to store entity counts per layer
        total_entities = {}  # Dictionary to store total entity counts per layer
        
        for entity in doc.modelspace().query('*'):  # Loop through all entities in the modelspace
            layer_name = entity.dxf.layer
            entity_type = entity.dxftype()
            
            if layer_name not in layer_entities:
                layer_entities[layer_name] = {
                    'POINT': 0, 'LINE': 0, 'POLYLINE': 0, 'LWPOLYLINE': 0,
                    'ARC': 0, 'CIRCLE': 0, 'ELLIPSE': 0, 'SPLINE': 0,
                    'TEXT': 0, 'MTEXT': 0, 'HATCH': 0, 'DIMENSION': 0, 'Other types': {}, 'INSERT': 0, 'BLOCKS': []
                }
                total_entities[layer_name] = 0
            
            if entity_type in layer_entities[layer_name]:
                if entity_type == 'BLOCK':
                    layer_entities[layer_name][entity_type].append(f"{entity.dxf.name}: 1")
                elif entity_type == 'INSERT':
                    block_name = entity.dxf.name
                    if block_name not in layer_entities[layer_name]['BLOCKS']:
                        layer_entities[layer_name]['BLOCKS'].append(block_name)
                    layer_entities[layer_name][entity_type] += 1
                else:
                    layer_entities[layer_name][entity_type] += 1
                total_entities[layer_name] += 1
            else:
                # Here, we use a dictionary to count unique entity types
                if entity_type in layer_entities[layer_name]['Other types']:
                    layer_entities[layer_name]['Other types'][entity_type] += 1
                else:
                    layer_entities[layer_name]['Other types'][entity_type] = 1
                total_entities[layer_name] += 1
        
        return {'layer_entities': layer_entities, 'total_entities': total_entities}

    except Exception as e:
        return str(e)

def display_and_save_results(results, file_path):
    data = results['layer_entities']
    total_entities = results['total_entities']
    
    sorted_layers = sorted(total_entities, key=total_entities.get, reverse=True)
    
    output_filename = file_path.replace('.dxf', '.txt')
    
    with open(output_filename, 'w') as output_file:
        output_file.write("Layer Name\tTotal\tPOINT\tLINE\tPOLYLINE\tLWPOLYLINE\tARC\tCIRCLE\tELLIPSE\tSPLINE\tTEXT\tMTEXT\tHATCH\tDIMENSION\tOther types\tINSERT\tBLOCKS\n")
        print("Layer Name\tTotal\tPOINT\tLINE\tPOLYLINE\tLWPOLYLINE\tARC\tCIRCLE\tELLIPSE\tSPLINE\tTEXT\tMTEXT\tHATCH\tDIMENSION\tOther types\tINSERT\tBLOCKS")
        for layer in sorted_layers:
            output_file.write(layer + "\t" + str(total_entities[layer]) + "\t")
            print(layer, total_entities[layer], end="\t")
            for entity_type, count in data[layer].items():
                if entity_type in ('INSERT', 'DIMENSION'):
                    output_file.write(f"{count}\t")
                    print(count, end="\t")
                elif entity_type == 'BLOCKS':
                    blocks_info = ", ".join(count)
                    output_file.write(blocks_info + "\t")
                    print(blocks_info, end="\t")
                elif entity_type == 'Other types':
                    # Create a string of unique entity types and their counts
                    unique_types = ", ".join([f"{entity}: {count}" for entity, count in count.items()])
                    output_file.write(unique_types + "\t")
                    print(unique_types, end="\t")
                else:
                    output_file.write(str(count) + "\t")
                    print(count, end="\t")
            output_file.write("\n")
            print()

if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].lower().endswith(".dxf"):
        print("Usage: python analyzedxf.py <path_to_dxf_file.dxf>")
        print("Please provide a valid DXF file as a parameter.")
    else:
        dxf_file_path = sys.argv[1]
        print("Analyzing DXF...")
        results, total_results = analyze_dxf(dxf_file_path)
        display_and_save_results(results, total_results, dxf_file_path)
        print("DXF File Analyzer by Gürol Canbek")
