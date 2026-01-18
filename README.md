# 🧪 Calebasse Laboratoire — Projet de Scraping et d’Analyse de Produits

Ce projet vise à **extraire, traiter et analyser** les données des produits (alimentaires et équipements) du site **Calebasse Laboratoire**, un site de produits de soins aisatiques.  
Pour les produits alimentaires, les informations collectées concernent : le nom du produit, le prix, la catégorie et le service.
Pour les produits d'équipements, les informations collectées concernent: le nom du produit, le prix et la catégorie.
Les résultats d’analyse sont ensuite présentés à travers une application **Streamlit** interactive.


## 📂 Structure du projet
```
   projet/
   │
   ├── data/ # Données sources et transformées
   │ ├── raw_use_products.csv # Données brutes : données brutes extraites des produits alimentaires
   │ ├── raw_physical_products.csv # Données brutes : données brutes extraites des produits des équipements
   │ ├── raw_herbal_products.csv # Données brutes : données mergées des produits alimentaires
   │ ├── final_herb_products.csv # Données nettoyées : données finales des produits alimentaires
   │ ├── final_process_equipement.csv# Données nettoyées : données traitées finales des produits des équipements
   │ └── processed-data.csv # Jeu de données final unifié
   │
   ├── code/
   │ ├── scrap_herbal.py # Script de scraping des produits alimentaires
   │ ├── scrap_equipement.py # Script de scraping des produits des équipements
   │ ├── process_herbal.py # Script de nettoyage et formatage des données alimentaires
   │ ├── process_equipement.py # Script de nettoyage et formatage des données d’équipements
   │ ├── analyse_herbal.py # Analyse statistique des produits alimentaires
   │ ├── analyse_equipement.py # Analyse statistique des produits d'équipements
   │ └── main.py # Application Streamlit : visualisation et interface interactive
   │
   ├── demo/
   │ ├── images/ # Visualisations générées et commentaires
   │ └── videos/ # Vidéo de démonstration (≈ 1 min)
   │
   ├── requirements.txt # Liste des dépendances Python
   └── README.md # Présentation, étapes et discussion finale
```

## 🎯 Objectifs du projet

1. **Scraping des données**  
   - Collecte automatisée des produits depuis le site Calebasse Laboratoire.  
   - Pour les produits d'équipements: Extraction du *nom*, du *prix* et de la *catégorie*.
   - Pour les produits alimentaires: Extraction du *nom*, du *prix*, de la *catégorie* et du *service*.

2. **Processe de nettoyage et traitement**  
   - Suppression des doublons et des valeurs manquantes.  
   - Uniformisation des produits de même nom mais classifiés dans des différentes catégories.

3. **Analyse statistique et visuelle**  
   - Répartition des produits par catégorie (diagramme circulaire).  
   - Distribution des prix et comparaison entre catégories et entre services (seulement pour les produits alimentaires).  
   - Calculs des prix moyens des produits en fonction de la catégorie.

4. **Visualisation interactive (Streamlit)**  
   - Interface permettant d’explorer les données nettoyées.  
   - Graphiques dynamiques et tableaux filtrables.


## ⚙️ Installation et environnement
- requirements.txt


### Prérequis
- Python ≥ 3.10 
- Accès Internet pour le scraping


## 🌐 Conclusion des résultats
D'apres le graphique de répartition des produits par grandes catégories, les produits alimentaires représentent la majorité de l'offre du site, avec environ 61,5 % des références totales. Les produits matériels occupent une place significative et diversifiée. 

En observant la répartition des produits matériels par catégorie, on constate que la catégorie "livres" domine largement avec 43.2% des produits, suivi de près par l'acupuncture (25,9%). Les autres catégories comme décoration, peau et moxibustion, présentent des parts plus modestes, mais contribuent à la variété de l'offre.

Concernant le prix moyen par catégorie, il apparaît que les produits kit affichent le prix moyen le plus élevé (environ 191 €), bien au-dessus des autres catégories. Cette catégorie se distingue également par une forte variabilité des prix, ce qui suggère la présence de produits aux gammes très différentes (de base à haut de gamme).
Les catégories “cooker” (39,4 €), “decorative” (57,3 €) et “books” (33 €) présentent des prix moyens modérés, tandis que les produits “acupuncture”, “skin” et “moxibustion” se situent dans les tranches les plus basses (autour de 11 à 12 €), reflétant probablement des produits plus standards ou consommables.

