# JO 2028 Predictions — YPerf

Application de data storytelling qui predit le tableau des medailles des Jeux
Olympiques de Los Angeles 2028, a partir de 128 ans d'historique olympique.

**Site en ligne : https://nicolas69123.github.io/jo-2028-predictions/**

Projet realise dans le cadre de l'UF SPE Data & IA (Bachelor 3 Ynov) —
sujet 3 : "Performances sportives pour les JO 2028 a Los Angeles".

## Resultats cles

| Indicateur | Valeur |
|---|---|
| R2 au niveau pays (test Paris 2024, jamais vu a l'entrainement) | 0.88 |
| RMSE au niveau pays | 4.4 medailles |
| Editions couvertes | 30 (1896-2024) |
| Pays / sports | 158 / 70 |
| Modeles | 3 Ridge (Or, Argent, Bronze) |

Prediction phare : les USA, pays hote, en tete avec ~110 medailles
(fourchette P10-P90 : 31-150, obtenue par bootstrap des residus).

## Architecture

```
notebooks/
  01_acquisition.ipynb     Chargement et controle des 4 sources
  02_preparation.ipynb     Nettoyage, deduplication, agregation, enrichissement
  02b_exploration.ipynb    Analyse exploratoire + statistiques inferentielles
  03_modelisation.ipynb    3 Ridge + comparaison RF/XGBoost + projection 2028 + IC
data/
  JO_resultats.csv         Medailles 1896-2024 (24 000 lignes)
  JO2028_sports.csv        Programme officiel LA 2028
  JO_date_ete.csv          Table de reference des editions d'ete
  PIB_par_habitant.csv     PIB/habitant Banque Mondiale (1960-2024)
  processed/               Sorties du pipeline (gitignore)
models/                    Bundle des 3 modeles Ridge (gitignore)
app/
  build.py                 Export des JSON pour le frontend
  dist/                    Site statique (HTML + Plotly), deploye sur GitHub Pages
tests/                     Suite pytest (26 tests)
docs/                      Documentation detaillee
```

## Installation et reproduction

```bash
git clone https://github.com/Nicolas69123/jo-2028-predictions.git
cd jo-2028-predictions
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Pipeline complet (dans l'ordre)
jupyter nbconvert --to notebook --execute --inplace notebooks/01_acquisition.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/02_preparation.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/02b_exploration.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/03_modelisation.ipynb
python app/build.py

# Tests
python -m pytest tests/ -v

# Site en local
cd app/dist && python -m http.server 8765
# puis ouvrir http://localhost:8765
```

Note macOS : XGBoost necessite OpenMP (`brew install libomp`).

## Documentation

- [docs/SOURCES.md](docs/SOURCES.md) — les 4 sources de donnees et leur validation
- [docs/METHODOLOGIE.md](docs/METHODOLOGIE.md) — demarche scientifique de bout en bout
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — choix techniques justifies
- [PLAN.md](PLAN.md) — plan de projet et suivi

## Stack

Python 3.12+, pandas, scikit-learn, XGBoost, scipy, matplotlib/seaborn (notebooks),
Plotly.js (site), pytest, GitHub Actions (CI + deploiement Pages).

## Auteurs

Nicolas Chalopin et Frederic Somas — Bachelor 3 Ynov, promotion 2025-2026.
