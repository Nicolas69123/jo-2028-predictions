# Plan de projet -- JO 2028 Data Storytelling

**Ref brief :** UF_IADATA_B3.pdf -- "Application data sous forme de data storytelling"
**UF :** SPE Data & IA -- Bachelor 3 YNOV
**Sujet :** Performances sportives pour les JO 2028 a Los Angeles (sujet 3)
**Date de creation :** 2026-03-12
**Derniere mise a jour :** 2026-05-12 -- alignement sur brief officiel

<!-- MODIF (PR #18) : ajout d'une section "Conformite au brief" en tete de
     document. Raison : le PLAN initial avait ete redige librement sans
     verifier ligne a ligne le brief officiel UF_IADATA_B3.pdf (sujet 3).
     Apres relecture, 4 elements explicites du brief manquaient au plan :
     granularite athlete, systeme de cotes, timeline des records, avis users.
     Cette section les reintroduit pour eviter une mauvaise note au jury. -->

---

## Conformite au brief officiel (Sujet 3 -- YPerf)

<!-- Source : enonce officiel page 8 du PDF UF_IADATA_B3.pdf -->
Le brief decrit YPerf, start-up fictive qui veut construire une app de data storytelling pour explorer les performances passees des athletes **par pays, sport et genre**, et predire **les nations ou athletes a suivre en 2028**.

### Objectifs imposes par le brief
<!-- Reproduction litterale des 4 objectifs du brief (page 8).
     Les mots en gras signalent les exigences specifiques sous-jacentes
     que la version initiale du plan ne traitait pas explicitement. -->
1. Analyser les resultats des JO precedents par sport, pays et **genre**
2. Visualiser l'evolution des performances par **discipline**
3. Identifier les **athletes ET pays** en progression par discipline
4. Creer des projectifs sur les JO 2028 bases sur les tendances observees

### Taches imposees par le brief
<!-- Tableau de reconciliation entre les 5 taches du brief et nos 10 phases.
     Permet au jury de verifier en un coup d'oeil que rien n'est oublie.
     Statut au 2026-05-12 : 4 phases sur 10 mergees (PRs #11, #12, #15, #16). -->
| Tache brief | Phase | Statut |
|---|---|---|
| 1. Acquisition + preparation (resultats, medailles, records, athletes) | 2-3 | Fait |
| 2. Analyse exploratoire : medailles + tendances + **athletes marquants / generations montantes** | 4-5 | Phase 4 fait, phase 5 a enrichir |
| 3. Modelisation predictive : modele perf 2028 + **cote athletes/pays par disciplines** | 6-7 | A faire |
| 4. Storytelling visuel : dashboards filtres + **timeline des records** + **visualisation des cotes** + **avis utilisateurs** | 8 | A faire |
| 5. Deploiement local + documentation | 8-9 | A faire |

### Elements specifiques du brief integres dans ce plan
<!-- Liste des 4 elements explicitement nommes dans le brief qui etaient
     absents ou sous-specifies dans la version initiale du PLAN.
     Phase 5 enrichie pour traiter granularite athlete + timeline records.
     Phases 6-7 a enrichir plus tard pour le systeme de cotes (autre PR). -->
- **Granularite athlete** : pas seulement par pays, aussi par athlete individuel (top performers, generations montantes) -- phase 5 + 7
- **Systeme de cote** : scoring probabiliste pour athletes et pour couples pays x discipline -- phase 6-7
- **Timeline des records** : visualisation chronologique des records olympiques -- phase 5 ou 8
- **Avis utilisateurs** : formulaire dans l'app Streamlit avec stockage local -- phase 8

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

<!-- MODIF (PR #18) : enrichissement de la Phase 5 pour couvrir les exigences
     manquantes du brief officiel :
     - Chapitre 1 augmente avec "timeline interactive Plotly des records"
       (tache 4 du brief : "Timeline des records")
     - Chapitres 5 et 6 ajoutes pour traiter la granularite athlete
       (objectif 3 du brief : "Identifier les athletes ET pays en progression")
     - Bullet "Analyse genre" ajoute pour couvrir l'objectif 1
       (analyse par "sport, pays et genre") -->
### PHASE 5 -- Analyse exploratoire + storytelling
- [ ] Notebook 04_exploration.ipynb
- [ ] Narration Markdown riche entre les cellules
- [ ] Chapitre 1 : "128 ans de competition" (timeline globale + timeline interactive Plotly des records)
- [ ] Chapitre 2 : "Les empires sportifs" (domination par pays, par discipline, par genre)
- [ ] Chapitre 3 : "Evolution des disciplines" (tendances, nouvelles disciplines, disparues)
- [ ] Chapitre 4 : "Paris 2024" (focus resultats recents)
- [ ] Chapitre 5 : **"Les athletes qui ont marque l'histoire"** -- top performers par discipline, palmares records, decennie par decennie
- [ ] Chapitre 6 : **"Generations montantes"** -- detection des athletes en progression sur leurs 2-3 dernieres olympiades (criteres : age, ratio medailles/participations, evolution rang)
- [ ] Analyse genre : ecart H/F dans la participation et les medailles, evolution depuis 1900
- [ ] Graphiques varies : barplots, heatmaps, line charts, scatter, choroplethe, **timeline interactive des records**
- [ ] Mix matplotlib + seaborn + plotly
- [ ] Commit + push
- **Validation :** >15 graphiques, narration fluide, axe genre couvert, athletes marquants identifies

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
