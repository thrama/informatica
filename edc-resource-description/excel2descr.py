#!/usr/bin/env python3
"""
# DATE: 2025-06-01
# VERSION: 1.1.0
# AUTHOR: Lorenzo Lombardi
# LINKEDIN: https://www.linkedin.com/in/lorenzolombardi/
# GITHUB: https://github.com/thrama

EDC Lineage Formatter - Informatica Enterprise Data Catalog
===========================================================
Generates a formatted textual description of data lineage
from a CSV or Excel export file produced by Informatica EDC.

Typical use case: populate the description field of EDC assets
with a human-readable summary of upstream data sources.

Expected input columns: 'From Object', 'To Object'
Path format: Resource://Instance/Schema/Table/Column

Output format example:
  To Object: TargetResource / TargetSchema / TargetTable / TargetColumn

  From Object:
  - SourceResource / SourceSchema
    ├ SourceTable1 (COL_A, COL_B, COL_C)
    ├ SourceTable2 (COL_D)
    └ SourceTable3 (COL_E, COL_F)
"""

import os
import pandas as pd
import argparse
from collections import defaultdict
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if present (silently ignored if missing)
load_dotenv()


def parse_object_path(path: str) -> dict:
    """
    Parse an EDC path in the format: Resource://Instance/Schema/Table/Column
    Returns a dictionary with the individual components.

    Supported formats (by number of path segments after '://'):
      4 parts -> Instance / Schema / Table / Column
      3 parts -> Schema / Table / Column  (no instance)
      2 parts -> Schema / Table
      1 part  -> Schema only

    Examples:
      SourceDB://INST01/SCHEMA_A/TABLE_001/COL_01
        -> resource=SourceDB, instance=INST01, schema=SCHEMA_A,
           table=TABLE_001, column=COL_01

      CustomResource://SCHEMA_B/TABLE_002/COL_02
        -> resource=CustomResource, schema=SCHEMA_B,
           table=TABLE_002, column=COL_02
    """
    if not path or pd.isna(path):
        return None

    try:
        resource_part, object_part = path.split("://", 1)
        parts = object_part.split("/")

        result = {
            "resource": resource_part,
            "full_path": path
        }

        if len(parts) == 4:
            # Instance / Schema / Table / Column
            result["instance"] = parts[0]
            result["schema"] = parts[1]
            result["table"] = parts[2]
            result["column"] = parts[3]
        elif len(parts) == 3:
            # Schema / Table / Column (no instance)
            result["schema"] = parts[0]
            result["table"] = parts[1]
            result["column"] = parts[2]
        elif len(parts) == 2:
            # Schema / Table
            result["schema"] = parts[0]
            result["table"] = parts[1]
        elif len(parts) == 1:
            result["schema"] = parts[0]

        return result

    except Exception:
        return {"resource": path, "full_path": path}


def group_lineage_data(df: pd.DataFrame) -> dict:
    """
    Group lineage rows by destination, then by source resource/db/schema/table.

    Result structure:
      {
        dest_key -> {
          source_key (resource / db / schema) -> {
            table -> [column, ...]
          }
        }
      }

    The source_key includes database when present (4-part paths).
    Tables are grouped under this key, with their contributing columns listed.
    """
    grouped = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for _, row in df.iterrows():
        from_obj = parse_object_path(row.get("From Object", ""))
        to_obj = parse_object_path(row.get("To Object", ""))

        if not from_obj or not to_obj:
            continue

        # ── Destination key ──────────────────────────────────────────────
        if "column" in to_obj:
            dest_key = (
                f"{to_obj['resource']} / {to_obj.get('schema', '')} / "
                f"{to_obj.get('table', '')} / {to_obj.get('column', '')}"
            )
        elif "table" in to_obj:
            dest_key = (
                f"{to_obj['resource']} / {to_obj.get('schema', '')} / "
                f"{to_obj.get('table', '')}"
            )
        else:
            dest_key = to_obj["full_path"]

        # ── Source key: resource / [db /] schema ──────────────────────────
        # Include DB (instance) when present in 4-part paths
        if "instance" in from_obj and from_obj["instance"]:
            source_key = (
                f"{from_obj['resource']} / {from_obj['instance']} / "
                f"{from_obj.get('schema', '')}"
            )
        else:
            source_key = f"{from_obj['resource']} / {from_obj.get('schema', '')}"

        # ── Table and column from source ──────────────────────────────────
        table = from_obj.get("table", "N/A")
        column = from_obj.get("column", "")

        if column and column not in grouped[dest_key][source_key][table]:
            grouped[dest_key][source_key][table].append(column)

    return grouped


