"""
-------------------------------------------------
Project : Product Data Analysis -- Calebasse Laboratoire
Author  : DOAN Ngoc Anh Thu
Date    : 2025-10-17
Description :
    Ce script visualise les données sous forme de graphiques
    (pie chart, pie chart, heatmap)
-------------------------------------------------
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="whitegrid", palette="Set2")
from matplotlib.colors import ListedColormap
import streamlit as st

# Analyse de la classification des produits selon la catégorie de produits / catégorie d'usage 
def plot_pie_categorie(category, name, image_name):
    df_final = pd.read_csv('data/final_herb_products.csv')
    df_product = df_final.copy()
    df_product[category] = df_product[category].astype(str)

    cate_product = (
        df_product[category]
        .str.split(';').explode().str.strip().value_counts().sort_values(ascending=False)
    )
    label_product = cate_product.index
    data_product = cate_product.values

    fig, ax = plt.subplots(figsize=(6, 4))

    wedges, texts, autotexts = ax.pie(
        data_product,
        labels=None,
        autopct=lambda pct: f"{pct:.1f}%" if pct > 3 else "",
        shadow=None,
        startangle=90
    )
    ax.legend(
        wedges, label_product,
        loc="center right",
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=7
    )

    plt.setp(autotexts, size=7, weight="bold")
    ax.set_title(name)
    current_path = os.getcwd()
    save_pie_image = os.path.join(current_path, image_name)
    fig.savefig(save_pie_image, dpi=300, bbox_inches='tight')
    st.pyplot(fig)


# Analyse le prix moyen par categorie de produit / categorie d'usage
def plot_bar_price(category, name, image_name):
    df_final = pd.read_csv('data/final_herb_products.csv')
    df_exploded = df_final.copy()
    df_exploded[category] = df_exploded[category].str.split(';')
    df_exploded = df_exploded.explode(category)
    df_exploded[category] = df_exploded[category].str.strip()  

    df_mean = (
        df_exploded.groupby(category)
        .agg({'Price (€)': 'mean'})
        .sort_values(by='Price (€)', ascending=False)
    )


    categories = df_mean.index
    mean_prices = df_mean['Price (€)']


    def add_value_labels(ax, bars, spacing=0.5):
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2,
                height + spacing,
                f"{height:.2f}",
                ha='center', va='bottom', fontsize=9
            )


    fig, ax = plt.subplots(figsize=(8,5))
    bars = ax.bar(categories, mean_prices, color='skyblue', edgecolor='gray')
    add_value_labels(ax, bars, spacing=0.5)

    ax.set_ylabel('Prix moyen (€)', fontsize=12)
    ax.set_xlabel('Catégories de produit', fontsize=12)
    ax.set_title(name)
    ax.set_ylim(0, max(mean_prices)*1.2)
    ax.grid(axis='both', linestyle='--', alpha=0.5)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    fig.savefig(image_name, dpi=300)
    st.pyplot(fig)


# Heatmap des 2 categories
def plot_heatmap(image_name):
    df_final = pd.read_csv('data/final_herb_products.csv')
    df_exploded = df_final.copy()
    df_exploded = df_exploded.assign(
        Product_category_exploded = df_exploded['Product category'].str.split('; '),
        Use_category_exploded = df_exploded['Use category'].str.split('; ')
    ).explode('Product_category_exploded').explode('Use_category_exploded')


    heatmap_data = pd.crosstab(
        df_exploded['Product_category_exploded'],
        df_exploded['Use_category_exploded']
    )

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
    ax.set_title("Heatmap: Product category vs Use category")
    ax.set_xlabel("Use category")
    ax.set_ylabel("Product category")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    plt.tight_layout()
    fig.savefig(image_name, dpi=300)
    st.pyplot(fig)




