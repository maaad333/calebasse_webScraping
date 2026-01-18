"""
-------------------------------------------------
Project : Product Data Analysis -- Calebasse Laboratoire
Author  : Xinyi DU
Date    : 2025-10-13
Description :
    Ce script lit les données sauvegardées dans le fichier csv 
    et les analyse en générant des graphes (camembert, barre, boite à moustache)
-------------------------------------------------
"""

import os
import csv 
import pandas as pd 
import matplotlib.pyplot as plt
import streamlit as st


def pei_figure(df, image_name):
    # trouvers les informations de la colonne de catégorie
    category_counts = df['Product category'].value_counts()
    labels = category_counts.index
    data = category_counts.to_numpy()

    # streamlit part
    colors = plt.cm.tab20.colors 
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(
        data,
        labels=None,
        autopct=lambda pct: f"{pct:.1f}%" if pct > 3 else "",
        startangle=90,
        counterclock=False,
        colors=colors[:len(labels)],
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
        textprops={'fontsize': 11, 'color': 'black'}
    )
    ax.legend(
        wedges,
        labels,
        title="Categories",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=11 
    )
    ax.set_title('Répartition des produits par catégorie')
    ax.axis('equal')
    current_path = os.getcwd()
    save_pie_image = os.path.join(current_path, image_name)
    fig.savefig(save_pie_image, dpi=300, bbox_inches='tight')
    st.pyplot(fig)
  
    
def bar_figure(df, image_name):
    # trouver les informations de la colonne de catégorie et de prix
    df_mean = df.groupby("Product category").agg({"Price (€)": "mean"})
    x = df_mean.index
    y = df_mean['Price (€)']

    # streamlit
    fig, ax = plt.subplots(figsize=(8,5))
    bars = ax.bar(df_mean.index, df_mean['Price (€)'], color='skyblue')

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            height + 0.3,
            f"{height:.2f}",
            ha='center', va='bottom', fontsize=9
        )

    ax.set_ylabel('Prix moyen (€)')
    ax.set_xlabel('Catégorie de produit')
    ax.set_title('Prix moyen par catégorie')
    plt.xticks(rotation=45, ha='right')
    current_image = os.getcwd()
    save_bar_image = os.path.join(current_image, image_name)
    fig.savefig(save_bar_image, dpi=300)
    st.pyplot(fig)


def plot_box_visualisation(df, image_name):
    plt.figure(figsize=(8,6))
    df.boxplot(column='Price (€)', by='Product category', grid=False)

    # streamlit 
    fig, ax = plt.subplots(figsize=(8,6))
    df.boxplot(column='Price (€)', by='Product category', grid=False, ax=ax)
    ax.set_title('Distribution du prix par catégorie')
    ax.set_xlabel('Catégorie de produit')
    ax.set_ylabel('Prix (€)')
    plt.suptitle('')
    plt.xticks(rotation=45, ha='right')
    current_path = os.getcwd()
    save_box_image = os.path.join(current_path, image_name)
    fig.savefig(save_box_image, dpi=300)
    st.pyplot(fig)
    




 