def format_lineage_description(grouped_data: dict) -> str:
    """
    Format the grouped lineage data into a human-readable string.

    All columns are always listed in alphabetical order with no truncation,
    regardless of how many columns a table has.
    """
    output_lines = []

    for dest, sources in grouped_data.items():
        output_lines.append(f"To Object: {dest}")
        output_lines.append("")

        for source_key, tables in sources.items():
            output_lines.append(f"From Object:\n- {source_key}")

            table_list = list(tables.items())
            for i, (table, columns) in enumerate(table_list):
                prefix = "  └" if i == len(table_list) - 1 else "  ├"

                if columns:
                    col_str = ", ".join(sorted(columns))
                    output_lines.append(f"{prefix} {table} ({col_str})")
                else:
                    output_lines.append(f"{prefix} {table}")

            output_lines.append("")

        output_lines.append("-" * 60)
        output_lines.append("")

    return "\n".join(output_lines)


def resolve_input_path(filename: str) -> Path:
    """
    Resolve the full input path, prepending EDC_LINEAGE_INPUT_DIR
    from the environment if set and the filename is not already absolute.
    """
    p = Path(filename)
    if not p.is_absolute():
        input_dir = os.getenv("EDC_LINEAGE_INPUT_DIR", "").strip()
        if input_dir:
            p = Path(input_dir) / p
    return p


def resolve_output_path(input_path: Path, output_arg: str | None) -> Path:
    """
    Resolve the output file path.
    Priority: --output CLI arg > EDC_LINEAGE_OUTPUT_DIR env var > same dir as input.
    """
    stem = f"{input_path.stem}_formatted.txt"

    if output_arg:
        return Path(output_arg)

    output_dir = os.getenv("EDC_LINEAGE_OUTPUT_DIR", "").strip()
    if output_dir:
        return Path(output_dir) / stem

    return input_path.with_name(stem)


def main():
    # Read defaults from environment (overridable via CLI)
    default_preview = int(os.getenv("EDC_LINEAGE_PREVIEW_LINES", "50"))

    parser = argparse.ArgumentParser(
        description=(
            "EDC Lineage Formatter - generates formatted textual descriptions "
            "of data lineage from Informatica EDC CSV/Excel exports."
        )
    )
    parser.add_argument(
        "input_file",
        help="CSV or Excel file with 'From Object' and 'To Object' columns"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path (overrides EDC_LINEAGE_OUTPUT_DIR)"
    )
    parser.add_argument(
        "--preview-lines",
        type=int,
        default=default_preview,
        metavar="N",
        help=f"Lines to show in terminal preview (default from env: {default_preview})"
    )

    args = parser.parse_args()

    input_path = resolve_input_path(args.input_file)
    if not input_path.exists():
        print(f"[ERROR] Input file not found: {input_path}")
        raise SystemExit(1)

    # ── Read input ────────────────────────────────────────────────────────
    if input_path.suffix.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(input_path)
    else:
        df = pd.read_csv(input_path, encoding="utf-8-sig")

    print(f"Read {len(df)} rows from {input_path.name}")

    # ── Process ───────────────────────────────────────────────────────────
    grouped = group_lineage_data(df)
    formatted = format_lineage_description(grouped)

    # ── Write output ──────────────────────────────────────────────────────
    output_path = resolve_output_path(input_path, args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(formatted, encoding="utf-8")
    print(f"Output written to: {output_path}")

    # ── Terminal preview ──────────────────────────────────────────────────
    all_lines = formatted.split("\n")
    print(f"\n--- PREVIEW (first {args.preview_lines} lines) ---\n")
    print("\n".join(all_lines[:args.preview_lines]))
    if len(all_lines) > args.preview_lines:
        print(f"\n[... {len(all_lines) - args.preview_lines} more lines ...]")


if __name__ == "__main__":
    main()
