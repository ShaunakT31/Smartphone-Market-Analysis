"""
pipeline/combine_data.py
-------------------------
Combines all cleaned brand CSV files from 'data/clean/' into a single
master dataset stored in 'data/processed/all_brands_20k.csv'.

Adds a 'brand' column, standardizes brand names, removes duplicates,
and prepares the data for analysis.
"""

import os
import pandas as pd


CLEAN_PATH = os.path.join("data", "clean")
PROCESSED_PATH = os.path.join("data", "processed")
os.makedirs(PROCESSED_PATH, exist_ok=True)


def combine_all_clean_files():
    """Combines all *_clean.csv files from data/clean/ into one dataset."""
    clean_files = [f for f in os.listdir(CLEAN_PATH) if f.endswith("_clean.csv")]

    if not clean_files:
        print("⚠️ No cleaned CSV files found in data/clean/. Run clean_data.py first.")
        return

    all_dfs = []
    for file in clean_files:
        brand_name = os.path.splitext(file)[0].replace("_clean", "")
        df = pd.read_csv(os.path.join(CLEAN_PATH, file))
        df["brand"] = brand_name.capitalize()
        all_dfs.append(df)
        print(f"Loaded {file} ({len(df)} rows)")

    combined_df = pd.concat(all_dfs, ignore_index=True)

    # Remove color variants again (extra safety)
    combined_df["name"] = combined_df["name"].str.replace(r"\(.*?\)", "", regex=True).str.strip()

    # Drop duplicates (same phone, RAM, storage)
    if {"ram_gb", "storage_gb", "name"}.issubset(combined_df.columns):
        combined_df = combined_df.drop_duplicates(subset=["name", "ram_gb", "storage_gb"])

    output_path = os.path.join(PROCESSED_PATH, "all_brands_20k.csv")
    combined_df.to_csv(output_path, index=False)
    print(f"\nCombined dataset saved to {output_path}")
    print(f"Total rows: {len(combined_df)}")

    return combined_df


if __name__ == "__main__":
    combine_all_clean_files()
