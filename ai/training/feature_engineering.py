"""
feature_engineering.py — Zumedical Prenatal AI
================================================
Ingeniería de características mejorada para predicción de riesgo prenatal.

Mejoras v2:
  - Se reducen features derivadas redundantes con BMI para evitar dominancia
  - Se agregan features de interacción clínica más relevantes
  - Se normaliza la importancia relativa entre features
  - Se agregan rangos clínicos más precisos para glucosa, PA y edad

Variables finales del modelo (17 features):
  age, systolic_bp, diastolic_bp, glucose, body_temp, heart_rate, bmi,
  prev_complications, diabetes_preexisting, diabetes_gestacional,
  pulse_pressure, hipertension_flag, diabetes_flag, edad_avanzada,
  glucosa_cat, map_arterial, riesgo_combinado
"""

import pandas as pd
import numpy as np

# ── Columnas que entran al modelo ─────────────────────────────────────────────
MODEL_FEATURES = [
    "age",
    "systolic_bp",
    "diastolic_bp",
    "glucose",
    "body_temp",
    "heart_rate",
    "bmi",
    "prev_complications",
    "diabetes_preexisting",
    "diabetes_gestacional",
    "pulse_pressure",
    "hipertension_flag",
    "diabetes_flag",
    "edad_avanzada",
    "glucosa_cat",
    "map_arterial",
    "riesgo_combinado",
]

TARGET = "risk_level"

# Codificación ordinal de la variable objetivo
LABEL_ENCODE = {"low": 0, "mid": 1, "high": 2}
LABEL_DECODE = {0: "Bajo", 1: "Medio", 2: "Alto"}


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega columnas de ingeniería de características al DataFrame.
    Trabaja sobre una copia para no mutar el original.
    """
    df = df.copy()

    # ── Pulse pressure (presión diferencial) ──────────────────────────────
    # Marcador de rigidez arterial — clínicamente relevante en preeclampsia
    df["pulse_pressure"] = df["systolic_bp"] - df["diastolic_bp"]

    # ── Presión arterial media (MAP) ──────────────────────────────────────
    # MAP = diastólica + (1/3) * pulse_pressure — mejor predictor que PA sola
    df["map_arterial"] = df["diastolic_bp"] + (df["pulse_pressure"] / 3.0)

    # ── Flag hipertensión (umbral OMS para embarazadas) ───────────────────
    # ≥140/90 = hipertensión gestacional
    df["hipertension_flag"] = (
        (df["systolic_bp"] >= 140) | (df["diastolic_bp"] >= 90)
    ).astype(int)

    # ── Flag diabetes por glucosa en mmol/L ───────────────────────────────
    # >7.8 = hiperglucemia postprandial (criterio ADA/OMS)
    df["diabetes_flag"] = (df["glucose"] > 7.8).astype(int)

    # ── Edad avanzada ─────────────────────────────────────────────────────
    df["edad_avanzada"] = (df["age"] >= 35).astype(int)

    # ── Categoría de glucosa (mmol/L) ─────────────────────────────────────
    # 0=Normal(<5.6)  1=Límite(5.6-7.8)  2=Elevada(7.8-11)  3=Muy elevada(>11)
    df["glucosa_cat"] = pd.cut(
        df["glucose"],
        bins=[-np.inf, 5.6, 7.8, 11.0, np.inf],
        labels=[0, 1, 2, 3],
    ).astype(int)

    # ── Riesgo combinado: interacción PA + glucosa ────────────────────────
    # Feature de interacción que captura la co-ocurrencia de HTA + hiperglucemia
    # Este patrón es fuertemente predictivo de preeclampsia + diabetes gestacional
    df["riesgo_combinado"] = df["hipertension_flag"] * df["diabetes_flag"]

    # ── BMI: rellenar con mediana si hay NaN ──────────────────────────────
    if df["bmi"].isna().any():
        df["bmi"] = df["bmi"].fillna(df["bmi"].median())

    return df


def prepare_xy(df: pd.DataFrame):
    """
    Retorna (X, y) listos para scikit-learn.
    X: DataFrame con MODEL_FEATURES
    y: Series codificada numéricamente (0=low, 1=mid, 2=high)
    """
    df = add_features(df)
    df["risk_encoded"] = df[TARGET].map(LABEL_ENCODE)
    df = df.dropna(subset=["risk_encoded"])

    X = df[MODEL_FEATURES].copy()
    y = df["risk_encoded"].astype(int)
    return X, y


def prepare_single_record(data: dict) -> pd.DataFrame:
    """
    Convierte un dict de datos clínicos en un DataFrame de 1 fila
    con todas las features necesarias para la predicción.

    Parámetros esperados (mínimo):
        age, systolic_bp, diastolic_bp, glucose (en mmol/L),
        body_temp, heart_rate, bmi,
        prev_complications, diabetes_preexisting, diabetes_gestacional

    Los que falten se rellenan con valores medianos clínicos seguros.
    """
    defaults = {
        "age":                  25,
        "systolic_bp":          110,
        "diastolic_bp":         70,
        "glucose":              6.5,    # mmol/L — normal en embarazo
        "body_temp":            98.0,
        "heart_rate":           75,
        "bmi":                  23.0,   # Normal
        "prev_complications":   0,
        "diabetes_preexisting": 0,
        "diabetes_gestacional": 0,
    }
    defaults.update(data)

    row = pd.DataFrame([defaults])
    row = add_features(row)
    return row[MODEL_FEATURES]


if __name__ == "__main__":
    from preprocess import get_clean_dataframe
    df = get_clean_dataframe()
    X, y = prepare_xy(df)
    print("X shape:", X.shape)
    print("y dist:\n", y.value_counts())
    print("\nFeatures:\n", X.dtypes)
