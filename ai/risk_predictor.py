
"""
Clinical Rule-Based Risk Predictor for Gestational Risks (RF-18)
Implements evidence-based rules for prenatal risk assessment with:
- Numerical risk score (0-100)
- Transparent factor explanation
- Personalized recommendations
"""
from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class RiskAssessment:
    """Data class to hold comprehensive risk assessment results"""
    score: int  # 0-100
    level: str  # "Muy Bajo", "Bajo", "Medio", "Alto"
    contributing_factors: List[str]  # Exact reasons
    recommendations: List[str]
    details: Dict[str, any]


class PrenatalRiskPredictor:
    """
    Clinical rule-based expert system for gestational risks
    """

    # Score thresholds for risk levels
    LEVELS = {
        "Muy Bajo": (0, 20),
        "Bajo": (21, 40),
        "Medio": (41, 65),
        "Alto": (66, 100),
    }

    # Weights for each risk factor
    RISK_FACTORS = {
        "preeclampsia_critical": 50,  # PA ≥ 160/110
        "preeclampsia_moderate": 25,  # PA ≥ 140/90
        "diabetes_critical": 45,  # Glucosa > 180
        "diabetes_moderate": 20,  # Glucosa > 140
        "diabetes_risk": 10,  # Glucosa > 110
        "age_very_high": 30,  # ≥40
        "age_high": 15,  # ≥35
        "obesity": 20,  # IMC ≥30
        "overweight": 8,  # IMC ≥25
        "previous_risk": 20,
        "multiple_pregnancies": 5,  # ≥3
        "trimester_first": 10,
        "trimester_third_advanced": 8,
    }

    def __init__(self):
        pass

    def _parse_blood_pressure(self, bp_str: str) -> Tuple[int, int]:
        """Parse blood pressure string like '120/80' into systolic/diastolic integers"""
        try:
            parts = bp_str.split('/')
            systolic = int(parts[0].strip())
            diastolic = int(parts[1].strip())
            return systolic, diastolic
        except (IndexError, ValueError):
            return 120, 80  # Default normal values

    def _calculate_bmi(self, weight: float, height: float) -> float:
        """Calculate Body Mass Index"""
        if height <= 0:
            return 22.0
        return round(weight / (height ** 2), 2)

    def assess_risk(
        self,
        age: int,
        weeks_gestation: int,
        blood_pressure: str,
        weight: float,
        glucose: float,
        height: float = 1.65,
        previous_pregnancies: int = 0,
        has_previous_risk: bool = False
    ) -> RiskAssessment:
        """
        Main method to perform comprehensive, explainable risk assessment
        """
        score = 0
        factors = []
        systolic, diastolic = self._parse_blood_pressure(blood_pressure)
        bmi = self._calculate_bmi(weight, height)

        # 1. Analyze blood pressure (preeclampsia risk)
        if systolic >= 160 or diastolic >= 110:
            score += self.RISK_FACTORS["preeclampsia_critical"]
            factors.append(f"Presión arterial CRÍTICA ({systolic}/{diastolic} mmHg)")
        elif systolic >= 140 or diastolic >= 90:
            score += self.RISK_FACTORS["preeclampsia_moderate"]
            factors.append(f"Presión arterial elevada ({systolic}/{diastolic} mmHg)")

        # 2. Analyze glucose (gestational diabetes risk)
        if glucose > 180:
            score += self.RISK_FACTORS["diabetes_critical"]
            factors.append(f"Glucosa muy elevada ({glucose} mg/dL)")
        elif glucose > 140:
            score += self.RISK_FACTORS["diabetes_moderate"]
            factors.append(f"Glucosa elevada ({glucose} mg/dL)")
        elif glucose > 110:
            score += self.RISK_FACTORS["diabetes_risk"]
            factors.append(f"Glucosa ligeramente alta ({glucose} mg/dL)")

        # 3. Analyze age
        if age >= 40:
            score += self.RISK_FACTORS["age_very_high"]
            factors.append(f"Edad materna avanzada ({age} años)")
        elif age >= 35:
            score += self.RISK_FACTORS["age_high"]
            factors.append(f"Edad materna ≥35 años ({age} años)")

        # 4. Analyze BMI
        if bmi >= 30:
            score += self.RISK_FACTORS["obesity"]
            factors.append(f"Obesidad (IMC: {bmi})")
        elif bmi >= 25:
            score += self.RISK_FACTORS["overweight"]
            factors.append(f"Sobrepeso (IMC: {bmi})")

        # 5. Previous history
        if has_previous_risk:
            score += self.RISK_FACTORS["previous_risk"]
            factors.append("Antecedentes de riesgos obstétricos")

        # 6. Previous pregnancies
        if previous_pregnancies >= 3:
            score += self.RISK_FACTORS["multiple_pregnancies"]
            factors.append(f"{previous_pregnancies} embarazos anteriores")

        # 7. Trimester-specific factors
        if weeks_gestation < 12:
            score += self.RISK_FACTORS["trimester_first"]
            factors.append("Primer trimestre (mayor riesgo de complicaciones iniciales)")
        elif weeks_gestation > 37:
            score += self.RISK_FACTORS["trimester_third_advanced"]
            factors.append("Tercer trimestre avanzado")

        # Cap score at 100
        score = min(score, 100)

        # Determine risk level
        level = self._map_score_to_level(score)

        # Generate personalized recommendations
        recommendations = self._generate_recommendations(level, factors)

        return RiskAssessment(
            score=score,
            level=level,
            contributing_factors=factors,
            recommendations=recommendations,
            details={
                "systolic_bp": systolic,
                "diastolic_bp": diastolic,
                "bmi": bmi,
                "weeks_gestation": weeks_gestation
            }
        )

    def _map_score_to_level(self, score: int) -> str:
        """Map numerical score to risk level string"""
        for level, (min_score, max_score) in self.LEVELS.items():
            if min_score <= score <= max_score:
                return level
        return "Alto"

    def _generate_recommendations(self, risk_level: str, factors: List[str]) -> List[str]:
        """Generate personalized, specific recommendations based on risk and contributing factors"""
        recommendations = []

        # Base recommendations per level
        if risk_level == "Alto":
            recommendations.extend([
                "⚠️ URGENCIA: Acuda a consulta con su obstetra INMEDIATAMENTE.",
                "Realice control prenatal SEMANAL.",
                "Monitoree su presión arterial 2 veces al día.",
                "Tome medicamentos según indicación médica (si aplica).",
            ])
        elif risk_level == "Medio":
            recommendations.extend([
                "Consulte a su médico EN LOS PRÓXIMOS 3 DÍAS.",
                "Control prenatal cada 15 días.",
                "Mantenga un registro de presión arterial y peso.",
                "Evite estrés y actividad física extenuante.",
            ])
        elif risk_level == "Bajo":
            recommendations.extend([
                "Continúe sus controles prenatales mensuales.",
                "Mantenga una alimentación saludable y equilibrada.",
                "Tome ácido fólico y vitaminas prenatales.",
                "Realice actividad física ligera autorizada (caminar, yoga prenatal).",
            ])
        else:
            recommendations.extend([
                "Mantenga sus controles prenatales periódicos.",
                "Alimentación balanceada rica en frutas y verduras.",
                "Hidratación adecuada (2-3 litros de agua al día).",
                "Descanso suficiente (7-8 horas de sueño).",
            ])

        # Specific recommendations for identified factors
        for factor in factors:
            if "presión" in factor.lower() or "preeclampsia" in factor.lower():
                recommendations.append("🔍 Reduzca el consumo de sal, embutidos y alimentos procesados.")
                recommendations.append("📝 Registre su presión arterial y compártala con su médico.")
            if "glucosa" in factor.lower() or "diabetes" in factor.lower():
                recommendations.append("🥗 Controle el consumo de carbohidratos, azúcares y refrescos.")
                recommendations.append("🍎 Prefiera frutas con bajo índice glucémico (manzana, naranja, pera).")
            if "edad" in factor.lower():
                recommendations.append("📋 Considere los estudios genéticos prenatales recomendados.")
            if "obesidad" in factor.lower() or "sobrepeso" in factor.lower():
                recommendations.append("⚖️ Siga la guía de ganancia de peso de su obstetra.")
                recommendations.append("🥤 Evite bebidas azucaradas y alimentos fritos.")
            if "antecedentes" in factor.lower():
                recommendations.append("📂 Comparta todo su historial médico con su actual obstetra.")

        # Always add medical disclaimer
        recommendations.append("---")
        recommendations.append("ℹ️ Esta información es guía y NO reemplaza la consulta médica.")

        return recommendations
