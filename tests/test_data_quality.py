"""Qualite des donnees sources et du dataset prepare."""
import pandas as pd

from .conftest import DATA_DIR


class TestSourcesBrutes:
    def test_colonnes_attendues(self, raw_results):
        attendues = {"discipline", "event", "medal_type", "country_code",
                     "country", "event_year"}
        assert attendues.issubset(raw_results.columns)

    def test_types_de_medailles_valides(self, raw_results):
        medailles = raw_results["medal_type"].dropna().unique()
        assert set(medailles).issubset({"Gold", "Silver", "Bronze"})

    def test_periode_couverte(self, raw_results):
        assert raw_results["event_year"].min() <= 1900
        assert raw_results["event_year"].max() >= 2024

    def test_programme_2028_sans_doublons(self):
        sports = pd.read_csv(DATA_DIR / "JO2028_sports.csv", sep=";")
        assert not sports.duplicated().any()

    def test_pib_couvre_les_grandes_nations(self):
        gdp = pd.read_csv(DATA_DIR / "PIB_par_habitant.csv", sep=";")
        for iso3 in ["USA", "CHN", "FRA", "DEU", "JPN"]:
            assert iso3 in set(gdp["iso3"]), f"PIB manquant pour {iso3}"


class TestDatasetPrepare:
    def test_coherence_total(self, processed):
        somme = processed["Gold"] + processed["Silver"] + processed["Bronze"]
        assert (somme == processed["Total"]).all()

    def test_pas_de_medailles_negatives(self, processed):
        assert processed[["Gold", "Silver", "Bronze"]].min().min() >= 0

    def test_pas_de_doublons_noc_annee_sport(self, processed):
        assert not processed.duplicated(subset=["Year", "NOC", "Sport"]).any()

    def test_editions_ete_uniquement(self, processed):
        # Les JO d'hiver (1994, 1998, 2002...) ne doivent pas apparaitre
        annees_hiver = {1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022}
        assert annees_hiver.isdisjoint(set(processed["Year"].unique()))

    def test_validation_cio_paris_2024(self, processed):
        # Chiffres officiels CIO : USA 40 or / 126 total, France 16 or / 64 total
        p24 = processed[processed["Year"] == 2024]
        usa = p24[p24["NOC"] == "USA"][["Gold", "Total"]].sum()
        fra = p24[p24["NOC"] == "FRA"][["Gold", "Total"]].sum()
        assert usa["Gold"] == 40
        assert fra["Gold"] == 16
