"""
-------------------------------------------------
Project : Product Data Analysis -- Calebasse Laboratoire
Author  : Xinyi DU
Date    : 2025-10-13
Description :
    Ce script scrappe les produits d'équipement qui sert aux soins 
    du corps sur le site Calebasse Laboratoire et sauvegarede les 
    informations nettoyéescdes produits (nom du produit, prix, cathégorie)
    au forma jons et csv
-------------------------------------------------
"""

import re
import os
import pandas as pd

def combine_same_products(path_csv, output_path=None):
    """
    parcourir les données et combiner les produits 
    avec les mêmes catégories
    """
    df = pd.read_csv(path_csv, encoding='utf-8-sig')
    
    # Grouper par nom de produit
    products_by_name = {}
    
    for index, row in df.iterrows():
        product_name = row['Product name']
        category = row['Product category']
        price = row['Price (€)']
        
        if product_name not in products_by_name:
            # Créer une nouvelle entrée
            products_by_name[product_name] = {
                'Product category': [category],
                'Price (€)': price
            }
        else:
            # Ajouter la catégorie si elle n'existe pas déjà
            if category not in products_by_name[product_name]['Product category']:
                products_by_name[product_name]['Product category'].append(category)
    
    # Convertir en DataFrame
    result_data = []
    for product_name, info in products_by_name.items():
        result_data.append({
            'Product name': product_name,
            'Price (€)': info['Price (€)'],
            'Product category': ', '.join(info['Product category'])
        })
    
    result_df = pd.DataFrame(result_data)
    
    # Sauvegarder
  
    output_path =  "data/final_process_equipement.csv"
    
    result_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print(f"✅ {len(result_data)} produits sauvegardés dans {output_path}")
    
    return result_df


def main():
    combine_same_products("data/raw_physical_products.csv")


if __name__ == '__main__':
    main()