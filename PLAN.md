# Plan de projet -- JO 2028 Data Storytelling

**Ref brief :** UF_IADATA_B3.pdf -- "Application data sous forme de data storytelling"
**UF :** SPE Data & IA -- Bachelor 3 YNOV
**Sujet :** Performances sportives pour les JO 2028 a Los Angeles (sujet 3)
**Date de creation :** 2026-03-12

---

## Contraintes du brief

- Groupe de 2
- Stack obligatoire : Python, pandas, scikit-learn, matplotlib/seaborn, Plotly, Streamlit ou Dash
- Deploiement local
- 2 oraux : intermediaire (coef 1) + final (coef 3)

## Livrables exiges

1. Depot Git avec tout le code et la documentation
2. Jupyter Notebook retracant la demarche et les analyses
3. Application de data storytelling deployee localement
4. Documentation technique du projet et manuel d'installation et utilisation

## Grille d'evaluation -- Oral intermediaire (coef 1)

| Critere | Description | Pond. |
|---|---|---|
| Git et GitHub | Branches, commits, PRs, collaboration | 3 |
| Gestion de projet | Outils adaptes (Trello, Notion, ClickUp...) | 4 |
| Justifier demarche et choix techniques | Formaliser besoins, strategie, technologies | 5 |
| Presenter un projet a l'oral | Presentation claire, convaincante | 5 |
| Posture professionnelle | Autonomie, rigueur, respect des contraintes | 3 |

## Grille d'evaluation -- Oral final (coef 3)

| Critere | Description | Module de cours | Pond. |
|---|---|---|---|
| Acquerir des donnees | Sources ouvertes, API, base de donnees | Analyse + Python avance | 4 |
| Preparer et nettoyer | Doublons, valeurs manquantes, standardisation | Analyse + Python avance | 3 |
| Explorer et analyser | Analyse pertinente, criteres selectionnes | Analyse + Maths DataScience | 3 |
| Visualiser | Visualisations claires, informatives, adaptees | Analyse + Python avance | 3 |
| Modele ML + evaluer | Regression, classification, clustering + metriques | Analyse + Maths DataScience | 4 |
| Predire + recommandations | Projections, simulations, scenarios | Analyse + Maths DataScience | 4 |
| Interface interactive | Fonctionnelle, intuitive, deployee localement | Python avance | 2 |
| Documenter | Demarche, choix techniques, installation, utilisation | Analyse | 2 |

## Notation

| Non acquis | En cours d'acquisition | Partiellement acquis | Acquis | Maitrise |
|---|---|---|---|---|
| 0 | 8 | 12 | 15 | 20 |

Note finale = competence * ponderation

---

## Donnees disponibles (data/raw/)

| Fichier | Lignes | Contenu | Source |
|---|---|---|---|
| bios.csv | 145 500 | Biographies athletes | KeithGalli/Olympics-Dataset |
| bios_locs.csv | 145 500 | Bios + geolocalisation | KeithGalli/Olympics-Dataset |
| results.csv | 308 407 | Resultats par epreuve (1896-2022) | KeithGalli/Olympics-Dataset |
| olympics_1896_2024.csv | 24 012 | Medailles 1896-2024 (incl. Paris) | DjangoMustang/Olympics-1896-2024-Tableau |
| noc_regions.csv | 229 | Mapping NOC -> pays | KeithGalli/Olympics-Dataset |
| populations.csv | 266 | Population par pays (1960-2023) | KeithGalli/Olympics-Dataset (World Bank) |
| city_locations.csv | 55 | Coordonnees villes hotes | DjangoMustang/Olympics-1896-2024-Tableau |

---

## Etapes de realisation

### PHASE 1 -- Setup projet
- [ ] Creer le repo GitHub (Nicolas69123)
- [ ] Structure du projet, .gitignore, requirements.txt
- [ ] Premier commit + push
- **Validation :** repo accessible sur GitHub

### PHASE 2 -- Acquisition des donnees
- [ ] Notebook 01_acquisition.ipynb
- [ ] Charger les 7 CSV, documenter chaque source (URL, licence, description)
- [ ] Verifier la coherence, afficher les shapes et dtypes
- [ ] Sauvegarder les donnees brutes consolidees
- [ ] Commit + push
- **Validation :** notebook executable sans erreur, sources citees

### PHASE 3 -- Preparation et nettoyage
- [ ] Notebook 02_nettoyage.ipynb
- [ ] Analyse des valeurs manquantes (heatmap, pourcentages)
- [ ] Gestion des doublons
- [ ] Standardisation NOC, types de donnees
- [ ] Imputation (mediane par sport/sexe pour age, taille, poids)
- [ ] Visualisations qualite avant/apres
- [ ] Export data/processed/
- [ ] Commit + push
- **Validation :** dataset propre, zero doublon, colonnes typees

