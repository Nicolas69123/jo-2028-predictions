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


class TestCoherenceAffichage:
    """Les totaux affiches par le site doivent matcher la base, pays par pays."""

    def test_totals_by_year_egaux_a_la_base(self, processed):
        data = _load("per_sport_predictions")
        ecarts = []
        for c in data:
            for year, t in c["totals_by_year"].items():
                if year == "2028":
                    continue  # prediction, pas dans la base
                base = processed[(processed["NOC"] == c["NOC"])
                                 & (processed["Year"] == int(year))]
                attendu = (int(base["Gold"].sum()), int(base["Silver"].sum()),
                           int(base["Bronze"].sum()), int(base["Total"].sum()))
                montre = (t["Gold"], t["Silver"], t["Bronze"], t["Total"])
                if montre != attendu:
                    ecarts.append(f"{c['NOC']} {year}: {montre} != {attendu}")
        assert ecarts == [], ecarts[:10]

    def test_totals_2028_egaux_a_la_projection(self, projection):
        data = _load("per_sport_predictions")
        proj = projection.set_index("NOC")
        for c in data:
            if c["NOC"] in proj.index:
                assert abs(c["totals_by_year"]["2028"]["Total"]
                           - proj.loc[c["NOC"], "Total_2028"]) < 0.11, c["NOC"]

    def test_historique_top5_egal_a_la_base(self, processed):
        for pays in _load("historical_top5"):
            for rec in pays["data"]:
                base = processed[(processed["NOC"] == pays["NOC"])
                                 & (processed["Year"] == rec["Year"])]
                assert rec["Total"] == int(base["Total"].sum()), \
                    f"{pays['NOC']} {rec['Year']}"

    def test_validation_reelle_egale_a_la_base_perimetre_modele(self, processed, bundle):
        # Le scatter de validation porte sur les 30 sports modelises
        top_sports = set(bundle["top_sports"])
        p24 = processed[(processed["Year"] == 2024)
                        & (processed["Sport"].isin(top_sports))]
        for d in _load("validation_2024")[:30]:
            attendu = int(p24[p24["NOC"] == d["NOC"]]["Total"].sum())
            assert d["real_2024"] == attendu, f"{d['NOC']}: {d['real_2024']} != {attendu}"
