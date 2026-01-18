"""
-------------------------------------------------
Project : Product Data Analysis -- Calebasse Laboratoire
Author  : Xinyi DU
Date    : 2025-10-13
Description :
    Process physical product data by merging products with the same name
    and combining their categories.
-------------------------------------------------
"""

from pathlib import Path
import pandas as pd

# ======================
# PATH CONFIG
# ======================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# ======================
# CORE PROCESSING
# ======================
def combine_same_products(
    input_csv: Path,
    output_csv: Path
) -> pd.DataFrame:
    """
    Combine products with the same name by merging their categories.
    """

    print(f"[INFO] Loading data from {input_csv}")
    df = pd.read_csv(input_csv, encoding="utf-8-sig")

    required_columns = {"Product name", "Product category", "Price (€)"}
    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"Missing required columns: {required_columns - set(df.columns)}"
        )

    # groupby + aggregation (vectorized & safe)
    result_df = (
        df.groupby("Product name", as_index=False)
        .agg({
            "Price (€)": "first",
            "Product category": lambda x: ", ".join(sorted(set(x)))
        })
    )

    result_df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"[SAVED] {len(result_df)} products → {output_csv}")

    return result_df


# ======================
# ENTRY POINT
# ======================
def run():
    input_csv = DATA_DIR / "raw_physical_products.csv"
    output_csv = DATA_DIR / "final_process_equipment.csv"

    combine_same_products(
        input_csv=input_csv,
        output_csv=output_csv
    )
