"""
-------------------------------------------------
Project : Product Data Analysis -- Calebasse Laboratoire
Author  : DOAN Ngoc Anh Thu
Date    : 2025-10-17
Description :
   Ce script scrappe les produits de la catégorie plantes 
   sur le site Calebasse Laboratoire et sauvegarde 
   les informations brutes des produits (nom du produit, prix, catégorie) au format CSV.
   Il y a deux types de catégories : les catégories selon le type de produit 
   et les catégories selon l’usage (ou la fonction)
-------------------------------------------------
"""

import webbrowser
import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd
import numpy as np

def scrap(base_url, category_name, nb_pages):
    products = []
    for page in range(1, nb_pages + 1):
        if nb_pages > 1:
            url = base_url + '?page=' + str(page)
        else:
            url = base_url
        response = requests.get(url)
        if response.ok:
            soup = BeautifulSoup(response.text, 'lxml')

            title = soup.find_all(
                'div',
                class_='product-card-title line-clamp-2 max-w-full font-medium underline-offset-2 group-hover:underline text-center text-sm @[200px]:text-base'
            )
            prices = soup.find_all(
                'div',
                class_='product-card-price flex items-center gap-2 text-base font-medium @[200px]:text-lg'
            )

            for i in range(len(title)):
                name = title[i].get_text(strip=True)
                price_span = prices[i].find('span')
                price = price_span.get_text(strip=True).replace('€','').replace(',', '.').strip()
                products.append((name, float(price), category_name))
        else:
            sys.exit(f'BUG : Failed to connect to {url}')
    return pd.DataFrame(products, columns=['Product name', 'Price (€)', 'Category'])


#Scrap produits par catégorie de produit
categories_pages = [
    ('https://calebasse.com/en/bains-de-pieds', 'Foot baths', 1),
    ('https://calebasse.com/en/bio', 'Bio', 1),
    ('https://calebasse.com/en/champignons', 'Mushroom', 1),
    ('https://calebasse.com/en/gruaux', 'Congees', 1),
    ('https://calebasse.com/en/infusions-a-fleurs', 'Flower infusions', 1),
    ('https://calebasse.com/en/melanges-maison', 'Homemade blends', 1),
    ('https://calebasse.com/en/plantes-en-vrac', 'Bulk plantes', 2),
    ('https://calebasse.com/en/thes', 'Tea', 2),
    ('https://calebasse.com/en/plantes-mtc', 'TMC Herbs', 5),
    ('https://calebasse.com/en/complements-alimentaires', 'Food supplements', 1),
    ('https://calebasse.com/en/ingredients-petites-formules', 'Plant powder', 1)

]


dfs = []
for base_url, category_name, nb_pages in categories_pages:
    webbrowser.open(base_url, new=2)
    df_temp = scrap(base_url, category_name, nb_pages)
    dfs.append(df_temp)


df_herbal_product = pd.concat(dfs, ignore_index=True)

df_herbal_product.to_csv("data/raw_herbal_products.csv", index=False, encoding="utf-8-sig")

print('Total number of scraped products:', len(df_herbal_product))
print(df_herbal_product.head())

#Scrap produits par catégorie d'usage
uses_pages = [
    ('https://calebasse.com/en/articulations-and-muscles', 'Articulations and muscles', 1),
    ('https://calebasse.com/en/calme-and-bien-etre', 'Calm and well-being', 1),
    ('https://calebasse.com/en/confort-respiratoire', 'Respiratory comfort', 1),
    ('https://calebasse.com/en/detox-and-draineur', 'Detox and drainer', 1),
    ('https://calebasse.com/en/equilibre-feminin', 'Female balance', 1),
    ('https://calebasse.com/en/forme', 'Fatigue and Energy', 2),
    ('https://calebasse.com/en/sante-cardiovasculaire', 'Cardiovascular health', 1),
    ('https://calebasse.com/en/beaute-and-minceur', 'Beauty and slimming', 1),
    ('https://calebasse.com/en/circulation', 'Circulation', 1),
    ('https://calebasse.com/en/confort-urinaire', 'Urinary comfort', 1),
    ('https://calebasse.com/en/digestion', 'Digestion', 1),
    ('https://calebasse.com/en/equilibre-masculin', 'Male balance', 1),
    ('https://calebasse.com/en/mtv', 'MTV', 1),
    ('https://calebasse.com/en/vitalite-sexuelle', 'Sexual vitality', 1)
]

dfs_uses = []
for base_url, category_name, nb_pages in uses_pages:
    df_temp = scrap(base_url, category_name, nb_pages)
    dfs_uses.append(df_temp)

df_uses_product = pd.concat(dfs_uses, ignore_index=True)

df_uses_product.to_csv('data/raw_uses_products.csv', index=False, encoding='utf-8-sig')

print('Total number of scraped products (uses):', len(df_uses_product))
print(df_uses_product.head())


