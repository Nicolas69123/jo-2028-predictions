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
        # Table officielle CIO complete de Paris 2024 (92 NOC medailles).
        # Wikipedia utilise BAH pour Bahrein (nous : BRN) et ROT pour les
        # refugies (nous : EOR) : la table ci-dessous emploie nos codes.
        officiel = (
            "USA 40 44 42|CHN 40 27 24|JPN 20 12 13|AUS 18 19 16|FRA 16 26 22|"
            "NED 15 7 12|GBR 14 22 29|KOR 13 9 10|ITA 12 13 15|GER 12 13 8|"
            "NZL 10 7 3|CAN 9 7 11|UZB 8 2 3|HUN 6 7 6|ESP 5 4 9|SWE 4 4 3|"
            "KEN 4 2 5|NOR 4 1 3|IRL 4 0 3|BRA 3 7 10|IRI 3 6 3|UKR 3 5 4|"
            "ROU 3 4 2|GEO 3 3 1|BEL 3 1 6|BUL 3 1 3|SRB 3 1 1|CZE 3 0 2|"
            "DEN 2 2 5|AZE 2 2 3|CRO 2 2 3|CUB 2 1 6|BRN 2 1 1|SLO 2 1 0|"
            "TPE 2 0 5|AUT 2 0 3|HKG 2 0 2|PHI 2 0 2|ALG 2 0 1|INA 2 0 1|"
            "ISR 1 5 1|POL 1 4 5|KAZ 1 3 3|JAM 1 3 2|RSA 1 3 2|THA 1 3 2|"
            "AIN 1 3 1|ETH 1 3 0|SUI 1 2 5|ECU 1 2 2|POR 1 2 1|GRE 1 1 6|"
            "ARG 1 1 1|EGY 1 1 1|TUN 1 1 1|BOT 1 1 0|CHI 1 1 0|LCA 1 1 0|"
            "UGA 1 1 0|DOM 1 0 2|GUA 1 0 1|MAR 1 0 1|DMA 1 0 0|PAK 1 0 0|"
            "TUR 0 3 5|MEX 0 3 2|ARM 0 3 1|COL 0 3 1|KGZ 0 2 4|PRK 0 2 4|"
            "LTU 0 2 2|IND 0 1 5|MDA 0 1 3|KOS 0 1 1|CYP 0 1 0|FIJ 0 1 0|"
            "JOR 0 1 0|MGL 0 1 0|PAN 0 1 0|TJK 0 0 3|ALB 0 0 2|GRN 0 0 2|"
            "MAS 0 0 2|PUR 0 0 2|CPV 0 0 1|CIV 0 0 1|PER 0 0 1|QAT 0 0 1|"
            "EOR 0 0 1|SGP 0 0 1|SVK 0 0 1|ZAM 0 0 1"
        )
        p24 = processed[processed["Year"] == 2024].groupby("NOC")[
            ["Gold", "Silver", "Bronze"]].sum()
        ecarts = []
        for ligne in officiel.split("|"):
            noc, g, s, b = ligne.split()
            if noc not in p24.index:
                ecarts.append(f"{noc} absent")
                continue
            row = p24.loc[noc]
            if (row["Gold"], row["Silver"], row["Bronze"]) != (int(g), int(s), int(b)):
                ecarts.append(f"{noc}: {row['Gold']}/{row['Silver']}/{row['Bronze']}"
                              f" != {g}/{s}/{b}")
        assert ecarts == [], f"Ecarts vs table officielle CIO 2024 : {ecarts}"
        assert len(p24) == 92
