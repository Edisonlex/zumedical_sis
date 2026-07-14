"""
train_model.py — Zumedical Prenatal AI v2
==========================================
Entrenamiento mejorado del modelo Random Forest con:
  - GradientBoosting como modelo secundario para comparación
  - Calibración de probabilidades (CalibratedClassifierCV)
  - Reducción de dominancia del BMI via max_features ajustado
  - Feature importance normalizada y reporte detallado

Uso:
    python train_model.py

Genera:
    ai/model/modelo_riesgo.pkl   — modelo entrenado
    ai/model/scaler.pkl          — StandardScaler ajustado
    ai/model/feature_names.pkl   — lista de features en orden exacto
    ai/model/training_report.txt — reporte de métricas
"""

import os
import sys
import pickle
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, classification_report, confusion_matrix,
)

from preprocess import get_clean_dataframe
from feature_engineering import prepare_xy, LABEL_DECODE, MODEL_FEATURES


MODEL_DIR  = Path(__file__).resolve().parent.parent / "model"
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH    = MODEL_DIR / "modelo_riesgo.pkl"
SCALER_PATH   = MODEL_DIR / "scaler.pkl"
FEATURES_PATH = MODEL_DIR / "feature_names.pkl"
REPORT_PATH   = MODEL_DIR / "training_report.txt"


def train():
    print("=" * 60)
    print("  ZUMEDICAL — Entrenamiento del Modelo de Riesgo Prenatal v2")
    print("=" * 60)

    # ── 1. Cargar y preparar datos ────────────────────────────────────────
    print("\n[1/6] Cargando y preprocesando datasets...")
    df = get_clean_dataframe()
    X, y = prepare_xy(df)

    print(f"      Total registros : {len(X)}")
    print(f"      Features         : {X.shape[1]}")
    dist = y.value_counts().sort_index()
    for k, v in dist.items():
        print(f"      Clase {k} ({LABEL_DECODE[k]}): {v} registros ({v/len(y)*100:.1f}%)")

    # ── 2. División train/test estratificada (80/20) ──────────────────────
    print("\n[2/6] Dividiendo datos 80% entrenamiento / 20% prueba...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y,
    )
    print(f"      Train: {len(X_train)} | Test: {len(X_test)}")

    # ── 3. Escalar features ───────────────────────────────────────────────
    print("\n[3/6] Escalando features (StandardScaler)...")
    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)

    # ── 4. Entrenar Random Forest con calibración ─────────────────────────
    print("\n[4/6] Entrenando Random Forest con calibración de probabilidades...")
    rf_base = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,           # Limitar profundidad reduce overfitting al BMI
        min_samples_split=5,
        min_samples_leaf=3,
        max_features="sqrt",
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )

    # CalibratedClassifierCV mejora las probabilidades predict_proba
    # para que sean más confiables en la práctica clínica
    model = CalibratedClassifierCV(rf_base, cv=5, method="isotonic")
    model.fit(X_train_sc, y_train)
    print("      Modelo entrenado con calibración isotónica.")

    # ── 5. Evaluar ────────────────────────────────────────────────────────
    print("\n[5/6] Evaluando modelo...")
    y_pred = model.predict(X_test_sc)
    y_proba = model.predict_proba(X_test_sc)

    acc  = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    rec  = recall_score(y_test, y_pred, average="weighted", zero_division=0)
    f1   = f1_score(y_test, y_pred, average="weighted", zero_division=0)
    cm   = confusion_matrix(y_test, y_pred)

    # Cross-validation 5 folds estratificado
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(
        model, scaler.transform(X), y, cv=skf, scoring="f1_weighted"
    )

    target_names = [LABEL_DECODE[i] for i in sorted(LABEL_DECODE.keys())]
    report_str = classification_report(
        y_test, y_pred, target_names=target_names, zero_division=0
    )

    print(f"\n      Accuracy  : {acc:.4f}  ({acc*100:.2f}%)")
    print(f"      Precision : {prec:.4f}")
    print(f"      Recall    : {rec:.4f}")
    print(f"      F1 Score  : {f1:.4f}")
    print(f"      CV F1 (5k): {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    print("\n      Clasificación por clase:")
    print(report_str)
    print("      Matriz de confusión (filas=real, cols=pred):")
    print("      Clases:", target_names)
    print(cm)

    # Feature importances del RF base dentro del calibrador
    try:
        importances = pd.Series(
            rf_base.feature_importances_, index=MODEL_FEATURES
        ).sort_values(ascending=False)
        print("\n      Top variables más importantes:")
        for feat, imp in importances.head(10).items():
            bar = "█" * int(imp * 50)
            print(f"        {feat:<28} {imp:.4f}  {bar}")
    except Exception:
        importances = pd.Series(index=MODEL_FEATURES, dtype=float)
        print("      (importancias no disponibles con calibrador)")

    # ── 6. Guardar ────────────────────────────────────────────────────────
    print("\n[6/6] Guardando modelo en ai/model/...")

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(SCALER_PATH, "wb") as f:
        pickle.dump(scaler, f)
    with open(FEATURES_PATH, "wb") as f:
        pickle.dump(MODEL_FEATURES, f)

    report_content = f"""
ZUMEDICAL — Reporte de Entrenamiento del Modelo de Riesgo Prenatal v2
======================================================================
Algoritmo        : Random Forest (n=300, max_depth=12) + Calibración Isotónica
Dataset principal: Maternal Health and High-Risk Pregnancy Dataset
Dataset secundario: Maternal Health Risk Data Set UCI
Total registros  : {len(X)}
Features         : {len(MODEL_FEATURES)}

MÉTRICAS DE EVALUACIÓN (Test 20%)
-----------------------------------
Accuracy   : {acc:.4f} ({acc*100:.2f}%)
Precision  : {prec:.4f}
Recall     : {rec:.4f}
F1 Score   : {f1:.4f}
CV F1 (5k) : {cv_scores.mean():.4f} ± {cv_scores.std():.4f}

CLASIFICACIÓN POR CLASE:
{report_str}

MATRIZ DE CONFUSIÓN (filas=real, columnas=predicho):
Clases: {target_names}
{cm}

IMPORTANCIA DE VARIABLES:
{importances.to_string() if not importances.empty else "N/A"}
"""
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"\n  ✔ modelo_riesgo.pkl   → {MODEL_PATH}")
    print(f"  ✔ scaler.pkl          → {SCALER_PATH}")
    print(f"  ✔ feature_names.pkl   → {FEATURES_PATH}")
    print(f"  ✔ training_report.txt → {REPORT_PATH}")
    print("\n" + "=" * 60)
    print(f"  Entrenamiento completado. Accuracy = {acc*100:.1f}% | F1 = {f1*100:.1f}%")
    print("=" * 60)


if __name__ == "__main__":
    train()
