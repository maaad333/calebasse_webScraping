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


# ======================
# ENTRY POINT
# ======================
def run():
    urls = [
        "https://calebasse.com/en/autocuiseurs-pour-decoction",
        "https://calebasse.com/en/herbiers-et-kits",
        "https://calebasse.com/en/materiel-de-moxibustion",
        "https://calebasse.com/en/materiel-dacupuncture",
        "https://calebasse.com/en/nouveautes",
        "https://calebasse.com/en/ventouses",
        "https://calebasse.com/en/objets-decoratifs",
        "https://calebasse.com/en/livres",
    ]

    categories = [
        "cooker", "kit", "moxibustion", "acupuncture",
        "new products", "cupping", "decorative", "books"
    ]

    all_products = []

    for url, cat in zip(urls, categories):
        all_products.append(scrape_physical_products(url, cat))

    skin_url = "https://calebasse.com/en/peau"
    skin_data = scrape_physical_products(skin_url, "skin")
    all_products.append(filter_skin_products(skin_data))

    save_products(all_products)