En observant la répartition des produits des catégories de produits à base de plantes, on constate "TMC Herbs" occupe la plus grande part avec 36,0 %, ce qui montre qu’il s’agit de la catégorie principale. Viennent ensuite "Bulk plantes" (13,4 %) et "Others" (12,6 %), également importantes mais à un niveau nettement inférieur. Les groupes tels que "Bio" (8,1 %), "Homemade blends" (6,7 %) et "Plant powder" (6,2 %) représentent des parts moyennes, reflétant une certaine diversité dans la gamme de produits. Les autres catégories, comme "Flower infusions" (5,5 %), "Food supplements" (5,2 %), "Mushroom" (3,2 %) ainsi que "Foot baths", "Congees" et "Tea", n’occupent qu’une très petite portion. Dans l’ensemble, le graphique montre une forte concentration sur une catégorie principale (TMC Herbs), tandis que les autres traduisent une stratégie de diversification destinée à répondre à divers besoins du marché.

En observant la répartition des catégories d’usage des produits à base de plantes, on constate que la catégorie "Others" occupe la plus grande part avec 27,0 %, indiquant une proportion importante de produits ne correspondant pas à d’autres groupes spécifiques. Elle est suivie par "Fatigue and Energy" (12,7 %), traduisant une forte demande pour les produits favorisant l’énergie et la réduction de la fatigue. Les catégories "Digestion" (7,9 %), "Calm and well-being" (7,6 %), "Respiratory comfort" (7,5 %) et "Female balance" (6,3 %) représentent des parts moyennes, illustrant l’intérêt des consommateurs pour la santé digestive, le bien-être mental, le confort respiratoire et l’équilibre hormonal féminin. D’autres segments tels que "Detox and drainer" (5,8 %), "Beauty and slimming" (5,1 %) et "Urinary comfort" (4,5 %) ont également une présence notable. Les catégories restantes – "Articulations and muscles", "Cardiovascular health","Circulation", "Sexual vitality", "Male balance" et "MTV" – ne représentent qu’une petite fraction (environ 3 à 4 % chacune). Globalement, les usages des produits à base de plantes sont très diversifiés, mais se concentrent principalement sur l’énergie, le bien-être général et la santé globale, tandis que les besoins plus spécifiques occupent une part plus réduite.

Concernant le prix moyen par catégorie, on observe une différence marquée entre les différentes catégories. La catégorie ayant le prix moyen le plus élevé est "Food supplements" avec 38,45 €, nettement supérieure aux autres. Elle est suivie par "Others" (24,50 €), "Foot baths" (20,39 €) et "Plant powder" (20,34 €), qui affichent également des prix relativement élevés. Les catégories "Congees" (14,12 €) et "Homemade blends" (13,00 €) se situent dans la moyenne. En revanche, les produits comme "Flower infusions" (10,07 €), "Bio" (9,97 €), "Mushroom" (9,87 €), "Bulk plantes" (9,65 €) et "Tea"(8,38 €) présentent les prix les plus bas. Ainsi, les produits à valeur ajoutée, notamment les compléments alimentaires, sont nettement plus coûteux que les produits plus courants ou naturels comme le thé.

Selon le graphique qui illustre le prix moyen des produits selon leur usage, on observe une variation significative entre les différentes catégories. La catégorie "MTV" présente le prix moyen le plus élevé, atteignant 29,40 €, bien au-dessus des autres. Elle est suivie par "Calm and well-being" (20,48 €) et "Sexual vitality" (20,07 €), deux usages liés au bien-être mental et à la vitalité, qui affichent également des prix élevés. Les catégories "Cardiovascular health" (16,78 €), "Articulations and muscles" (16,76 €), "Beauty and slimming" (16,67 €), "Female balance" (16,57 €) et "Circulation" (15,67 €) se situent dans la moyenne. En revanche, les produits destinés à la fatigue et l’énergie (15,24 €), au drainage ou détox (14,09 €), à la digestion (13,19 €), au confort respiratoire (13,08 €), ou encore au confort urinaire (12,48 €) présentent les prix les plus bas. Ainsi, les produits visant des besoins spécifiques, notamment la vitalité et le bien-être, sont globalement plus chers que ceux destinés à des usages plus courants comme la digestion ou le drainage.