### PHASE 4 -- Statistiques (Maths pour la DataScience)
- [ ] Notebook 03_statistiques.ipynb
- [ ] Statistiques descriptives completes (mean, median, std, quartiles)
- [ ] Indicateurs univaries et multivaries
- [ ] Matrice de correlation
- [ ] Test du chi-2 (repartition medailles vs continent)
- [ ] Test t de Student/Welch (progression France 2000-2024)
- [ ] Intervalles de confiance
- [ ] ACP (Analyse en Composantes Principales)
- [ ] Commit + push
- **Validation :** tests statistiques avec p-values, interpretations

### PHASE 5 -- Analyse exploratoire + storytelling
- [ ] Notebook 04_exploration.ipynb
- [ ] Narration Markdown riche entre les cellules
- [ ] Chapitre 1 : "128 ans de competition" (timeline)
- [ ] Chapitre 2 : "Les empires sportifs" (domination par pays)
- [ ] Chapitre 3 : "Evolution des disciplines" (tendances)
- [ ] Chapitre 4 : "Paris 2024" (focus resultats recents)
- [ ] Graphiques varies : barplots, heatmaps, line charts, scatter, choroplethe
- [ ] Mix matplotlib + seaborn + plotly
- [ ] Commit + push
- **Validation :** >15 graphiques, narration fluide

### --- ORAL INTERMEDIAIRE (phases 1-5) ---

### PHASE 6 -- Modelisation ML
- [ ] Notebook 05_modelisation.ipynb
- [ ] Feature engineering (medailles cumulees, tendance, GDP, population, is_host...)
- [ ] Split temporel train/test (pas random, par annee)
- [ ] Comparaison 3+ modeles : Ridge, Random Forest, XGBoost
- [ ] GridSearchCV pour hyperparameter tuning
- [ ] Metriques : RMSE, MAE, R2
- [ ] Tableau comparatif des performances
- [ ] Feature importance
- [ ] Sauvegarde modele (joblib -> models/medal_predictor.pkl)
- [ ] Commit + push
- **Validation :** 3 modeles compares, metriques documentees, modele serialise

### PHASE 7 -- Predictions 2028
- [ ] Notebook 06_predictions_2028.ipynb
- [ ] Charger le modele
- [ ] Predictions par pays pour LA 2028
- [ ] Top 10 pays predits
- [ ] Focus France par discipline
- [ ] Recommandations ("investir dans tel sport")
- [ ] Scenarios what-if (boycott, nouveaux sports, effet pays hote)
- [ ] Visualisations de synthese
- [ ] Commit + push
- **Validation :** predictions coherentes, recommandations argumentees

### PHASE 8 -- Application Streamlit
- [ ] app.py (accueil + KPIs)
- [ ] pages/01_explorer.py (filtres, timeline, carte, top pays, distributions)
- [ ] pages/02_comparer.py (face-a-face 2 pays, radar chart)
- [ ] pages/03_predire.py (predictions ML, sliders, top 10, recommandations)
- [ ] Test local : `streamlit run app.py`
- [ ] Commit + push
- **Validation :** app fonctionnelle, toutes les pages sans erreur

### PHASE 9 -- Documentation
- [ ] docs/README.md (installation, utilisation, stack, sources)
- [ ] docs/SOURCES.md (toutes les sources avec URLs)
- [ ] docs/METHODOLOGIE.md (demarche scientifique)
- [ ] docs/ARCHITECTURE.md (choix techniques justifies)
- [ ] Support de presentation (slides pour oral final)
- [ ] Commit + push
- **Validation :** README clair, installation reproductible

### PHASE 10 -- Tests + polish final
- [ ] Tests pytest (qualite donnees, preprocessing, model, app)
- [ ] Verification de tous les notebooks (run complet sans erreur)
- [ ] Verification de l'app Streamlit
- [ ] Nettoyage code, derniers commits
- [ ] Tag release sur GitHub
- **Validation :** tous les tests passent, app deployable

---

## Progression

| Phase | Statut | Date |
|---|---|---|
| Phase 1 -- Setup | A faire | |
| Phase 2 -- Acquisition | A faire | |
| Phase 3 -- Nettoyage | A faire | |
| Phase 4 -- Statistiques | A faire | |
| Phase 5 -- Exploration | A faire | |
| ORAL INTERMEDIAIRE | A faire | |
| Phase 6 -- Modelisation | A faire | |
| Phase 7 -- Predictions | A faire | |
| Phase 8 -- Streamlit | A faire | |
| Phase 9 -- Documentation | A faire | |
| Phase 10 -- Tests | A faire | |
| ORAL FINAL | A faire | |
