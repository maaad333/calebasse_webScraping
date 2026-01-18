
import os
import csv 
import pandas as pd 
import matplotlib.pyplot as plt
import streamlit as st
from analyse_equipement import pei_figure, bar_figure, plot_box_visualisation
from analyse_herbal import plot_pie_categorie, plot_bar_price, plot_heatmap

def compare_food_equipements(df_food, df_equipement, image_name):
    'using pie chart to compare the food products and equipement products'
    nb_food = len(df_food)
    nb_eq = len(df_equipement)
    total = nb_food + nb_eq
    labels = ['Food', 'Equipment']
    data = [nb_food, nb_eq]
    
    colors = plt.cm.tab20.colors 
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(
        data,
        labels=labels,
        autopct=lambda pct: f"{pct:.1f}%" if pct > 3 else "",
        startangle=90,
        counterclock=False,
        colors=colors[:len(labels)],
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
        textprops={'fontsize': 11, 'color': 'black'}
    )
    
    ax.set_title('Répartition des produits par deux grandes catégories')
    ax.axis('equal')
    current_path = os.getcwd()
    save_pie_image = os.path.join(current_path, image_name)
    fig.savefig(save_pie_image, dpi=300, bbox_inches='tight')
    st.pyplot(fig)
    

def main():
    st.set_page_config(page_title="Calebasse Product Data Visualization", layout="wide")
    st.title("📊 Product Data Visualization — Calebasse Laboratoire")
    st.markdown("Visualisez les données extraites du site Calebasse (catégories, prix, etc.).")
    
    eq_path_csv = 'data/final_process_equipement.csv'
    eq_df = pd.read_csv(eq_path_csv)
    food_path_csv = 'data/final_herb_products.csv'
    food_df = pd.read_csv(food_path_csv)
    compare_food_equipements(food_df, eq_df, image_name='demo\images\/food_eq_products.png')
    path_csv = 'data/raw_physical_products.csv'
    df = pd.read_csv(path_csv)
    pei_figure(df=df, image_name='demo\images\equipements_pei_category.png')
    bar_figure(df=df, image_name='demo\images\/equipements_bar_price.png')
    plot_box_visualisation(df=df, image_name='demo\images\equipements_plotbox_price.png')

    plot_pie_categorie("Product category", "Catégories de produits de plantes", 'demo\images\herbal_cate_product.png')
    plot_pie_categorie("Use category", "Catégories d'usage des produits de plantes", 'demo\images\herbal_cate_use.png')
    plot_bar_price("Product category", 'Prix moyen par catégorie de produit', 'demo\images\herbal_price_product.png')
    plot_bar_price("Use category", 'Prix moyen par catégorie des usages de produit', 'demo\images\herbal_price_use.png')
    plot_heatmap('demo\images\herbal_heatmap.png')


if __name__ == '__main__': 
    main()




