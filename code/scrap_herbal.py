"""
-------------------------------------------------
Project : Product Data Analysis -- Calebasse Laboratoire
Author  : DOAN Ngoc Anh Thu (refactored by Xinyi DU)
Date    : 2025-10-17
Description :
    Scrape herbal products by product type and usage category
    from Calebasse Laboratoire and save raw data to CSV.
-------------------------------------------------
"""

from pathlib import Path
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from typing import List, Tuple

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
# CORE SCRAPER
# ======================
def scrape_category(
    base_url: str,
    category_name: str,
    nb_pages: int
) -> pd.DataFrame:
    rows = []

    for page in range(1, nb_pages + 1):
        url = base_url if nb_pages == 1 else f"{base_url}?page={page}"
        print(f"[INFO] Scraping {category_name} | page {page}")

        try:
            response = SESSION.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"[ERROR] Failed to fetch {url}: {e}")
            continue

        soup = BeautifulSoup(response.text, "lxml")

        titles = soup.find_all("div", class_=re.compile("product-card-title"))
        prices = soup.find_all("div", class_=re.compile("product-card-price"))

        for title_tag, price_tag in zip(titles, prices):
            name = title_tag.get_text(strip=True)

            price_span = price_tag.find("span")
            if price_span:
                price_text = (
                    price_span.get_text(strip=True)
                    .replace("€", "")
                    .replace(",", ".")
                )
                try:
                    price = float(price_text)
                except ValueError:
                    price = None
            else:
                price = None

            rows.append({
                "Product name": name,
                "Price (€)": price,
                "Category": category_name
            })

        time.sleep(1)

    return pd.DataFrame(rows)


# ======================
# PIPELINES
# ======================
def scrape_by_product_type() -> pd.DataFrame:
    categories_pages: List[Tuple[str, str, int]] = [
        ("https://calebasse.com/en/bains-de-pieds", "Foot baths", 1),
        ("https://calebasse.com/en/bio", "Bio", 1),
        ("https://calebasse.com/en/champignons", "Mushroom", 1),
        ("https://calebasse.com/en/gruaux", "Congees", 1),
        ("https://calebasse.com/en/infusions-a-fleurs", "Flower infusions", 1),
        ("https://calebasse.com/en/melanges-maison", "Homemade blends", 1),
        ("https://calebasse.com/en/plantes-en-vrac", "Bulk plants", 2),
        ("https://calebasse.com/en/thes", "Tea", 2),
        ("https://calebasse.com/en/plantes-mtc", "TMC Herbs", 5),
        ("https://calebasse.com/en/complements-alimentaires", "Food supplements", 1),
        ("https://calebasse.com/en/ingredients-petites-formules", "Plant powder", 1),
    ]

    dfs = [
        scrape_category(url, cat, pages)
        for url, cat, pages in categories_pages
    ]

    return pd.concat(dfs, ignore_index=True)


def scrape_by_usage() -> pd.DataFrame:
    uses_pages: List[Tuple[str, str, int]] = [
        ("https://calebasse.com/en/articulations-and-muscles", "Articulations and muscles", 1),
        ("https://calebasse.com/en/calme-and-bien-etre", "Calm and well-being", 1),
        ("https://calebasse.com/en/confort-respiratoire", "Respiratory comfort", 1),
        ("https://calebasse.com/en/detox-and-draineur", "Detox and drainer", 1),
        ("https://calebasse.com/en/equilibre-feminin", "Female balance", 1),
        ("https://calebasse.com/en/forme", "Fatigue and Energy", 2),
        ("https://calebasse.com/en/sante-cardiovasculaire", "Cardiovascular health", 1),
        ("https://calebasse.com/en/beaute-and-minceur", "Beauty and slimming", 1),
        ("https://calebasse.com/en/circulation", "Circulation", 1),
        ("https://calebasse.com/en/confort-urinaire", "Urinary comfort", 1),
        ("https://calebasse.com/en/digestion", "Digestion", 1),
        ("https://calebasse.com/en/equilibre-masculin", "Male balance", 1),
        ("https://calebasse.com/en/mtv", "MTV", 1),
        ("https://calebasse.com/en/vitalite-sexuelle", "Sexual vitality", 1),
    ]

    dfs = [
        scrape_category(url, cat, pages)
        for url, cat, pages in uses_pages
    ]

    return pd.concat(dfs, ignore_index=True)


# ======================
# ENTRY POINT
# ======================
def run():
    print("[START] Herbal products scraping")

    df_products = scrape_by_product_type()
    df_products.to_csv(
        DATA_DIR / "raw_herbal_products.csv",
        index=False,
        encoding="utf-8-sig"
    )
    print(f"[SAVED] raw_herbal_products.csv ({len(df_products)})")

    df_uses = scrape_by_usage()
    df_uses.to_csv(
        DATA_DIR / "raw_uses_products.csv",
        index=False,
        encoding="utf-8-sig"
    )
    print(f"[SAVED] raw_uses_products.csv ({len(df_uses)})")

    print("[DONE] Herbal scraping pipeline completed")
