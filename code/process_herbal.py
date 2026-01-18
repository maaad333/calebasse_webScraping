"""
-------------------------------------------------
Project : Product Data Analysis -- Calebasse Laboratoire
Author  : DOAN Ngoc Anh Thu
Date    : 2025-10-17
Description :
    Ce script exclut les produits qui ne sont pas à base de plantes
    et fusionne les informations relatives aux deux types de catégories: 
    la catégorie du type de produit et la catégorie liée à l’usage du produit.
-------------------------------------------------
"""

import os
import pandas as pd


def normalize_name(s):
    """Normalize product name for merging"""
    if pd.isna(s):
        return ''
    return ' '.join(str(s).lower().strip().split())


def merge_categories(values):
    """Merge categories into a single string"""
    unique_values = set(values)
    sorted_values = sorted(unique_values)
    return '; '.join(sorted_values)


def process_herbal_products(raw_herbal_csv: str, raw_uses_csv: str, output_csv: str):
    """Process raw herbal and usage CSVs into final merged CSV"""
    # --- Load CSVs ---
    df_herbal = pd.read_csv(raw_herbal_csv)
    df_herbal = df_herbal[~df_herbal["Product name"].str.contains("Filter|Boule à thé|filter")]

    df_uses = pd.read_csv(raw_uses_csv)
    df_uses = df_uses[~df_uses["Product name"].str.contains("sha|Roller|Plate|Massager|Brush|brush|Comb")]

    # --- Normalize names for merging ---
    df_herbal['name_norm'] = df_herbal['Product name'].apply(normalize_name)
    df_uses['name_norm'] = df_uses['Product name'].apply(normalize_name)

    # --- Rename columns for clarity ---
    df_herbal = df_herbal.rename(columns={'Category': 'Product category'})
    df_uses = df_uses.rename(columns={'Category': 'Use category'})

    # --- Merge ---
    df_merged = pd.merge(
        df_herbal[['name_norm', 'Product name', 'Price (€)', 'Product category']],
        df_uses[['name_norm', 'Product name', 'Price (€)', 'Use category']],
        on='name_norm',
        how='outer',
        suffixes=('_type', '_use')
    )

    df_merged['Product name'] = df_merged['Product name_type'].combine_first(df_merged['Product name_use'])
    df_merged['Price (€)'] = df_merged['Price (€)_type'].combine_first(df_merged['Price (€)_use'])

    df_final = df_merged[['Product name', 'Price (€)', 'Product category', 'Use category']].copy()
    df_final = df_final.fillna({'Product category': 'Others', 'Use category': 'Others'})

    # --- Group by product name and price, merge categories ---
    df_final = (
        df_final.groupby(['Product name', 'Price (€)'])
        .agg({
            'Product category': merge_categories,
            'Use category': merge_categories
        })
        .reset_index()
    )

    # --- Save CSV ---
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df_final.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"✅ Total number of products: {len(df_final)}")
    print(f"CSV saved at: {output_csv}")

    return df_final

def main():
    raw_herbal_csv = "data/raw_herbal_products.csv"
    raw_uses_csv = "data/raw_uses_products.csv"
    output_csv = "data/final_herb_products.csv"
    process_herbal_products(raw_herbal_csv, raw_uses_csv, output_csv)
    
# --- Main entry ---
if __name__ == "__main__":
    main()