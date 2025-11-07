"""
pipeline/run_pipeline.py
-------------------------
Main orchestrator script for the Mobile_Phones_Analysis project.
Runs all key pipeline stages in order:

1. Cleaning raw JSONs  -> data/clean/
2. Combining clean CSVs -> data/processed/all_brands_20k.csv
3. Adding scoring metrics (composite_score, value_per_100k)

After execution, the project data is fully prepared for analysis notebooks.
"""

import os
import sys
import subprocess
import pandas as pd

# Add project root to import path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import your scoring functions
from utils.Scoring import add_scores

# Define paths
DATA_PROCESSED_PATH = os.path.join(project_root, "data", "processed", "all_brands_20k.csv")
PIPELINE_SCRIPTS = [
    os.path.join("pipeline", "clean_data.py"),
    os.path.join("pipeline", "combine_data.py")
]


def run_subprocess(script_path):
    """Runs another Python script and streams its output."""
    print(f"\n🚀 Running: {script_path}")
    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("⚠️ Errors/Warnings:\n", result.stderr)


def run_full_pipeline():
    """Executes the full pipeline: clean → combine → score."""
    print("\n==============================")
    print(" 📊 Starting Mobile Phones Data Pipeline ")
    print("==============================\n")

    # Step 1 + 2: Run cleaning and combining scripts
    for script in PIPELINE_SCRIPTS:
        run_subprocess(script)

    # Step 3: Apply scoring to combined dataset
    if os.path.exists(DATA_PROCESSED_PATH):
        print("\n📈 Adding composite & value scores...")
        df = pd.read_csv(DATA_PROCESSED_PATH)
        df = add_scores(df)
        df.to_csv(DATA_PROCESSED_PATH, index=False)
        print(f"✅ Scoring complete. Updated file saved: {DATA_PROCESSED_PATH}")
        print(f"Total rows: {len(df)}")
    else:
        print("❌ Combined dataset not found. Run combine_data.py manually.")

    print("\n🎉 Pipeline finished successfully!")


if __name__ == "__main__":
    run_full_pipeline()
