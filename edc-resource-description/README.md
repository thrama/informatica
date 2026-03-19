# EDC Lineage Formatter

Python script to generate formatted textual descriptions of data lineage from **Informatica Enterprise Data Catalog (EDC)** CSV/Excel exports.

Designed to produce output ready for copy-pasting into EDC asset description fields, giving data stewards a clear, human-readable view of upstream data sources.

---

## Output Format

```
To Object: TargetResource / TargetSchema / TargetTable / TargetColumn

From Object:
- SourceResource / SourceDB / SourceSchema
  ├ SourceTable1 (COL_A, COL_B, COL_C)
  ├ SourceTable2 (COL_D, COL_E)
  └ SourceTable3 (COL_F)

------------------------------------------------------------
```

- Sources are grouped by **destination object**, then by **resource / database / schema**
- Tables are listed with all their contributing columns in alphabetical order — no truncation
- Tree-style connectors (`├` / `└`) for visual clarity
- When source paths have 4 parts (resource/db/schema/table/column), the database is included in the grouping key

---

## Requirements

- Python 3.8+
- `pandas`
- `openpyxl` (required for Excel input files)

Install dependencies:

```bash
pip install pandas openpyxl
```

---

## Usage

```bash
# Basic usage with a CSV file
python edc_lineage_formatter.py lineage_export.csv

# Specify a custom output file
python edc_lineage_formatter.py lineage_export.csv -o lineage_description.txt

# With an Excel file
python edc_lineage_formatter.py lineage_export.xlsx -o lineage_description.txt

# Control how many lines are shown in the terminal preview (default: 50)
python edc_lineage_formatter.py lineage_export.csv --preview-lines 100
```

---

## Parameters

| Parameter         | Description                                          |
| ----------------- | ---------------------------------------------------- |
| `input_file`      | CSV or Excel file with lineage data (required)       |
| `-o, --output`    | Output file path (default: `<input>_formatted.txt`)  |
| `--preview-lines` | Lines to display in terminal preview (default: `50`) |

---

## Input Format

The input file must contain the columns **`From Object`** and **`To Object`**, with EDC paths in the format:

```
Resource://Instance/Schema/Table/Column
```

Supported path formats (by number of segments after `://`):

| Segments | Interpreted as                     |
| -------- | ---------------------------------- |
| 4        | Instance / Schema / Table / Column |
| 3        | Schema / Table / Column            |
| 2        | Schema / Table                     |
| 1        | Schema only                        |

### Example CSV

```csv
Association,From Connection,To Connection,From Object,To Object
core.DirectionalDataFlow,,,SourceDB://INST01/SCHEMA_A/TABLE_001/COL_01,TargetDB://SCHEMA_B/TABLE_OUT/COL_OUT
core.DirectionalDataFlow,,,SourceDB://INST01/SCHEMA_A/TABLE_001/COL_02,TargetDB://SCHEMA_B/TABLE_OUT/COL_OUT
core.DirectionalDataFlow,,,SourceDB://INST01/SCHEMA_A/TABLE_002/COL_03,TargetDB://SCHEMA_B/TABLE_OUT/COL_OUT
```

---

## Changelog

| Version | Date       | Notes                                                             |
| ------- | ---------- | ----------------------------------------------------------------- |
| 1.1.0   | 2025-06-01 | Fixed source grouping for 4-part paths; removed column truncation |
| 1.0.0   | 2025-05-01 | Initial release                                                   |

---

## License

Apache License 2.0 — see [LICENSE](../LICENSE) for details.

---

## Author

**Lorenzo Lombardi**
[linkedin.com/in/lorenzolombardi](https://www.linkedin.com/in/lorenzolombardi/) · [github.com/thrama](https://github.com/thrama)
