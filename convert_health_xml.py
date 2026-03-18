#!/usr/bin/env python3
"""
Apple Health XML → CSV Converter
Converts the FREE Apple Health export (XML) into CSV files
that @neiltron/apple-health-mcp expects.

Usage:
  1. iPhone → Health app → Profile pic (top right) → Export All Health Data
  2. AirDrop the zip to your Mac
  3. Unzip it (double-click)
  4. Run: python3 convert_health_xml.py ~/Downloads/apple_health_export/export.xml

Output: CSV files in the same directory as this script, named like:
  HKQuantityTypeIdentifierStepCount.csv
  HKQuantityTypeIdentifierHeartRate.csv
  HKWorkoutActivityTypeRunning.csv
  etc.
"""

import xml.etree.ElementTree as ET
import csv
import os
import sys
from collections import defaultdict
from datetime import datetime

def convert(xml_path, output_dir=None):
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    print(f"Parsing {xml_path}...")
    print("(This may take a minute for large exports)")

    tree = ET.iterparse(xml_path, events=("end",))

    records = defaultdict(list)
    workouts = defaultdict(list)
    record_count = 0

    for event, elem in tree:
        if elem.tag == "Record":
            rec_type = elem.attrib.get("type", "Unknown")
            row = {
                "type": rec_type,
                "sourceName": elem.attrib.get("sourceName", ""),
                "sourceVersion": elem.attrib.get("sourceVersion", ""),
                "unit": elem.attrib.get("unit", ""),
                "creationDate": elem.attrib.get("creationDate", ""),
                "startDate": elem.attrib.get("startDate", ""),
                "endDate": elem.attrib.get("endDate", ""),
                "value": elem.attrib.get("value", ""),
            }
            records[rec_type].append(row)
            record_count += 1
            if record_count % 100000 == 0:
                print(f"  ...{record_count:,} records processed")
            elem.clear()

        elif elem.tag == "Workout":
            w_type = elem.attrib.get("workoutActivityType", "Unknown")
            row = {
                "workoutActivityType": w_type,
                "duration": elem.attrib.get("duration", ""),
                "durationUnit": elem.attrib.get("durationUnit", ""),
                "totalDistance": elem.attrib.get("totalDistance", ""),
                "totalDistanceUnit": elem.attrib.get("totalDistanceUnit", ""),
                "totalEnergyBurned": elem.attrib.get("totalEnergyBurned", ""),
                "totalEnergyBurnedUnit": elem.attrib.get("totalEnergyBurnedUnit", ""),
                "sourceName": elem.attrib.get("sourceName", ""),
                "creationDate": elem.attrib.get("creationDate", ""),
                "startDate": elem.attrib.get("startDate", ""),
                "endDate": elem.attrib.get("endDate", ""),
            }
            workouts[w_type].append(row)
            elem.clear()

    print(f"\nTotal: {record_count:,} health records + {sum(len(v) for v in workouts.values()):,} workouts")
    print(f"Found {len(records)} record types + {len(workouts)} workout types\n")

    # Write record CSVs
    for rec_type, rows in records.items():
        filename = f"{rec_type}.csv"
        filepath = os.path.join(output_dir, filename)
        if rows:
            with open(filepath, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            print(f"  {filename} ({len(rows):,} rows)")

    # Write workout CSVs
    for w_type, rows in workouts.items():
        filename = f"{w_type}.csv"
        filepath = os.path.join(output_dir, filename)
        if rows:
            with open(filepath, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            print(f"  {filename} ({len(rows):,} rows)")

    total_files = len(records) + len(workouts)
    print(f"\nDone! {total_files} CSV files written to {output_dir}")
    print(f"Set HEALTH_DATA_DIR={output_dir} in your MCP config")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 convert_health_xml.py /path/to/export.xml [output_dir]")
        print("\nHow to get export.xml:")
        print("  iPhone → Health app → Profile pic (top right) → Export All Health Data")
        print("  AirDrop to Mac → Unzip → find export.xml inside")
        sys.exit(1)

    xml_path = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(xml_path):
        print(f"File not found: {xml_path}")
        sys.exit(1)

    convert(xml_path, out_dir)
