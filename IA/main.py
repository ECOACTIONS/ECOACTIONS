"""
PIPELINE PRINCIPAL — GreenIA
Orchestration complète : Couche 1 → Couche 2 → Couche 3
Point d'entrée unique pour générer un plan d'action carbone complet.
"""

import json
import sys
import os

# Ajout des chemins de modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from couche1.scorer import CarbonScorer, UserInput, TransportData, EnergyData, AlimentationData
from couche2.optimizer import CarbonOptimizer
from couche3.xai_explainer import XAIExplainer


def run_pipeline(
    user_input: UserInput,
    target_reduction_percent: float = 33.0,
    verbose: bool = True,
) -> dict:
    """
    Exécute le pipeline complet GreenIA.

    Args:
        user_input: habitudes de vie de l'utilisateur (Couche 1)
        target_reduction_percent: objectif de réduction CO2e en %
        verbose: afficher les étapes intermédiaires

    Returns:
        dict avec tous les résultats : score, plan optimisé, explication XAI
    """

    # ── COUCHE 1 : Scoring ────────────────────────────────────────────────────
    if verbose:
        print("⚙️  [Couche 1] Calcul du score carbone initial...")

    scorer = CarbonScorer()
    couche1_payload = scorer.compute(user_input)

    if verbose:
        score = couche1_payload["initial_score"]["total_kgCO2e"]
        print(f"   → Score initial : {score} kgCO2e/mois")

    # ── COUCHE 2 : Optimisation ───────────────────────────────────────────────
    if verbose:
        print("⚙️  [Couche 2] Optimisation linéaire (PuLP)...")

    optimizer = CarbonOptimizer(target_reduction_percent=target_reduction_percent)
    couche2_payload = optimizer.optimize(couche1_payload)

    if verbose:
        metrics = couche2_payload["metrics"]
        print(f"   → Score optimisé : {metrics['optimized_carbon_score_kgCO2e']} kgCO2e/mois")
        print(f"   → Réduction : -{metrics['absolute_reduction_kgCO2e']} kgCO2e ({metrics['relative_reduction_percent']}%)")
        print(f"   → Statut solveur : {couche2_payload['solver_status']}")
        print(f"   → {len(couche2_payload['recom_vectors'])} actions recommandées")

    # ── COUCHE 3 : XAI Narrative ──────────────────────────────────────────────
    if verbose:
        print("⚙️  [Couche 3] Génération de l'explication XAI (Gemini)...")

    explainer = XAIExplainer()
    couche3_result = explainer.generate(couche2_payload)

    if verbose:
        validation = couche3_result["validation"]
        print(f"   → Modèle : {couche3_result['model_used']}")
        print(f"   → Structure OK : {validation['sections_structure_ok']}")
        print(f"   → Chiffres clés présents : {validation['key_figures_present']}")
        print(f"   → Risque hallucination : {validation['hallucination_risk']}")

    # ── Résultat final ────────────────────────────────────────────────────────
    return {
        "couche1": couche1_payload,
        "couche2": couche2_payload,
        "couche3": {
            "narrative": couche3_result["xai_narrative"],
            "validation": couche3_result["validation"],
            "model": couche3_result["model_used"],
        },
    }


# ─── Exemple d'utilisation ───────────────────────────────────────────────────

if __name__ == "__main__":
    print("🌿 GreenIA — Pipeline Carbone Complet\n" + "="*50)

    user = UserInput(
        transport=TransportData(
            km_voiture_par_semaine=70,
            km_bus_par_semaine=10,
            vols_court_courrier_par_an=2,
        ),
        energie=EnergyData(
            heures_clim_par_jour=4,
            kwh_electricite_par_mois=200,
            kwh_gaz_par_mois=50,
        ),
        alimentation=AlimentationData(
            repas_viande_rouge_par_semaine=4,
            repas_viande_blanche_par_semaine=3,
            repas_vegetarien_par_semaine=7,
        ),
    )

    results = run_pipeline(user, target_reduction_percent=33.0, verbose=True)

    print("\n" + "="*50)
    print("📋 PLAN D'ACTION GÉNÉRÉ :\n")
    print(results["couche3"]["narrative"])
    print("\n" + "="*50)

    # Sauvegarde JSON complète
    with open("output_pipeline.json", "w", encoding="utf-8") as f:
        # Exclure la narrative du JSON (déjà affichée)
        output = {k: v for k, v in results.items() if k != "couche3"}
        output["couche3_validation"] = results["couche3"]["validation"]
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("💾 Résultats complets sauvegardés dans output_pipeline.json")
