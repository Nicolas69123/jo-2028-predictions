"""Tests du bundle de modeles et de la projection 2028."""
import numpy as np


class TestBundle:
    def test_trois_modeles_presents(self, bundle):
        assert set(bundle["models"].keys()) == {"Gold", "Silver", "Bronze"}

    def test_features_coherentes_entre_couleurs(self, bundle):
        # Chaque couleur a ses propres lags mais le meme nombre de features
        tailles = {c: len(cols) for c, cols in bundle["feature_columns"].items()}
        assert len(set(tailles.values())) == 1

    def test_performance_minimale_niveau_pays(self, bundle):
        # Garde-fou anti-regression : le R2 pays valide sur Paris 2024
        assert bundle["country_level_r2"] > 0.80
        assert bundle["country_level_rmse"] < 6.0

    def test_comparaison_modeles_presente(self, bundle):
        assert "model_comparison" in bundle
        assert "Ridge" in bundle["model_comparison"]["R2_pays"]

    def test_quantiles_bootstrap_coherents(self, bundle):
        q = bundle["ci_quantiles"]
        assert q["q10"] < 0 < q["q90"]


class TestProjection2028:
    def test_usa_dans_le_top_3(self, projection):
        # Effet hote + domination historique : USA attendu dans le trio de tete
        assert "USA" in projection.head(3)["NOC"].tolist()

    def test_rangs_uniques_et_continus(self, projection):
        assert projection["Rank"].tolist() == list(range(1, len(projection) + 1))

    def test_pas_de_prediction_negative(self, projection):
        cols = ["Gold_2028", "Silver_2028", "Bronze_2028", "Total_2028"]
        assert (projection[cols] >= 0).all().all()

    def test_fourchettes_encadrent_la_prediction(self, projection):
        assert (projection["Total_low"] <= projection["Total_2028"]).all()
        assert (projection["Total_high"] >= projection["Total_2028"]).all()

    def test_ordre_de_grandeur_realiste(self, projection):
        # Aucun pays n'a jamais depasse ~230 medailles sur une edition moderne
        assert projection["Total_2028"].max() < 200
