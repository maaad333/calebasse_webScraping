"""
-------------------------------------------------
Project : Product Data Analysis -- Calebasse Laboratoire
Author  : Xinyi DU
Date    : 2025-10-13
Description :
    Scrape physical healthcare products from Calebasse Laboratoire
    and save cleaned data into CSV and JSON.
-------------------------------------------------
"""

from pathlib import Path
import requests
import re
import time
import csv
import json
from bs4 import BeautifulSoup
from typing import List, Dict

# ======================
# PATH CONFIG
# ======================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# ======================
# REQUEST SESSION
# ======================
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
    )
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)

# ======================
# UTILS
# ======================
def has_next_page(soup: BeautifulSoup) -> bool:
    selectors = [
        'a[rel="next"]',
        'a.next',
        'li.next a'
    ]
    return any(soup.select_one(sel) for sel in selectors)


# ======================
# SCRAPER
# ======================
def scrape_physical_products(url: str, category: str) -> List[Dict]:
    print(f"[INFO] Scraping category: {category}")
    results = []
    page = 1

    while True:
        page_url = url if page == 1 else f"{url}?page={page}"
        print(f"[INFO] Fetching page {page}: {page_url}")

        try:
            response = SESSION.get(page_url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"[ERROR] Request failed: {e}")
            break

        soup = BeautifulSoup(response.text, "lxml")

        products = soup.find_all(
            "div", class_=re.compile("^product-card")
        )

        if not products:
            print("[INFO] No products found, stopping.")
            break

        for product in products:
            name_tag = product.find("div", class_=re.compile("product-card-title"))
            price_tag = product.find("span")

            product_name = (
                name_tag.get_text(strip=True)
                if name_tag else "Unknown"
            )

            product_price = (
                price_tag.get_text(strip=True)
                if price_tag else "ToBeDefined"
            )

            results.append({
                "Product name": product_name,
                "Price (€)": product_price,
                "Product category": category
            })

        if not has_next_page(soup):
            break

        page += 1
        time.sleep(1)

    print(f"[SUCCESS] {len(results)} products collected for {category}")
    return results


# ======================
# FILTER
# ======================
def filter_skin_products(data: List[Dict]) -> List[Dict]:
    keywords = ['stone', 'plate', 'roller', 'tool', 'wood', 'pen', 'sha']
    return [
        item for item in data
        if any(k in item["Product name"].lower() for k in keywords)
    ]


# ======================
# SAVE
# ======================
def save_products(data: List[List[Dict]]) -> None:
    flat_data = []

    for category_data in data:
        for item in category_data:
            price = item.get("Price (€)", "")
            if price != "ToBeDefined":
                price = re.sub(r"[^\d,]", "", price).replace(",", ".")
            item["Price (€)"] = price
            flat_data.append(item)

    csv_path = DATA_DIR / "raw_physical_products.csv"
    json_path = DATA_DIR / "raw_physical_products.json"

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=flat_data[0].keys())
        writer.writeheader()
        writer.writerows(flat_data)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(flat_data, f, ensure_ascii=False, indent=2)

    print(f"[SAVED] CSV → {csv_path}")
    print(f"[SAVED] JSON → {json_path}")
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

import webbrowser
import requests
import os
import re
from bs4 import BeautifulSoup
import time
import csv 
import json
import pandas as pd




def check_next_page(soup):
    """
    check if it has the next page
    """
    next_button_selectors = [
        'a.next',
        'a[rel="next"]',
        'a.pagination-next',
        'button.next-page',
        'a:contains("Next")',
        'a:contains',
        'a.page-link:contains("›")',
        'li.next a'
    ]
    
    for selector in next_button_selectors:
        if 'contains' in selector:
            continue
        next_btn = soup.select_one(selector)
        if next_btn and not next_btn.get('disabled'):
            return True        

    
