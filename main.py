
import os
import csv 
import pandas as pd 
import matplotlib.pyplot as plt
import streamlit as st
from code import ( 
    process_equipement_products,
    process_herbal_products,
    scrap_equipement_products,
    scrap_herbal_products,
    pei_figure,
    bar_figure,
    plot_box_visualisation,
    plot_pie_categorie,
    plot_bar_price,
    plot_heatmap, 
)


# --------------------------------------------------
# Utility
# --------------------------------------------------
def compare_food_equipements(df_food, df_equipement, image_name):
    import matplotlib.pyplot as plt

    nb_food = len(df_food)
    nb_eq = len(df_equipement)

    labels = ['Food (Herbal)', 'Equipment']
    data = [nb_food, nb_eq]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        data,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90
    )
    ax.set_title('Répartition des produits')
    ax.axis('equal')

    fig.savefig(image_name, dpi=300, bbox_inches='tight')
    st.pyplot(fig)


# --------------------------------------------------
# MAIN PIPELINE
# --------------------------------------------------
def main():
    st.set_page_config(
        page_title="Calebasse Product Data Visualization",
        layout="wide"
    )

    st.title("📊 Calebasse — Product Data Pipeline")
    st.markdown("Scraping → Processing → Visualization")

    """
    # =============================
    # 1️⃣ SCRAPING
    # =============================
    with st.spinner("Scraping equipement products..."):
        scrap_equipement_products()

    with st.spinner("Scraping herbal products..."):
        scrap_herbal_products()

    st.success("Scraping terminé")

    # =============================
    # 2️⃣ PROCESSING
    # =============================

    process_equipement_products()
    process_herbal_products()
    

    st.success("Traitement terminé")
    """
    
    # =============================
    # 3️⃣ VISUALIZATION
    # =============================

    
    eq_path_csv = "data/final_process_equipement.csv"
    eq_df = pd.read_csv(eq_path_csv)
    food_path_csv = "data/final_herb_products.csv"
    food_df = pd.read_csv(food_path_csv)
    compare_food_equipements(food_df, eq_df, image_name="demo/images/food_eq_products.png")
    path_csv = "data/raw_physical_products.csv"
    df = pd.read_csv(path_csv)
    pei_figure(df=df, image_name="demo/images/equipements_pei_category.png")
    bar_figure(df=df, image_name="demo/images/equipements_bar_price.png")
    plot_box_visualisation(df=df, image_name="demo/images/equipements_plotbox_price.png")

    plot_pie_categorie("Product category", "Catégories de produits de plantes", "demo/images/herbal_cate_product.png")
    plot_pie_categorie("Use category", "Catégories d'usage des produits de plantes", "demo/images/herbal_cate_use.png")
    plot_bar_price("Product category", 'Prix moyen par catégorie de produit', "demo/images/herbal_price_product.png")
    plot_bar_price("Use category", 'Prix moyen par catégorie des usages de produit', "demo/images/herbal_price_use.png")
    plot_heatmap("demo/images/herbal_heatmap.png")

# --------------------------------------------------
if __name__ == '__main__':
    
    main()
