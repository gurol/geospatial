# Geospatial Utilities
Geospatial utilities (AutoCAD, DWG/DXF, GeoJSON, ...)
- `dwgversion.py`
- `analyzedxf.py`
- `geojson_analyzer.py` and `geojson_folder_analyzer.py`

## DXF File Analyzer (`analyzedxf.py`)

### Overview

This Python script, `analyzedxf.py`, is designed to analyze [DXF (Drawing Exchange Format)](https://www.adobe.com/creativecloud/file-types/image/vector/dxf-file.html) files, a common file format used for CAD (Computer-Aided Design) drawings. It provides insights into the composition of the DXF file, including the number of different entity types (e.g., lines, circles, text) and blocks present on each layer. The script generates a detailed summary of these statistics and saves it to a text file.

### Usage

Before running the script, ensure you have Python installed on your system. The script relies on the `ezdxf` library, which can be installed via pip:

```
pip install ezdxf
```

To analyze a DXF file, run the script from the command line with the path to the DXF file as an argument:

```
python analyzedxf.py path_to_dxf_file.dxf
```

### Output

The script produces a tab-separated text file (`.txt`) containing a DXF file composition summary. The output includes the following columns:

- **Layer Name**: The name of each layer within the DXF file.
- **Total**: The total count of entities on the layer.
- **POINT, LINE, POLYLINE, LWPOLYLINE, ARC, CIRCLE, ELLIPSE, SPLINE, TEXT, MTEXT, HATCH, DIMENSION**: Counts of specific entity types on the layer.
- **Other types**: Counts of entity types that do not fall into the predefined categories. Unique entity types are counted individually.
- **INSERT**: Counts of INSERT entities, which represent blocks inserted into the drawing.
- **BLOCKS**: Lists the names of blocks on the layer and their counts.

Layers are listed in descending order of entity count, from the highest to the lowest.

### Constraints

- The provided file must be in DXF format for the script to work correctly.
- The script assumes that layers are used to organize entities within the DXF file. Entity counts are tabulated per layer.
- Entity types are categorized into predefined groups, but the script also identifies and counts unique entity types under "Other types."
- The script is primarily designed for analyzing CAD drawings, so its utility may be limited for other types of DXF files.

### Example Output

Here's an example of the output produced by the script:

```
Layer Name  Total   POINT   LINE    POLYLINE    LWPOLYLINE  ARC CIRCLE  ELLIPSE SPLINE  TEXT    MTEXT   HATCH   DIMENSION   Other types INSERT  BLOCKS
FIXTURES    783     0       10      0           34          10  0       0       0       0       2       2       0           725 *U522, *U189, *U515, *U581, *U541, *U198, *U518, *U517, *U203, *U209, *U210, *U199, *U200, *U201, *U202, *U205, *U440, *U441, *U204, *U674, *U206, *U219, XREF2$0
BORDER      593     0       445     0           102         0   0       0       0       0       40      6       0           0
LABELS      422     0       0       0           0           0   0       0       0       422     0       0       0           0
DIMS        241     0       0       0           0           0   0       0       0       0       0       0       241         0
ROOMS       240     0       172     0           45          0   6       0       0       0       8       0       4           SOLID: 2, LEADER: 3    0
FIXT        16      0       0       0           0           0   1       0       0       10      4       0       0           MULTILEADER: 1  0
```

This table provides a breakdown of entity types and block counts on different layers within the DXF file, offering valuable insights into its composition.

## GeoJSON File and Folder Analyzer (`geojson_analyzer.py` and `geojson_folder_analyzer`)

### geojson_analyzer.py

#### Overview
`geojson_analyzer.py` is a comprehensive Python script designed to analyze the content of a GeoJSON file. It provides detailed statistics on the number of features, geometry types, property fields, and their values. The script can output the results both to the console and a text file in the same directory as the input GeoJSON file.

#### Features 
- **Feature Count:**  Calculates the total number of features in the GeoJSON file.
- **Geometry Types:**  Provides a count of features per geometry type (e.g., Point, LineString, Polygon).
- **Property Fields Analysis:**  
  - Aggregates and lists all field names under the `properties` section, including nested fields.
  - Counts occurrences of each field value, sorted from maximum to minimum frequency.
- **Combination Analysis:**  Allows counting occurrences of combinations of specified fields under `properties`.
- **Statistical Analysis:**  Computes basic statistics (mean, median, standard deviation) for numeric fields.
- **Geospatial Analysis:** 
  - Calculates the bounding box and centroid of all geometries.
- **Visualization:**  Generates bar charts for the distribution of geometry types and property values.

#### Usage 
```sh
python geojson_analyzer.py <geojson_file_path> [--exclude <exclude_fields>] [--combination <combination_fields>]
```

**Parameters:**  
- `<geojson_file_path>`: Path to the GeoJSON file to analyze.
- `--exclude`: *(Optional)* Comma-separated list of properties to exclude from the analysis (e.g., `'id,style,extra.id'`).
- `--combination`: *(Optional)* Comma-separated list of field names to combine and count occurrences (e.g., `'code,extra.category'`).

**Example:** 
```sh
python geojson_analyzer.py /path/to/your/file.geojson --exclude 'id,style,extra.id' --combination 'code, extra.category'
```

#### Output 
- Text file with detailed analysis saved in the same directory as the input GeoJSON file.
- Console output summarizing the analysis.
- Visualization images saved as PNG files in the same directory.

---

### geojson_folder_analyzer.py

#### Overview
`geojson_folder_analyzer.py` is a Python script that analyzes all GeoJSON files within a specified folder. It aggregates statistics across all files and generates a comprehensive CSV report. This utility is ideal for batch processing and comparing multiple GeoJSON datasets.

#### Features 
- **Batch Processing:**  Analyzes all GeoJSON files in a given directory. 
- **Feature Count:**  Reports the number of features per file.
- **Geometry Types:**  Counts the number of features per geometry type for each file.
- **Property Fields Analysis:** 
  - Counts occurrences of specified field values across all files.
  - Supports sorting of CSV columns based on the average number of occurrences.
- **Geospatial Summary:** 
  - Calculates combined bounding box and centroid for all geometries across files.
- **CSV Customization:** 
  - Allows specifying a custom delimiter for the output CSV file.
  - Optionally appends the name of the dumped field to the CSV filename.

#### Usage 
```sh
python geojson_folder_analyzer.py <folder_path> [--exclude <exclude_fields>] [--dump <dump_field>] [--delimiter <csv_delimiter>]
```

**Parameters:**  
- `<folder_path>`: Path to the folder containing GeoJSON files to analyze. 
- `--exclude`: *(Optional)* Comma-separated list of properties to exclude (e.g., `'id,style,extra.id'`).
- `--dump`: *(Optional)* Field name to count occurrences under `properties` (e.g., `'typeCode'`).
- `--delimiter`: *(Optional)* Delimiter for the CSV file. The default is comma `,`.

**Example:** 
```sh
python geojson_folder_analyzer.py /path/to/your/folder --exclude 'id,style,extra.id' --dump 'code' --delimiter ';'
```

#### Output 
- CSV file named after the folder (and dumped field if specified), containing:
  - Feature counts per file.
  - Geometry-type feature counts per file.
  - Counts of occurrences of the specified field, sorted by average occurrences across all files.
- Console output summarizing the process and any combined geospatial information.

---

### Note
Both scripts require Python 3 and the following Python libraries: 
- `argparse`
- `json`
- `os`
- `collections` (`defaultdict`, `Counter`)
- `csv` *`csv` (for `geojson_folder_analyzer.py`)*
- `numpy` *`numpy` (for statistical calculations in `geojson_analyzer.py`)*
- `matplotlib` *`matplotlib` (for generating charts in `geojson_analyzer.py`)*
- `shapely` *(for geospatial calculations)*

**Installation of Required Libraries:** You can install the required libraries using `pip`:

```sh
pip install numpy matplotlib shapely
```
