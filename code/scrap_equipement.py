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


def save_products(data: list, csv_file: str = "data/raw_physical_products.csv", json_file: str = "raw_physical_products.json"):
    current_path = os.getcwd()
    csv_path = os.path.join(current_path, csv_file)
    json_path = os.path.join(current_path, json_file)
    
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
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(orgniz_data)
    print(f"CSV file has been saved：{csv_file}")
    
    # sauvegarder les données dans le fichier json
    with open(json_path, 'w', encoding='utf-8') as f:
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
        
        
            