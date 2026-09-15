# Cellule de recrutement — Streamlit

Mini-projet de datavisualisation construit avec Streamlit à partir du dataset `all_players_clean.csv`.

## Question métier
L'application aide une cellule de recrutement à explorer le vivier de joueurs, appliquer des critères globaux et identifier des profils adaptés.

## Fonctionnalités
- filtres globaux catégoriels : championnat, nation, poste, équipe, pied préféré, genre et postes alternatifs ;
- filtres numériques principaux et avancés ;
- page Synthèse avec KPI, constats automatiques et meilleurs profils ;
- analyse univariée adaptée au type de variable ;
- analyse bivariée : quanti×quanti, quali×quanti et quali×quali ;
- analyse multivariée : corrélations et relation avec couleur/taille ;
- profil joueur avec caractéristiques, radar, percentiles et comparaison.

## Choix graphiques
Une variable quantitative est décrite par sa distribution. Une qualitative est résumée par ses effectifs.
Deux quantitatives sont comparées par un nuage de points ; une quantitative et une qualitative par un boxplot.
Deux qualitatives sont croisées par une heatmap d'effectifs. Les corrélations utilisent une matrice divergente centrée sur zéro.

## Normalisation du profil
Les notes EA étant déjà principalement sur une échelle 0–100, le radar absolu ne nécessite pas de normalisation supplémentaire.
Un second radar transforme les notes en percentiles par rapport au même poste, au même championnat ou à tous les joueurs.

## Limites
Les statistiques décrivent le dataset disponible et ne remplacent pas une observation terrain. Les percentiles dépendent du groupe de référence et les données peuvent contenir des valeurs manquantes.

## Installation
```bash
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install -r requirements.txt
```

## Lancement
```bash
python -m streamlit run main.py
```

## Navigation
La navigation principale est affichée horizontalement sous le titre sous forme d'onglets visibles : Synthèse, Analyse univariée, Analyse bivariée, Analyse multivariée et Profil joueur. La barre latérale est réservée aux filtres globaux, qui restent actifs dans tous les onglets.

## Valeur marchande via Live Football API

L'application utilise d'abord les colonnes `Valeur Marchande` et `API_Player_ID` du fichier local. Si la valeur est absente, le profil joueur peut être enrichi via Live Football API puis la valeur et l'identifiant sont sauvegardés dans le CSV afin d'éviter de consommer de nouveaux crédits lors des consultations suivantes.

1. Créer `.streamlit/secrets.toml` à partir de `.streamlit/secrets.toml.example`.
2. Renseigner `FOOTBALL_API_KEY = "..."`.
3. Installer les dépendances avec `pip install -r requirements.txt`.

En cas d'homonyme, l'application compare le nom, la nationalité, le club et l'âge. Si la correspondance reste ambiguë, elle demande une confirmation avant d'enregistrer le joueur API.
