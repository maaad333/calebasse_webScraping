"""
-------------------------------------------------
Project : Product Data Analysis -- Calebasse Laboratoire
Author  : DOAN Ngoc Anh Thu (refactored by Xinyi DU)
Date    : 2025-10-17
Description :
    Clean herbal product data and merge product type categories
    with usage categories.
-------------------------------------------------
"""

from pathlib import Path
import pandas as pd
import re

# ======================
# PATH CONFIG
# ======================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# ======================
# UTILS
# ======================
def normalize_name(value: str) -> str:
    if pd.isna(value):
        return ""
    return " ".join(str(value).lower().strip().split())


def merge_categories(series: pd.Series) -> str:
    values = sorted(set(series.dropna()))
    return "; ".join(values) if values else "Others"


# ======================
# FILTERS
# ======================
def filter_non_herbal_products(df: pd.DataFrame, pattern: str) -> pd.DataFrame:
    mask = ~df["Product name"].str.contains(
        pattern, case=False, regex=True, na=False
    )
    return df.loc[mask].copy()


# ======================
# CORE PROCESSING
# ======================
def process_herbal_products(
    herbal_csv: Path,
    uses_csv: Path,
    output_csv: Path
) -> pd.DataFrame:
    print("[INFO] Loading raw herbal datasets")

    df_herbal = pd.read_csv(herbal_csv, encoding="utf-8-sig")
    df_uses = pd.read_csv(uses_csv, encoding="utf-8-sig")

    # Filter non-herbal products
    df_herbal = filter_non_herbal_products(
        df_herbal, r"Filter|Boule à thé|filter"
    )
    df_uses = filter_non_herbal_products(
        df_uses, r"sha|roller|plate|massager|brush|comb"
    )

    # Normalize product names
    df_herbal = df_herbal.assign(
        name_norm=df_herbal["Product name"].apply(normalize_name)
    )
    df_uses = df_uses.assign(
        name_norm=df_uses["Product name"].apply(normalize_name)
    )

    # Rename columns
    df_herbal = df_herbal.rename(
        columns={"Category": "Product category"}
    )
    df_uses = df_uses.rename(
        columns={"Category": "Use category"}
    )

    # Merge datasets
    df_merged = pd.merge(
        df_herbal[["name_norm", "Product name", "Price (€)", "Product category"]],
        df_uses[["name_norm", "Product name", "Price (€)", "Use category"]],
        on="name_norm",
        how="outer",
        suffixes=("_type", "_use")
    )

    # Consolidate name and price
    df_merged["Product name"] = (
        df_merged["Product name_type"]
        .combine_first(df_merged["Product name_use"])
    )
    df_merged["Price (€)"] = (
        df_merged["Price (€)_type"]
        .combine_first(df_merged["Price (€)_use"])
    )

    df_final = df_merged[
        ["Product name", "Price (€)", "Product category", "Use category"]
    ].copy()

    df_final = df_final.fillna({
        "Product category": "Others",
        "Use category": "Others"
    })

    # Aggregate duplicated products
    df_final = (
        df_final
        .groupby(["Product name", "Price (€)"], as_index=False)
        .agg({
            "Product category": merge_categories,
            "Use category": merge_categories
        })
    )

    df_final.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"[SAVED] {len(df_final)} herbal products → {output_csv}")

    return df_final


# ======================
# ENTRY POINT
# ======================
def run():
    process_herbal_products(
        herbal_csv=DATA_DIR / "raw_herbal_products.csv",
        uses_csv=DATA_DIR / "raw_uses_products.csv",
        output_csv=DATA_DIR / "final_herb_products.csv"
    )
