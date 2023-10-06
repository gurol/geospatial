# geospatial
Geospatial utilities (AutoCAD, DWG/DXF, GeoJSON, ...)

Sure, I'll provide an explanation for the code and the output table to include in your README.md.
- dwgversion.py
- analyzedxf.py

## DXF File Analyzer (analyzedxf.py)

### Overview

This Python script, `analyzedxf.py`, is designed to analyze DXF (Drawing Exchange Format) files, a common file format used for CAD (Computer-Aided Design) drawings. It provides insights into the composition of the DXF file, including the number of different entity types (e.g., lines, circles, text) and blocks present on each layer. The script generates a detailed summary of these statistics and saves it to a text file.

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

The script produces a tab-separated text file (`.txt`) containing a summary of the DXF file's composition. The output includes the following columns:

- **Layer Name**: The name of each layer within the DXF file.
- **Total**: The total count of entities on the layer.
- **POINT, LINE, POLYLINE, LWPOLYLINE, ARC, CIRCLE, ELLIPSE, SPLINE, TEXT, MTEXT, HATCH, DIMENSION**: Counts of specific entity types on the layer.
- **Other types**: Counts of entity types that do not fall into the predefined categories. Unique entity types are counted individually.
- **INSERT**: Counts of INSERT entities, which represent blocks that have been inserted into the drawing.
- **BLOCKS**: Lists the names of blocks present on the layer and their counts.

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
