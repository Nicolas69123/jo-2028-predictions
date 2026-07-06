# Sources de donnees

## 1. JO_resultats.csv — Resultats olympiques 1896-2024

- **Contenu** : ~24 000 lignes de medailles (discipline, epreuve, genre, type
  athlete/equipe, medaille, nom, pays, ville, annee).
- **Origine** : dataset public olympics_1896_2024
  (DjangoMustang/Olympics-1896-2024-Tableau), choisi apres audit comparatif.
- **Validation** : match exact avec le classement officiel du CIO sur les trois
  dernieres editions (2016, 2020, 2024). Les editions plus anciennes presentent
  parfois +/- 1 medaille : reattributions post-Jeux (disqualifications pour dopage)
  que les datasets publics ne refletent pas en temps reel.
- **Piege connu** : contient les JO d'hiver ; le pipeline filtre via la table de
  reference des editions d'ete (jointure, pas de liste en dur).

## 2. JO2028_sports.csv — Programme officiel LA 2028

- **Contenu** : 347 epreuves (discipline, epreuve, genre) du programme officiel.
- **Usage** : identifier les disciplines sans historique olympique (flag football,
  squash, cricket...) que le modele ne peut pas predire, et cadrer le perimetre
  de la projection.
- **Nettoyage** : doublons de saisie retires (verifie par un test pytest).

## 3. JO_date_ete.csv — Editions d'ete

- **Contenu** : 32 lignes (annee, ville, pays) de 1896 a 2028.
- **Usage** : table de reference pour filtrer les JO d'ete et construire la
  variable pays hote (`is_host`).

## 4. PIB_par_habitant.csv — Banque Mondiale

- **Contenu** : ~14 000 lignes (iso3, annee, PIB/habitant en USD courants),
  1960-2024, 257 pays et agregats.
- **Origine** : API open data de la Banque Mondiale, indicateur `NY.GDP.PCAP.CD`
  (https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.CD).
- **Reproductibilite** : le fichier est versionne ; le notebook 01 ne retelecharge
  que s'il est absent.
- **Piege connu** : les codes CIO (NOC) different des codes ISO3 pour 48 pays
  (GER/DEU, NED/NLD, SUI/CHE...) — table de correspondance dans le notebook 02.
  Les entites historiques (URS, GDR, TCH) et neutres (EUN, AIN) n'ont pas de PIB :
  imputation a la mediane lors de la modelisation.

## Enrichissements derives

- **Population** : dictionnaire par NOC integre au notebook 02 (source Banque
  Mondiale, valeurs recentes), transformee en log.
- **Continent** : mapping NOC -> continent integre au notebook 02.
