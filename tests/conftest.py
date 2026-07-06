"""Fixtures partagees : chargement unique des artefacts du pipeline."""
from pathlib import Path

import joblib
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
DIST_DATA_DIR = PROJECT_ROOT / "app" / "dist" / "data"


@pytest.fixture(scope="session")
def raw_results():
    return pd.read_csv(DATA_DIR / "JO_resultats.csv", sep=";", low_memory=False)


def _require(path):
    """Skip proprement si l'artefact du pipeline n'a pas ete genere localement
    (data/processed et models/ sont gitignores : en CI seuls les tests sur
    les sources brutes s'executent)."""
    if not path.exists():
        pytest.skip(f"artefact absent : {path.name} (executer les notebooks d'abord)")
    return path


@pytest.fixture(scope="session")
def processed():
    return pd.read_csv(_require(PROCESSED_DIR / "medals_per_country_sport.csv"))


@pytest.fixture(scope="session")
def projection():
    return pd.read_csv(_require(PROCESSED_DIR / "projection_2028_country.csv"))


@pytest.fixture(scope="session")
def bundle():
    return joblib.load(_require(MODELS_DIR / "medal_predictor.pkl"))
