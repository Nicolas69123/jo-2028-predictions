# Plan de projet -- JO 2028 (version simplifiee)

**Ref brief :** UF_IADATA_B3.pdf -- "Application data sous forme de data storytelling"
**UF :** SPE Data & IA -- Bachelor 3 YNOV
**Sujet :** Performances sportives pour les JO 2028 a Los Angeles (sujet 3)
**Date de creation :** 2026-03-12
**Refonte :** 2026-05-12 -- scope reduit pour focus sur la prediction
**Finalisation :** 2026-07-06 -- PIB, EDA statistique, comparaison de modeles, IC bootstrap, tests, docs

---

## Objectif simplifie

Le brief demande de **predire les performances sportives pour LA 2028**.
On se concentre sur **deux predictions principales** :

1. **Quel sera le pays gagnant** (classement final Or/Argent/Bronze) ?
2. **Quelles seront les medailles par sport et par type** pour chaque pays ?

On n'a donc PAS besoin :
- Des informations individuelles des athletes (age, taille, poids, genre)
- Des analyses biographiques et stats biometriques
- Des chapitres "athletes marquants" ou "generations montantes"

Cette simplification permet de :
- **Reduire drastiquement la taille des donnees** (1 fichier de 6 871 lignes au lieu de 308 000)
- **Aller plus vite** sur le coeur du brief (prediction)
- **Avoir un modele plus interpretable** (3 modeles Ridge simples au lieu de pipelines complexes)

---

## Architecture finale

```
notebooks/
  01_acquisition.ipynb   -- charge et controle les 4 sources (dont PIB via API Banque Mondiale)
  02_preparation.ipynb   -- nettoyage + agregation + enrichissement -> 1 fichier unique
  02b_exploration.ipynb  -- EDA + statistiques inferentielles (effet hote, correlations)
  03_modelisation.ipynb  -- 3 Ridge + comparaison RF/XGBoost + projection 2028 + IC bootstrap

data/
  raw/                   -- CSV bruts telecharges automatiquement (gitignored)
  processed/
    medals_per_country_sport.csv   -- dataset unique (6 871 lignes)
    projection_2028_country.csv    -- classement predit LA 2028
    projection_2028_per_sport.csv  -- cote par (pays, sport)

models/
  medal_predictor.pkl    -- bundle des 3 modeles Ridge

app/
  build.py               -- script qui exporte les JSON pour le frontend
  dist/                  -- site web statique (3 pages HTML)
    index.html           -- accueil
    predict.html         -- classement + cote par discipline (interactif)
    methodology.html     -- demarche scientifique
    data/                -- 6 fichiers JSON (KPIs, projections, metriques)
    assets/              -- images JO + CSS
```

---

## Pipeline de bout en bout

### 1. Acquisition (`01_acquisition.ipynb`)
- Chargement des 4 sources : JO_resultats, JO2028_sports, JO_date_ete (versionnees)
  et PIB_par_habitant (API open data Banque Mondiale, versionne, retelecharge si absent)
- Verification de coherence (NOC, periode, valeurs manquantes, doublons)

### 2. Preparation (`02_preparation.ipynb`)
- Filtrage JO d'ete uniquement
- Deduplication (bugs scraping connus : Sailing 1900, Golf 1904)
- Integration Paris 2024 depuis olympics_1896_2024.csv (avec deduplication des athletes equipe)
- Agregation par (NOC, Year, Sport) -> Gold/Silver/Bronze/Total
- Enrichissement avec population, PIB/habitant (Banque Mondiale) et continent

### 3. Modelisation (`03_modelisation.ipynb`)
- Grille complete (NOC x Year x Sport) avec zeros
- Feature engineering : lag_1, lag_2, rolling_3 par couleur + is_host + log_population + log_gdp + Continent
- 3 modeles Ridge entraines independamment (Or, Argent, Bronze)
- GridSearchCV sur alpha (regularisation L2)
- Comparaison chiffree Ridge vs RandomForest vs XGBoost (memes features, meme split)
- Split temporel : train 1968-2016, test 2024
- Intervalles de confiance P10-P90 par bootstrap des residus relatifs (B=2000)
- Sauvegarde du bundle complet + projection LA 2028

### 4. Application (`app/`)
- `build.py` exporte les donnees agregees en JSON
- Site HTML statique avec graphes Plotly interactifs
- Page predict : tableau classement + selecteur pays interactif pour la cote par discipline

---

## Performance du modele

