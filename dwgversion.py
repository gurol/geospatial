"""
dwgversion.py - A Python script for parsing the version of a DWG file.

Author: Gürol Canbek
Date: 24 August 2023
Version: 1.0

Description:
This script parses the version of a DWG (Drawing) file and prints it to the console.
It supports various DWG versions from early releases to more recent ones.

Usage:
python dwgversion.py <path_to_dwg_file>

Example:
python dwgversion.py path/to/your/dwg/file.dwg

Note:
- Make sure you have Python installed.
- This script reads the first 20 bytes of the DWG file to determine its version.
- It provides human-readable versions for known DWG releases.
- If the DWG version is unknown or the file cannot be read, it will display "Unknown."

For more information, visit the GitHub repository:
https://github.com/gurol/geospatial

License:
This script is distributed under the MIT License. See the LICENSE file for details.
"""
def parse_dwg_version(file_path):
    version_map = {
        "MC0.0": "DWG Release 1.1",
        "AC1.2": "DWG Release 1.2",
        "AC1.4": "DWG Release 1.4",
        "AC1.50": "DWG Release 2.0",
        "AC2.10": "DWG Release 2.10",
        "AC1002": "DWG Release 2.5",
        "AC1003": "DWG Release 2.6",
        "AC1004": "DWG Release 9",
        "AC1006": "DWG Release 10",
        "AC1009": "DWG Release 11/12 (LT R1/R2)",
        "AC1012": "DWG Release 13 (LT95)",
        "AC1014": "DWG Release 14, 14.01 (LT97/LT98)",
        "AC1015": "DWG AutoCAD 2000/2000i/2002",
        "AC1018": "DWG AutoCAD 2004/2005/2006",
        "AC1021": "DWG AutoCAD 2007/2008/2009",
        "AC1024": "DWG AutoCAD 2010/2011/2012",
        "AC1027": "DWG AutoCAD 2013/2014/2015/2016/2017",
        "AC1032": "DWG AutoCAD 2018/2019/2020/2021/2022"
    }

    try:
        with open(file_path, 'rb') as file:
            first_bytes = file.read(20)  # Read the first 20 bytes
            first_chars = first_bytes.decode('utf-8', errors='ignore')
            version = first_chars.split('\x00', 1)[0]  # Get characters until first null byte
            if version in version_map:
                return version_map[version]
            else:
                return version.strip() if version.strip() else "Unknown"
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python dwgversion.py <path_to_dwg_file>")
    else:
        dwg_file_path = sys.argv[1]
        version = parse_dwg_version(dwg_file_path)
        print(f"DWG Version: {version}")
