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
import pandas as pd
#Supprimer les produits non-plantes du dataframe des produits à base de type
raw_herbal_products = pd.read_csv('data/raw_herbal_products.csv')
df_herbal = raw_herbal_products[
    raw_herbal_products["Product name"].str.contains("Filter|Boule à thé|filter") == False]

#Supprimer les produits non-plantes du dataframe des produits à base d'usage
raw_uses_products = pd.read_csv('data/raw_uses_products.csv')
df_uses = raw_uses_products[
    raw_uses_products["Product name"].str.contains("sha|Roller|Plate|Massager|Brush|brush|Comb") == False]

#Merge 2 dataframe en un seul avec quatre colonnes : nom du produit, prix, catégorie de produit et catégorie d’utilisation
def normalize_name(s):
    if pd.isna(s):
        return ''
    return ' '.join(str(s).lower().strip().split())

df_herbal['name_norm'] = df_herbal['Product name'].apply(normalize_name)
df_uses['name_norm'] = df_uses['Product name'].apply(normalize_name)

df_herbal = df_herbal.rename(columns={'Category': 'Product category'})
df_uses = df_uses.rename(columns={'Category': 'Use category'})

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

# Fonction pour merge les catégories 
def merge_categories(values):
    unique_values = set(values)           
    sorted_values = sorted(unique_values) 
    return '; '.join(sorted_values)       

# Grouper par nom de produit et prix, puis fusionner les catégories
df_final = (
    df_final.groupby(['Product name', 'Price (€)'])
    .agg({
        'Product category': merge_categories,
        'Use category': merge_categories
    })
    .reset_index()
)

print('Total number of products:', len(df_final))
df_final.to_csv('data/final_herb_products.csv', index=False)







