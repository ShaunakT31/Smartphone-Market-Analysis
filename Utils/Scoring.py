"""
utils/Scoring.py
-----------------
Utility module for computing composite and value-per-rupee scores
for smartphone specification datasets.

Used in: data processing and analysis stages of the Mobile_Phones_Analysis project.
"""

import pandas as pd


def add_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds two computed columns to the given DataFrame:
        - composite_score: weighted sum of key specifications
        - value_per_100k: composite_score normalized per ₹100,000 spent

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing columns:
        ['price', 'ram_gb', 'storage_gb', 'display_inch', 'battery_mah', 'camera_mp']

    Returns
    -------
    pd.DataFrame
        The same DataFrame with new columns 'composite_score' and 'value_per_100k'.
    """

    required_cols = ["price", "ram_gb", "storage_gb", "display_inch", "battery_mah", "camera_mp"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df[df["price"] > 0].copy()

    # Composite spec score
    df["composite_score"] = (
        (3 * df["ram_gb"]) +
        (df["storage_gb"] / 64) +
        (df["battery_mah"] / 1500) +
        (df["camera_mp"] / 12) +
        (df["display_inch"] * 0.5)
    )

    # Value efficiency per ₹100,000
    df["value_per_100k"] = (df["composite_score"] / df["price"]) * 100000

    return df


def rank_value_phones(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Returns the top N smartphones with the highest value_per_100k scores.

    Parameters
    ----------
    df : pd.DataFrame
        Must include 'brand', 'name', 'price', and 'value_per_100k' columns.
    top_n : int
        Number of top phones to return (default = 10).

    Returns
    -------
    pd.DataFrame
        Subset sorted by 'value_per_100k' descending.
    """
    required_cols = ["brand", "name", "price", "value_per_100k"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns for ranking: {missing}")

    ranked = df.sort_values("value_per_100k", ascending=False).head(top_n)
    return ranked.reset_index(drop=True)
