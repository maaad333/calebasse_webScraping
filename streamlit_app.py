import pandas as pd
import streamlit as st

from code import (
    pei_figure,
    bar_figure,
    plot_box_visualisation,
    pie_figure_herbal,
    bar_figure_herbal,
    plot_box_visualisation_herbal
)

# --------------------------------------------------
def main():
    st.set_page_config(
        page_title="Calebasse Product Data Visualization",
        layout="wide"
    )

    st.title("🌿 Calebasse — Product Data Analysis")
    st.markdown("Données issues du site Calebasse Laboratoire")

    # =============================
    # LOAD DATA
    # =============================
    df_eq = pd.read_csv('data/final_process_equipement.csv')
    df_food = pd.read_csv('data/final_herb_products.csv')
    df_raw_eq = pd.read_csv('data/raw_physical_products.csv')

    # =============================
    # GLOBAL
    # =============================
    st.header("📊 Global overview")
    st.metric("Nombre produits plantes", len(df_food))
    st.metric("Nombre produits équipement", len(df_eq))

    # =============================
    # EQUIPMENT
    # =============================
    st.header("🔧 Equipement products")
    pei_figure(df_raw_eq, "demo/images/eq_pie.png")
    bar_figure(df_raw_eq, "demo/images/eq_bar.png")
    plot_box_visualisation(df_raw_eq, "demo/images/eq_box.png")

    # =============================
    # HERBAL
    # =============================
    st.header("🌱 Herbal products")
    pie_figure_herbal(df_food, "demo/images/herbal_pie.png")
    bar_figure_herbal(df_food, "demo/images/herbal_bar.png")
    plot_box_visualisation_herbal(df_food, "demo/images/herbal_box.png")

    st.success("✅ Visualisation chargée")


# --------------------------------------------------
if __name__ == "__main__":
    main()
