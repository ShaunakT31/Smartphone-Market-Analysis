"""
pipeline/clean_data.py
-----------------------
Reads all raw JSON files from 'data/raw/', cleans and normalizes them into
structured CSV files stored in 'data/clean/'.

Handles:
- Missing or invalid prices
- Extraction of numeric specs (RAM, storage, battery, camera, display)
- Removal of duplicates and variant noise
"""

import os
import re
import json
import pandas as pd


RAW_PATH = os.path.join("data", "raw")
CLEAN_PATH = os.path.join("data", "clean")
os.makedirs(CLEAN_PATH, exist_ok=True)


def extract_numeric(value, unit):
    """Extracts numeric part from a text string (e.g., '8 GB' -> 8)."""
    if not isinstance(value, str):
        return None
    match = re.search(r"(\d+\.?\d*)\s*" + re.escape(unit), value, flags=re.IGNORECASE)
    return float(match.group(1)) if match else None


def parse_specs(spec_list):
    """
    Converts a list of spec strings into a dictionary with numeric features.
    Expects specs like: ['8 GB RAM', '256 GB Storage', '5000 mAh Battery']
    """
    specs = {}
    for spec in spec_list:
        spec = spec.strip()
        if "ram" in spec.lower():
            specs["ram_gb"] = extract_numeric(spec, "GB")
        elif "storage" in spec.lower() or "rom" in spec.lower():
            specs["storage_gb"] = extract_numeric(spec, "GB")
        elif "battery" in spec.lower() or "mah" in spec.lower():
            specs["battery_mah"] = extract_numeric(spec, "mAh")
        elif "camera" in spec.lower() and "mp" in spec.lower():
            specs["camera_mp"] = extract_numeric(spec, "MP")
        elif "inch" in spec.lower():
            specs["display_inch"] = extract_numeric(spec, "inch")
    return specs


def clean_single_file(filepath):
    """Cleans one raw JSON file and saves a CSV version in data/clean/."""
    brand_name = os.path.splitext(os.path.basename(filepath))[0].replace("_raw", "")
    print(f"Cleaning {brand_name}...")

    with open(filepath, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    df = pd.DataFrame(raw_data)
    if "specs" not in df.columns:
        raise ValueError(f"No 'specs' column found in {filepath}")

    # Expand specs into separate numeric columns
    spec_data = df["specs"].apply(parse_specs).apply(pd.Series)
    df = pd.concat([df, spec_data], axis=1)

    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace(",", "")
        .str.extract(r"(\d+)")
        .astype(float)
    )

    # Drop rows missing price or name
    df = df.dropna(subset=["price", "name"])

    # Remove color variants like “(Blue, 256GB)”
    df["name"] = df["name"].str.replace(r"\(.*?\)", "", regex=True).str.strip()

    clean_path = os.path.join(CLEAN_PATH, f"{brand_name}_clean.csv")
    df.to_csv(clean_path, index=False)
    print(f"✅ Saved: {clean_path} ({len(df)} rows)")

    return df


def clean_all_raw_files():
    """Iterates through all JSONs in data/raw and cleans them."""
    json_files = [f for f in os.listdir(RAW_PATH) if f.endswith(".json")]
    if not json_files:
        print("⚠️ No raw JSON files found in data/raw/")
        return

    all_dfs = []
    for file in json_files:
        df = clean_single_file(os.path.join(RAW_PATH, file))
        all_dfs.append(df)

    print(f"\n✅ Cleaning complete for {len(all_dfs)} files.\n")


if __name__ == "__main__":
    clean_all_raw_files()
