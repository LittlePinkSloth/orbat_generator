# 🪖 Orbat Generator

**Orbat Generator** is a Python application that automatically generates a PowerPoint presentation showing the structure of a military organization (ORBAT — Order of Battle). The hierarchy and equipment are extracted from an Excel spreadsheet, CSV mappings, and a set of graphical symbols.

## 🗂 Project Structure

```
.
├── main.py                   # Main entry point
├── datas/                   
│   ├── EquipmentType.csv     # Equipment categories
│   ├── datas.xls             # Source data (units & hierarchy)
│   ├── sidc.csv              # NATO SIDC symbol mapping
│   └── SYMB_PNG/             # Pictograms used for unit symbols                           
├── orbat_gen/
│   ├── __init__.py           # Initializes the package
│   ├── config.py             # Configurations des constantes
│   ├── classes.py            # Defines Unit and EqType classes
│   ├── units_gen.py          # Builds Unit objects from Excel
│   └── powerpoint_gen.py     # Handles PowerPoint slide generation
```

## ▶️ Run the app

```bash
python main.py
```

This will generate a `.pptx` presentation with one or more slides depending on the hierarchy in `datas.xls`.

## 🔧 Key Features

- Excel parsing with military hierarchy.
- Creation of `Unit` objects with linked equipment and subordinates.
- Automated PowerPoint slide generation including:
  - NATO symbols (via PNG).
  - Equipment tables per unit.
  - Hierarchical diagrams ("peignes").

## 📁 Data sources

- `datas.xls`: units' hierarchy and equipment.
- `EquipmentType.csv`: equipment categories.
- `sidc.csv`: NATO symbol codes.
- `SYMB_PNG/`: image files for unit types.

## ✅ Requirements

- `pandas`
- `python-pptx`

Install them using:

```bash
pip install pandas python-pptx
```