"""
-------------------------------------------------
Project : Product Data Analysis -- Calebasse Laboratoire
Author  : DOAN Ngoc Anh Thu / Xinyi DU
Date    : 2025-10-17
Description :
   Ce script scrappe les produits de la catégorie plantes 
   sur le site Calebasse Laboratoire et sauvegarde 
   les informations brutes des produits (nom du produit, prix, catégorie) au format CSV.
   Il y a deux types de catégories : les catégories selon le type de produit 
   et les catégories selon l’usage (ou la fonction)
-------------------------------------------------
"""

import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd
import os


def scrap(base_url, category_name, nb_pages):
    """
    Scrap products from a single category URL.
    Returns a DataFrame.
    """
    products = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }

    for page in range(1, nb_pages + 1):
        url = f"{base_url}?page={page}" if nb_pages > 1 else base_url
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"❌ Failed to connect to {url}: {e}")
            continue

        soup = BeautifulSoup(response.text, 'lxml')

        # Extract titles and prices
        title_tags = soup.find_all(
            'div',
            class_='product-card-title line-clamp-2 max-w-full font-medium underline-offset-2 group-hover:underline text-center text-sm @[200px]:text-base'
        )
        price_tags = soup.find_all(
            'div',
            class_='product-card-price flex items-center gap-2 text-base font-medium @[200px]:text-lg'
        )

        for i in range(len(title_tags)):
            name = title_tags[i].get_text(strip=True)
            price_span = price_tags[i].find('span')
            try:
                price = float(price_span.get_text(strip=True).replace('€','').replace(',', '.').strip())
            except Exception:
                price = None
            products.append((name, price, category_name))

    df = pd.DataFrame(products, columns=['Product name', 'Price (€)', 'Category'])
    return df


def scrap_all():
    """
    Scrap all herbal products (type + usage) and save CSVs.
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    os.makedirs(DATA_DIR, exist_ok=True)

    # --- Categories by product type ---
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
        print(f"Scraping type category: {category_name}")
        df_temp = scrap(base_url, category_name, nb_pages)
        dfs.append(df_temp)

    df_herbal_product = pd.concat(dfs, ignore_index=True)
    df_herbal_product.to_csv("data/raw_herbal_products.csv", index=False, encoding="utf-8-sig")
    print(f"✅ Total number of scraped products (type): {len(df_herbal_product)}")

    # --- Categories by product usage ---
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
        print(f"Scraping usage category: {category_name}")
        df_temp = scrap(base_url, category_name, nb_pages)
        dfs_uses.append(df_temp)

    df_uses_product = pd.concat(dfs_uses, ignore_index=True)
    df_uses_product.to_csv("data/raw_uses_products.csv", index=False, encoding='utf-8-sig')
    print(f"✅ Total number of scraped products (uses): {len(df_uses_product)}")


# --- Main entry ---
if __name__ == "__main__":
    scrap_all()
