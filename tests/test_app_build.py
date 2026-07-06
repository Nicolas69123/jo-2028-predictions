"""Tests des exports JSON consommes par le site statique."""
import json

from .conftest import DIST_DATA_DIR


def _load(name):
    with open(DIST_DATA_DIR / f"{name}.json", encoding="utf-8") as f:
        return json.load(f)


class TestExportsJson:
    def test_les_six_fichiers_existent(self):
        for name in ["kpis", "historical_top5", "projection_2028",
                     "per_sport_predictions", "model_metrics", "validation_2024"]:
            assert (DIST_DATA_DIR / f"{name}.json").exists(), f"{name}.json manquant"

    def test_kpis_complets(self):
        kpis = _load("kpis")
        for cle in ["n_editions", "n_countries", "n_sports", "country_r2", "country_rmse"]:
            assert cle in kpis

    def test_projection_alignee_avec_le_csv(self, projection):
        export = _load("projection_2028")
        assert len(export) == len(projection)
        assert export[0]["Rank"] == 1

    def test_projection_contient_les_fourchettes(self):
        export = _load("projection_2028")
        assert "Total_low" in export[0] and "Total_high" in export[0]

    def test_metrics_contiennent_la_comparaison(self):
        metrics = _load("model_metrics")
        assert metrics["model_comparison"] is not None
        assert metrics["ci_quantiles"] is not None

    def test_historique_top5_structure(self):
        historique = _load("historical_top5")
        assert len(historique) == 5
        assert {"NOC", "Country", "data"}.issubset(historique[0].keys())