| Niveau | Metric | Valeur |
|---|---|---|
| (pays, sport) granulaire | R² | 0.52 |
| (pays, sport) granulaire | MAE | 0.08 medaille |
| **Pays agrege** | **R²** | **0.88** |
| **Pays agrege** | **RMSE** | **4.4 medailles** |

Comparaison de modeles (test Paris 2024) : XGBoost fait mieux au niveau pays
(RMSE 3.6, R² 0.92) mais sur une seule edition de test ; Ridge est conserve pour
son interpretabilite et sa stabilite (details : docs/METHODOLOGIE.md).

## Source des donnees

Source primaire : **`olympics_1896_2024.csv`** (DjangoMustang/Olympics-1896-2024-Tableau).
Choisie apres audit : match exact CIO sur 2016, 2020 et 2024 (les 3 dernieres editions).
Quelques editions plus anciennes presentent +/-1 medaille par rapport au classement CIO actuel
en raison de **reattributions post-Jeux** (DSQ pour dopage revelees apres coup), que les datasets
publics ne refletent pas en temps reel.

Le R² granulaire est faible car 90% des couples (pays, sport) sont des zeros.
La metrique vraiment significative est **MAE = 0.08** (le modele se trompe en moyenne
de moins de 0.1 medaille par couple) et **R² pays = 0.85** (le classement final est
predit avec une bonne fiabilite).

---

## Top 10 LA 2028 predit

| Rang | Pays | Or | Argent | Bronze | Total | Fourchette P10-P90 |
|---|---|---|---|---|---|---|
| 1 | USA (hote) | 43 | 37 | 30 | 110 | 31-150 |
| 2 | Chine | 28 | 18 | 16 | 63 | 18-86 |
| 3 | Japon | 15 | 9 | 11 | 35 | 10-48 |
| 4 | Grande-Bretagne | 13 | 16 | 16 | 45 | 13-61 |
| 5 | Australie | 11 | 9 | 12 | 32 | 9-44 |
| 6 | Italie | 10 | 10 | 12 | 32 | 9-44 |
| 7 | France | 10 | 14 | 12 | 36 | 10-48 |
| 8 | Pays-Bas | 8 | 7 | 8 | 23 | 6-31 |
| 9 | Allemagne | 8 | 9 | 11 | 29 | 8-39 |
| 10 | Coree du Sud | 8 | 5 | 8 | 21 | 6-29 |

---

## Choix methodologiques cles

### Pourquoi un split temporel ?
Pas de random split : risque de data leakage (le modele "voit" partiellement le futur).
Train sur 1968-2016, test sur Paris 2024 (jamais vu a l'entrainement).

### Pourquoi 3 modeles separes ?
Le brief demande de predire par **type de medaille**. Trois Ridge independants
(un par couleur) offrent une meilleure interpretabilite que un MultiOutput.

### Pourquoi Ridge et pas RF/XGBoost ?
Avec seulement 13 annees d'entrainement, les modeles complexes overfittent.
Ridge avec regularisation L2 forte (alpha eleve) generalise mieux.

### Pourquoi pas de prediction des athletes ?
Le brief mentionne "athletes a suivre" mais cette information est tres bruitee
(carrieres courtes, blessures imprevisibles). Notre approche se limite a la cible
**(pays, sport)** qui est plus stable et plus utile pour les projections.

---

## Limites assumees

- **Nouveaux sports 2028** (cricket, lacrosse, flag football, baseball, squash) :
  pas d'historique, donc impossibles a predire.
- **Effet pays hote modelise simplement** (variable binaire), sans capter l'amplitude
  exacte (Chine 2008 a eu un boost different de Bresil 2016).
- **Incertitude quantifiee mais large** : fourchettes P10-P90 par bootstrap des
  residus du test 2024, sous hypothese de stationnarite des erreurs.

---

## Reproductibilite

Pour reproduire le projet depuis zero :

```bash
git clone https://github.com/Nicolas69123/jo-2028-predictions.git
cd jo-2028-predictions
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute notebooks/01_acquisition.ipynb
jupyter nbconvert --to notebook --execute notebooks/02_preparation.ipynb
jupyter nbconvert --to notebook --execute notebooks/02b_exploration.ipynb
jupyter nbconvert --to notebook --execute notebooks/03_modelisation.ipynb
python app/build.py
# Site dans app/dist/, lancer un serveur local :
cd app/dist && python -m http.server 8765
# Ouvrir http://localhost:8765
```
