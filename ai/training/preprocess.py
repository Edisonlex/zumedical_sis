"""
preprocess.py — Zumedical Prenatal AI
======================================
Fase 2 y 3: Análisis, normalización de columnas y limpieza de datos.

Dataset 1 (principal, 80%):  Maternal Health and High-Risk Pregnancy Dataset
Dataset 2 (complementario):  Maternal Health Risk Data Set (UCI)

Estrategia de combinación:
  - Se alinean columnas comunes entre ambos datasets.
  - Dataset 1 tiene BMI, complicaciones previas, diabetes; Dataset 2 agrega
    el nivel "mid risk" que enriquece la clasificación multiclase.
  - La unión final tiene 3 clases: low / mid / high.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ── Rutas ────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent.parent
DATASET_1  = BASE_DIR / "datasets" / "Maternal Health and High-Risk Pregnancy Dataset.csv"
DATASET_2  = BASE_DIR / "datasets" / "Maternal Health Risk Data Set.csv"


# ── Mapas de normalización de etiquetas ──────────────────────────────────────
LABEL_MAP_D1 = {
    "high": "high",
    "High": "high",
    "low":  "low",
    "Low":  "low",
    "mid":  "mid",
    "Mid":  "mid",
}

LABEL_MAP_D2 = {
    "high risk": "high",
    "mid risk":  "mid",
    "low risk":  "low",
}

# ── Rangos clínicos válidos para filtrar outliers ─────────────────────────────
VALID_RANGES = {
    "age":           (10, 60),
    "systolic_bp":   (60, 200),
    "diastolic_bp":  (40, 140),
    "glucose":       (3.0, 25.0),   # mmol/L (los datasets usan mmol/L en BS)
    "body_temp":     (95.0, 106.0), # Fahrenheit
    "heart_rate":    (40, 180),
    "bmi":           (10.0, 60.0),
}


def _load_dataset1() -> pd.DataFrame:
    """Carga y normaliza el Dataset 1 (principal)."""
    df = pd.read_csv(DATASET_1)

    # ── Renombrar columnas a nombres internos ──────────────────────────────
    df = df.rename(columns={
        "Age":                    "age",
        "Systolic BP":            "systolic_bp",
        "Diastolic":              "diastolic_bp",
        "BS":                     "glucose",
        "Body Temp":              "body_temp",
        "BMI":                    "bmi",
        "Previous Complications": "prev_complications",
        "Preexisting Diabetes":   "diabetes_preexisting",
        "Gestational Diabetes":   "diabetes_gestacional",
        "Mental Health":          "salud_mental",
        "Heart Rate":             "heart_rate",
        "Risk Level":             "risk_level",
    })

    # ── Normalizar etiquetas ───────────────────────────────────────────────
    df["risk_level"] = df["risk_level"].str.strip().map(LABEL_MAP_D1)

    # ── Fuente para debugging ──────────────────────────────────────────────
    df["_source"] = "d1"
    return df


def _load_dataset2() -> pd.DataFrame:
    """Carga y normaliza el Dataset 2 (complementario UCI)."""
    df = pd.read_csv(DATASET_2)

    # ── Renombrar columnas a nombres internos ──────────────────────────────
    df = df.rename(columns={
        "Age":        "age",
        "SystolicBP": "systolic_bp",
        "DiastolicBP":"diastolic_bp",
        "BS":         "glucose",
        "BodyTemp":   "body_temp",
        "HeartRate":  "heart_rate",
        "RiskLevel":  "risk_level",
    })

    # ── Dataset 2 no tiene estas columnas; las creamos con valor neutro ────
    for col in ["bmi", "prev_complications", "diabetes_preexisting",
                "diabetes_gestacional", "salud_mental"]:
        df[col] = np.nan

    # ── Normalizar etiquetas ───────────────────────────────────────────────
    df["risk_level"] = df["risk_level"].str.strip().map(LABEL_MAP_D2)

    df["_source"] = "d2"
    return df


def load_and_merge() -> pd.DataFrame:
    """
    Carga ambos datasets, los combina y devuelve un DataFrame unificado limpio.
    Retorna columnas: age, systolic_bp, diastolic_bp, glucose, body_temp,
                      heart_rate, bmi, prev_complications, diabetes_preexisting,
                      diabetes_gestacional, salud_mental, risk_level
    """
    d1 = _load_dataset1()
    d2 = _load_dataset2()

    # ── Unir ───────────────────────────────────────────────────────────────
    df = pd.concat([d1, d2], ignore_index=True)

    # ── Eliminar filas con risk_level nulo (etiquetas no reconocidas) ──────
    df = df.dropna(subset=["risk_level"])

    # ── Eliminar duplicados exactos ────────────────────────────────────────
    feature_cols = ["age", "systolic_bp", "diastolic_bp", "glucose",
                    "body_temp", "heart_rate", "risk_level"]
    df = df.drop_duplicates(subset=feature_cols)

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fase 3: Limpieza de datos.
    1. Elimina valores fuera de rango clínico.
    2. Imputa valores faltantes numéricos con la mediana por clase.
    3. Rellena columnas binarias faltantes con 0.
    """
    # ── 1. Filtrar outliers clínicos ───────────────────────────────────────
    range_map = {
        "age":          VALID_RANGES["age"],
        "systolic_bp":  VALID_RANGES["systolic_bp"],
        "diastolic_bp": VALID_RANGES["diastolic_bp"],
        "glucose":      VALID_RANGES["glucose"],
        "body_temp":    VALID_RANGES["body_temp"],
        "heart_rate":   VALID_RANGES["heart_rate"],
        "bmi":          VALID_RANGES["bmi"],
    }

    for col, (lo, hi) in range_map.items():
        if col in df.columns:
            mask = df[col].notna()
            df = df[~(mask & ((df[col] < lo) | (df[col] > hi)))]

    # ── 2. Imputar numéricos con mediana por clase ─────────────────────────
    numeric_cols = ["age", "systolic_bp", "diastolic_bp", "glucose",
                    "body_temp", "heart_rate", "bmi"]
    for col in numeric_cols:
        if df[col].isna().any():
            df[col] = df.groupby("risk_level")[col].transform(
                lambda s: s.fillna(s.median())
            )
            # Si aún quedan NaN (grupo vacío), usar mediana global
            df[col] = df[col].fillna(df[col].median())

    # ── 3. Columnas binarias: rellenar NaN con 0 ──────────────────────────
    binary_cols = ["prev_complications", "diabetes_preexisting",
                   "diabetes_gestacional", "salud_mental"]
    for col in binary_cols:
        df[col] = df[col].fillna(0).astype(int)

    df = df.reset_index(drop=True)
    return df


def get_clean_dataframe() -> pd.DataFrame:
    """Punto de entrada principal: devuelve el dataframe limpio y unificado."""
    df = load_and_merge()
    df = clean_data(df)
    return df


if __name__ == "__main__":
    df = get_clean_dataframe()
    print(f"Dataset final: {df.shape[0]} registros, {df.shape[1]} columnas")
    print("Distribución de riesgo:\n", df["risk_level"].value_counts())
    print("\nNulls restantes:\n", df.isnull().sum())
    print("\nMuestra:\n", df.head())
