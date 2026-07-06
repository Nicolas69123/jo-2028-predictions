"""Build script for the YPerf static web app (refonte simplifiee).

Reads the unique processed CSV + ML model, exports JSONs for the frontend.
"""
from pathlib import Path
import json
import pandas as pd
import joblib

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
OUT_DIR = Path(__file__).resolve().parent / "dist" / "data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Reading from : {PROCESSED_DIR}")
print(f"Writing to   : {OUT_DIR}")


def save(name, data):
    out = OUT_DIR / f"{name}.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, default=str)
    print(f"  -> {name}.json ({out.stat().st_size / 1024:.1f} Ko)")


# === Chargement ===
df = pd.read_csv(PROCESSED_DIR / "medals_per_country_sport.csv")
projection_country = pd.read_csv(PROCESSED_DIR / "projection_2028_country.csv")
projection_sport = pd.read_csv(PROCESSED_DIR / "projection_2028_per_sport.csv")
model_bundle = joblib.load(MODELS_DIR / "medal_predictor.pkl")

# === KPIs pour l'accueil ===
save("kpis", {
    "n_editions": int(df["Year"].nunique()),
    "n_countries": int(df["NOC"].nunique()),
    "n_sports": int(df["Sport"].nunique()),
    "n_medals_total": int(df["Total"].sum()),
    "n_models": 3,
    "country_r2": float(model_bundle["country_level_r2"]),
    "country_rmse": float(model_bundle["country_level_rmse"]),
})

# === Historique top 5 pays (Or par edition) ===
top5_nocs = (df[df["Year"] == 2024].groupby("NOC")["Total"].sum()
             .sort_values(ascending=False).head(5).index.tolist())
historical = []
for noc in top5_nocs:
    country_name = df[df["NOC"] == noc]["Country"].iloc[0]
    yearly = df[df["NOC"] == noc].groupby("Year").agg(
        Gold=("Gold", "sum"), Silver=("Silver", "sum"),
        Bronze=("Bronze", "sum"), Total=("Total", "sum"),
    ).reset_index()
    historical.append({
        "NOC": noc,
        "Country": str(country_name),
        "data": yearly.to_dict(orient="records"),
    })
save("historical_top5", historical)

# === Projection LA 2028 (classement complet) ===
save("projection_2028", projection_country.to_dict(orient="records"))

# === Projection par sport AVEC HISTORIQUE multi-annees ===
# Pour CHAQUE pays medaille, on exporte les medailles par sport sur 1952->2024
# (donnees reelles) + 2028 (seule annee predite). Permet comparaison pays et
# graphe d'evolution dans l'interface.

# Annees reelles a inclure : toutes les editions d'ete de 1952 a 2024
YEARS_REAL = [y for y in sorted(df["Year"].unique()) if 1952 <= y <= 2024]
# 2028 = seule annee de prediction
all_nocs = projection_country["NOC"].tolist()

per_sport_data = []
for noc in all_nocs:
    country_name = projection_country[projection_country["NOC"] == noc]["Country"].iloc[0]

    # Sports a afficher pour ce pays : top 15 selon la prediction 2028
    proj_country = projection_sport[projection_sport["NOC"] == noc].copy()
    top_sports_country = (proj_country.sort_values("pred_Total", ascending=False)
                          .head(15)["Sport"].tolist())

    # Donnees REELLES par annee x sport (valeurs entieres)
    by_year = {}
    for year in YEARS_REAL:
        year_data = df[(df["Year"] == year) & (df["NOC"] == noc)
                       & (df["Sport"].isin(top_sports_country))].copy()
        sport_records = []
        for sport in top_sports_country:
            row = year_data[year_data["Sport"] == sport]
            if len(row) > 0:
                r = row.iloc[0]
                sport_records.append({
                    "Sport": sport,
                    "Gold": int(r["Gold"]),
                    "Silver": int(r["Silver"]),
                    "Bronze": int(r["Bronze"]),
                    "Total": int(r["Total"]),
                })
            else:
                sport_records.append({
                    "Sport": sport, "Gold": 0, "Silver": 0, "Bronze": 0, "Total": 0,
                })
        by_year[str(year)] = sport_records

    # PREDICTION 2028 (valeurs decimales arrondies a 1 chiffre)
    pred_records = []
    for sport in top_sports_country:
        row = proj_country[proj_country["Sport"] == sport]
        if len(row) > 0:
            r = row.iloc[0]
            pred_records.append({
                "Sport": sport,
                "Gold": round(float(r["pred_Gold"]), 1),
                "Silver": round(float(r["pred_Silver"]), 1),
                "Bronze": round(float(r["pred_Bronze"]), 1),
                "Total": round(float(r["pred_Total"]), 1),
            })
        else:
            pred_records.append({
                "Sport": sport, "Gold": 0, "Silver": 0, "Bronze": 0, "Total": 0,
            })
    by_year["2028"] = pred_records  # 2028 = SEULE annee predite

    per_sport_data.append({
        "NOC": noc,
        "Country": str(country_name),
        "sports_list": top_sports_country,
        "available_years": YEARS_REAL + [2028],
        "by_year": by_year,
    })

save("per_sport_predictions", per_sport_data)

# === Metriques du modele ===
save("model_metrics", {
    "country_level": {
        "r2": float(model_bundle["country_level_r2"]),
        "rmse": float(model_bundle["country_level_rmse"]),
    },
    "by_color": {
        color: {
            "rmse": float(m["rmse"]),
            "mae": float(m["mae"]),
            "r2": float(m["r2"]),
        }
        for color, m in model_bundle["metrics_test_2024"].items()
    },
    "n_top_sports": len(model_bundle["top_sports"]),
    "trained_years": "1968-2016",
    "test_year": 2024,
    # Comparaison Ridge / RandomForest / XGBoost (test 2024) et quantiles bootstrap
    "model_comparison": model_bundle.get("model_comparison"),
    "ci_quantiles": model_bundle.get("ci_quantiles"),
})

# === Predictions reel vs predit 2024 (scatter de validation du site) ===
# Sorties reelles du split test du notebook 03 (le modele n'a jamais vu 2024)
validation = pd.read_csv(PROCESSED_DIR / "validation_2024_country.csv")
test_results = [
    {
        "NOC": row["NOC"],
        "Country": str(row["Country"]),
        "real_2024": int(row["real_Total"]),
        "pred_2024": float(row["pred_Total"]),
    }
    for _, row in validation.sort_values("real_Total", ascending=False).iterrows()
]
save("validation_2024", test_results)

print("\nBuild complete.")