def scrap_physical_products(url, categorie):
    """
    scrap healthcare physical products in website Calebasse Laboratoire
    """

    # stabiizer le site de web scrapping
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"}
    print("********* loading physical healthy products *********")

    # container pour collecer les données
    product_date = []
    # page initiale
    current_page = 1
    all_products = 0
    
    while True:
        print(f'\n scrapping the {current_page} page')
        
        # consider la situation ou il y a plusieurs pages de produits
        if current_page == 1:
            page_url = url
        else:
            page_url = url + f'?page={current_page}'
            
        # se preparer pour le web scrapping
        response = requests.get(page_url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        
        # trouver d'abord tous les produits 
        class_partern_products = re.compile("^product-card @container")
        physical_items = soup.find_all('div', attrs={"class":class_partern_products})
        print(f"****** the {current_page} page has {len(physical_items)} products")
        all_products += len(physical_items)
        if not physical_items:
            print(f'the {current_page} page does not have products, it is the last page')
            print(f'in total we find ')
            break
        
        # collecter ensuite les informations des produits
        for i, product in enumerate(physical_items):
            class_partern_name = re.compile("^product-card-title")
            div_name = product.find('div', attrs={"class":class_partern_name})
            product_name = div_name.get_text(strip=True)

            div_price = product.find('span', attrs={"class":""})
            if div_price:
                product_price = div_price.get_text(strip=True)
            else:
                product_price == 'ToBeDefined'

            product_date.append({
                'Product name': product_name,
                'Price (€)': product_price,
                'Product category': categorie
            })
            
        has_next_page = check_next_page(soup)
        if not has_next_page:
            print(f'already at the {current_page} page')
            break
        
        current_page += 1
        time.sleep(1)
            
    print(f'******* sucessfully grab{len(product_date)} physical products*******')
    return product_date
  
     
def skin_products_filter(data:list):
    # tirer les mots-clés des produits d'équopement pour la peau
    keywords = ['stone', 'plate', 'roller', 'tool', 'wood', 'pen', 'sha']
    data = [
        item for item in data
        if any(kw in item.get('Product name', '').lower() for kw in keywords)
    ]
    return data    


def save_products(data: list, csv_file: str = "data/raw_physical_products.csv", json_file: str = "data/raw_physical_products.json"):

    
    # nettoyer les données de prix
    orgniz_data = []
    for catgegory in data:
        for item in catgegory:
            price_str = item.get('Price (€)','')
            if price_str != 'ToBeDefined':
                price_num = re.sub(r'[^\d,]', '', price_str).replace(',', '.')
            else:
                price_num = price_str
            item['Price (€)'] = price_num
            orgniz_data.append(item)
    
    # sauvegarder les données dans le fichier csv
    headers = orgniz_data[0].keys()
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(orgniz_data)
    print(f"CSV file has been saved：{csv_file}")
    
    # sauvegarder les données dans le fichier json
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(orgniz_data, f, ensure_ascii=False, indent=2)
    
    print(f"JSON file has been saved：{json_file}")
    

def main():
    print("*" * 50)
    print('******************** physcial product scrapping ***************')
    print("*" * 50)

    
    # fourir les urls et les catégories des web scrapping
    urls = ['https://calebasse.com/en/autocuiseurs-pour-decoction', 'https://calebasse.com/en/herbiers-et-kits', 'https://calebasse.com/en/materiel-de-moxibustion', 'https://calebasse.com/en/materiel-dacupuncture', 'https://calebasse.com/en/nouveautes','https://calebasse.com/en/ventouses', 'https://calebasse.com/en/objets-decoratifs', 'https://calebasse.com/en/livres' ]
    cathegory = ['cooker', 'kit', 'moxibustion', 'acupuncture','new products', 'cupping', 'decorative', 'books']
    all_physical_products = []
    
    # web scrapping des produits d'équipement
    for url, cat in zip(urls, cathegory):
        webbrowser.open(url, new=2)
        print(cat)
        data = scrap_physical_products(url, cat)
        all_physical_products.append(data)
    
    # web scrapping des produits au service de la peau
    url_skin = 'https://calebasse.com/en/peau'
    webbrowser.open(url_skin, new=2)
    data_skin = scrap_physical_products(url_skin, 'skin')
    data_skin_filter = skin_products_filter(data_skin)
    all_physical_products.append(data_skin_filter)   
    
    save_products(all_physical_products)

    
if __name__ == "__main__":
    main()
        
        
            

# ======================
# ENTRY POINT
# ======================
