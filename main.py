
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
    pie_figure_herbal,
    bar_figure_herbal,
    plot_box_visualisation_herbal
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
    with st.spinner("Processing data..."):
        process_equipement_products()
        process_herbal_products()

    st.success("Traitement terminé")

    # =============================
    # 3️⃣ LOAD DATA
    # =============================
    df_eq = pd.read_csv('data/final_process_equipement.csv')
    df_food = pd.read_csv('data/final_herb_products.csv')
    df_raw_eq = pd.read_csv('data/raw_physical_products.csv')

    # =============================
    # 4️⃣ VISUALISATION
    # =============================
    st.header("📌 Global comparison")
    compare_food_equipements(
        df_food,
        df_eq,
        image_name='demo/images/food_eq_products.png'
    )

    st.header("🔧 Equipement analysis")
    pei_figure(df=df_raw_eq, image_name='demo/images/eq_pie.png')
    bar_figure(df=df_raw_eq, image_name='demo/images/eq_bar.png')
    plot_box_visualisation(df=df_raw_eq, image_name='demo/images/eq_box.png')

    st.header("🌿 Herbal products analysis")
    pie_figure_herbal(df_food, 'demo/images/herbal_pie.png')
    bar_figure_herbal(df_food, 'demo/images/herbal_bar.png')
    plot_box_visualisation_herbal(df_food, 'demo/images/herbal_box.png')

    st.success("🎉 Pipeline exécuté avec succès")


# --------------------------------------------------
if __name__ == '__main__':
    main()
