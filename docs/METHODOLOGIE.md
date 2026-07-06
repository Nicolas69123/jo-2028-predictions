# Methodologie

Demarche scientifique de bout en bout, du CSV brut a la prediction publiee.

## 1. Acquisition (notebook 01)

Quatre sources chargees et controlees : couverture temporelle, valeurs manquantes,
distribution des types de medailles, coherence des codes pays. Le PIB est acquis
via l'API Banque Mondiale (open data) et versionne pour la reproductibilite.

## 2. Preparation (notebook 02)

1. **Filtre JO d'ete** par jointure sur la table de reference des editions
   (aucune liste d'annees en dur).
2. **Deduplication** des medailles d'equipe : une medaille de relais apparait
   une fois par athlete dans la source ; on la compte une seule fois par
   (epreuve, pays), conformement au comptage CIO.
3. **Normalisation** des noms de sports (variations d'ecriture entre editions).
4. **Agregation** par (annee, pays, sport) -> Gold / Silver / Bronze / Total.
5. **Validation contre les chiffres officiels du CIO** (assertions bloquantes
   sur 2016, 2020, 2024 — USA, Chine, France...).
6. **Enrichissement** : population (log), continent, PIB/habitant (log,
   correspondance NOC -> ISO3, merge_asof sur la derniere valeur connue).

## 3. Exploration statistique (notebook 02b)

- **Descriptif** : la distribution des medailles est tres asymetrique
  (skewness eleve) ; ~20 % des pays concentrent 80 % des medailles.
- **Multivarie** : correlations de Spearman — le total de l'edition precedente
  est de loin le meilleur predicteur ; population et PIB sont des signaux
  secondaires. Cela justifie les features lag/rolling.
- **Inferentiel** : test de Wilcoxon apparie sur l'effet pays hote
  (medailles l'annee hote vs moyenne des editions adjacentes, 14 paires
  depuis 1968) : **p = 0.0007, boost median +10.5 medailles**. La feature
  `is_host` est statistiquement justifiee.

## 4. Modelisation (notebook 03)

- **Cible** : medailles par (pays, sport, couleur) sur une grille complete
  incluant les zeros (90 % des couples), top 30 sports.
- **Features** : lag_1, lag_2, rolling_3 par couleur, is_host, log_population,
  log_gdp, continent et sport (one-hot).
- **Split temporel** : train 1968-2016, test Paris 2024 (jamais vu). Pas de
  random split : il ferait fuiter le futur dans le passe (data leakage).
- **Modele retenu** : 3 regressions Ridge independantes (une par couleur),
  alpha optimise par GridSearchCV (validation croisee 5 plis).

### Comparaison de modeles (test Paris 2024)

| Modele | RMSE granulaire | RMSE pays | R2 pays |
|---|---|---|---|
| Ridge | 0.28 | 4.4 | 0.88 |
| RandomForest | 0.28 | 4.3 | 0.89 |
| XGBoost | 0.28 | 3.6 | 0.92 |

(Valeurs arrondies ; les chiffres exacts de la derniere execution sont dans
`model_metrics.json` et affiches dynamiquement sur la page methodologie du site.)

XGBoost gagne sur 2024, mais l'avantage est mesure sur **une seule edition de
test** : impossible d'exclure un sur-apprentissage des specificites de 2024.
Ridge est conserve pour son interpretabilite (coefficients lisibles) et sa
stabilite ; XGBoost est note comme perspective.

### Lecture des metriques

Le R2 granulaire (~0.5) est structurellement limite par la masse de zeros.
Les metriques significatives sont la **MAE granulaire (0.08 medaille)** et le
**R2 au niveau pays (0.88)** : le classement final est predit avec une bonne
fiabilite.

## 5. Incertitude (notebook 03, section 7bis)

Bootstrap des residus relatifs observes sur le test 2024, restreint aux pays
a >= 5 medailles predites (les micro-pays fausseraient les quantiles).
B = 2000 reechantillonnages -> quantiles P10 / P90 appliques a chaque
prediction 2028. Les fourchettes sont larges (USA : 31-150 pour 110 predites) :
c'est la variance reelle du probleme, assumee plutot que masquee.

## 6. Restitution (app/)

`build.py` exporte 6 JSON ; le site statique (3 pages, Plotly.js) raconte
l'histoire : contexte -> validation sur Paris 2024 -> classement predit avec
fourchettes -> cote par discipline -> methodologie et limites.

## Limites assumees

- Nouveaux sports 2028 sans historique : non predits.
- Effet hote binaire : ne capte pas l'amplitude propre a chaque pays.
- Fourchettes issues d'une seule edition de test : hypothese de stationnarite
  des erreurs entre 2024 et 2028.
- Les reattributions de medailles post-Jeux (dopage) ne sont pas refletees
  dans les editions anciennes du dataset.
