# Architecture et choix techniques

## Vue d'ensemble

```
CSV bruts (data/)
   |  01_acquisition : controles de coherence
   v
02_preparation : nettoyage + agregation + enrichissement
   |            -> data/processed/medals_per_country_sport.csv (unique dataset)
   |
   +--> 02b_exploration : stats descriptives + inferentielles (lecture seule)
   v
03_modelisation : 3 Ridge + comparaison + projection 2028 + bootstrap IC
   |            -> models/medal_predictor.pkl
   |            -> data/processed/projection_2028_*.csv
   v
app/build.py : export de 6 JSON
   v
app/dist/ : site statique (HTML + Plotly.js)
   v
GitHub Pages (deploiement automatique via Actions)
```

## Choix justifies

### Notebooks Jupyter pour le pipeline
Exiges par le brief ("Jupyter Notebook retracant la demarche"). Chaque etape
est un notebook autonome, relancable par `nbconvert --execute`, avec du
markdown qui documente les decisions au fil de l'eau.

### Un dataset unique en sortie de preparation
`medals_per_country_sport.csv` (~7 000 lignes) est la seule interface entre la
preparation et tout le reste (exploration, modelisation, build). Reduit le
couplage et rend chaque notebook testable isolement.

### Site statique plutot que Streamlit
Le brief demande une application "deployee localement" au minimum. Un site
statique HTML + Plotly.js :
- se deploie gratuitement sur GitHub Pages (URL publique permanente, un plus
  pour la demo au jury),
- ne necessite aucun serveur Python en production,
- reste interactif (selecteur multi-pays, graphes zoomables, filtres).
Le cout : la logique d'affichage est en JavaScript, et les donnees doivent
etre pre-exportees en JSON par `build.py`.

### Trois modeles Ridge plutot qu'un MultiOutput
Le brief demande une prediction par type de medaille. Trois modeles
independants permettent un alpha optimal par couleur et des coefficients
directement interpretables couleur par couleur.

### Split temporel strict
Train 1968-2016, test 2024. Un random split surestimerait les performances :
les lignes de la meme edition partagent de l'information (data leakage).

### Serialisation joblib d'un bundle unique
`medal_predictor.pkl` contient les 3 modeles, les colonnes de features, les
metriques, la comparaison de modeles et les quantiles bootstrap. Un seul
artefact a charger pour `build.py` et les tests : pas de derive entre modele
et metadonnees.

### Tests pytest en 3 modules
- `test_data_quality.py` : les invariants des donnees (coherence Or+Argent+Bronze
  = Total, pas de doublons, validation CIO 2024). Executables en CI.
- `test_model.py` : garde-fou anti-regression (R2 pays > 0.80), coherence de la
  projection et des fourchettes. Skippes en CI (artefacts gitignores).
- `test_app_build.py` : contrat des 6 JSON consommes par le frontend.

### CI/CD GitHub Actions
- `tests.yml` : pytest sur chaque push/PR.
- `deploy-pages.yml` : publication de `app/dist/` sur GitHub Pages a chaque
  modification.

## Conventions

- Branches `feature/*`, `fix/*`, `update/*` + pull requests vers `main`.
- Commits imperatifs prefixes (`feat:`, `fix:`, `test:`, `docs:`, `ci:`).
- `data/processed/` et `models/*.pkl` gitignores : seuls le code et les
  sources brutes sont versionnes, les artefacts se regenerent.
