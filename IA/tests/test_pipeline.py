"""
Tests unitaires — GreenIA
Vérifie chaque couche indépendamment sans appel API.
Lance avec : python -m pytest tests/ -v
"""

import pytest
import json
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from couche1.scorer import CarbonScorer, UserInput, TransportData, EnergyData, AlimentationData
from couche2.optimizer import CarbonOptimizer
from couche3.evaluator import (
    factual_grounding_score,
    hallucination_rate,
    structure_compliance,
)


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def standard_user():
    return UserInput(
        transport=TransportData(km_voiture_par_semaine=70, km_bus_par_semaine=10),
        energie=EnergyData(heures_clim_par_jour=4, kwh_electricite_par_mois=200),
        alimentation=AlimentationData(
            repas_viande_rouge_par_semaine=4,
            repas_vegetarien_par_semaine=7,
        ),
    )


@pytest.fixture
def zero_user():
    """Utilisateur avec habitudes neutres."""
    return UserInput(
        transport=TransportData(),
        energie=EnergyData(),
        alimentation=AlimentationData(),
    )


# ─── Tests Couche 1 ───────────────────────────────────────────────────────────

class TestCouche1:
    def test_score_positif(self, standard_user):
        scorer = CarbonScorer()
        result = scorer.compute(standard_user)
        assert result["initial_score"]["total_kgCO2e"] > 0

    def test_score_zero_pour_utilisateur_neutre(self, zero_user):
        scorer = CarbonScorer()
        result = scorer.compute(zero_user)
        assert result["initial_score"]["total_kgCO2e"] == 0.0

    def test_structure_payload(self, standard_user):
        scorer = CarbonScorer()
        result = scorer.compute(standard_user)
        assert "metadata" in result
        assert "initial_score" in result
        assert "raw_input" in result
        assert "user_id" in result["metadata"]

    def test_facteur_voiture(self):
        """Vérifie le facteur ADEME voiture : 0.218 kgCO2e/km."""
        scorer = CarbonScorer()
        user = UserInput(
            transport=TransportData(km_voiture_par_semaine=100),
            energie=EnergyData(),
            alimentation=AlimentationData(),
        )
        result = scorer.compute(user)
        # 100 km/sem × 4.33 sem × 0.218 = 94.39 kgCO2e
        expected = round(100 * 4.33 * 0.218, 2)
        assert abs(result["initial_score"]["transport_kgCO2e"] - expected) < 0.1

    def test_sous_scores_sommables(self, standard_user):
        scorer = CarbonScorer()
        result = scorer.compute(standard_user)
        s = result["initial_score"]
        total_computed = round(s["transport_kgCO2e"] + s["energie_kgCO2e"] + s["alimentation_kgCO2e"], 1)
        assert abs(total_computed - s["total_kgCO2e"]) < 0.5


# ─── Tests Couche 2 ───────────────────────────────────────────────────────────

class TestCouche2:

    @pytest.fixture
    def c1_payload(self, standard_user):
        return CarbonScorer().compute(standard_user)

    def test_reduction_atteinte(self, c1_payload):
        optimizer = CarbonOptimizer(target_reduction_percent=20.0)
        result = optimizer.optimize(c1_payload)
        assert result["metrics"]["relative_reduction_percent"] >= 15.0  # marge 5%

    def test_score_optimise_inferieur_initial(self, c1_payload):
        optimizer = CarbonOptimizer()
        result = optimizer.optimize(c1_payload)
        assert result["metrics"]["optimized_carbon_score_kgCO2e"] < result["metrics"]["initial_carbon_score_kgCO2e"]

    def test_au_moins_une_recommandation(self, c1_payload):
        optimizer = CarbonOptimizer()
        result = optimizer.optimize(c1_payload)
        assert len(result["recom_vectors"]) > 0

    def test_structure_payload_c2(self, c1_payload):
        optimizer = CarbonOptimizer()
        result = optimizer.optimize(c1_payload)
        assert "metrics" in result
        assert "recom_vectors" in result
        assert "solver_status" in result

    def test_impacts_positifs(self, c1_payload):
        optimizer = CarbonOptimizer()
        result = optimizer.optimize(c1_payload)
        for vec in result["recom_vectors"]:
            assert vec["impact_reduction_kgCO2e"] > 0


# ─── Tests Couche 3 (métriques, sans appel API) ───────────────────────────────

class TestCouche3Evaluator:

    @pytest.fixture
    def sample_payload(self):
        return {
            "metrics": {
                "initial_carbon_score_kgCO2e": 95.0,
                "optimized_carbon_score_kgCO2e": 63.0,
                "absolute_reduction_kgCO2e": 32.0,
                "relative_reduction_percent": 33.68,
            },
            "recom_vectors": [
                {"dimension": "transport", "impact_reduction_kgCO2e": 14.7},
            ],
        }

    def test_factual_grounding_parfait(self, sample_payload):
        text = "Score initial 95.0 kgCO2e réduit à 63.0, soit 32.0 kg évités, impact 14.7."
        score = factual_grounding_score(text, sample_payload)
        assert score == 1.0

    def test_factual_grounding_nul(self, sample_payload):
        text = "Le bilan carbone peut être amélioré grâce à diverses actions."
        score = factual_grounding_score(text, sample_payload)
        assert score == 0.0

    def test_structure_complete(self):
        text = "## 🌱 intro ## 🚀 axe ## ✅ impact"
        result = structure_compliance(text)
        assert result["score"] == 1.0

    def test_structure_incomplete(self):
        text = "## 🌱 intro seulement"
        result = structure_compliance(text)
        assert result["score"] < 1.0

    def test_hallucination_chiffre_invente(self, sample_payload):
        text = "La réduction est de 999.99 kgCO2e soit 87.5%"
        result = hallucination_rate(text, sample_payload)
        assert result["hallucination_rate"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
