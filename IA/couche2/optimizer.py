"""
COUCHE 2 — Optimisation Linéaire (PuLP)
Reçoit le score initial de la Couche 1 et retourne le plan d'actions optimal
minimisant le CO2e sous contraintes comportementales et réglementaires.
"""

import pulp
import json
from typing import Optional


# ─── Définition des leviers d'action disponibles ─────────────────────────────

LEVERS = {
    # Transport
    "transport_voiture_vers_bus": {
        "dimension": "transport",
        "action": "Substitution Véhicule Individuel → Bus",
        "unite": "km/mois",
        "impact_per_unit": 0.218 - 0.080,   # delta kgCO2e/km substitué
        "max_applicable_ratio": 0.80,         # max 80% des km voiture substituables
        "description": "Remplacer les trajets voiture par le bus urbain",
    },
    "transport_voiture_vers_velo": {
        "dimension": "transport",
        "action": "Substitution Véhicule Individuel → Vélo/Marche",
        "unite": "km/mois",
        "impact_per_unit": 0.218,
        "max_applicable_ratio": 0.30,
        "description": "Remplacer les courts trajets voiture par le vélo ou la marche",
    },
    "energie_reduction_clim": {
        "dimension": "energie",
        "action": "Modération utilisation climatisation",
        "unite": "heures/jour",
        "impact_per_unit": 0.078 * 30.44,   # kgCO2e par heure/jour réduite (sur 1 mois)
        "max_reduction": 4.0,               # max 4h/jour de réduction
        "description": "Réduire le nombre d'heures de climatisation quotidienne",
    },
    "energie_reduction_electricite": {
        "dimension": "energie",
        "action": "Sobriété électrique générale",
        "unite": "kWh/mois",
        "impact_per_unit": 0.052,
        "max_reduction_ratio": 0.20,
        "description": "Réduire la consommation électrique de 20%",
    },
    "alimentation_viande_rouge_vers_vege": {
        "dimension": "alimentation",
        "action": "Substitution Viande Rouge → Repas Végétarien",
        "unite": "repas/mois",
        "impact_per_unit": 6.8 - 0.5,       # delta kgCO2e/repas
        "max_applicable_ratio": 0.50,
        "description": "Remplacer la moitié des repas de viande rouge par des repas végétariens",
    },
    "alimentation_viande_blanche_vers_vege": {
        "dimension": "alimentation",
        "action": "Substitution Viande Blanche → Repas Végétarien",
        "unite": "repas/mois",
        "impact_per_unit": 1.5 - 0.5,
        "max_applicable_ratio": 0.30,
        "description": "Remplacer 30% des repas de viande blanche par des repas végétariens",
    },
}

SEMAINES_PAR_MOIS = 4.33
JOURS_PAR_MOIS = 30.44


class CarbonOptimizer:
    """
    Optimiseur linéaire PuLP.
    Minimise le delta d'émissions sous contrainte de faisabilité comportementale.
    """

    def __init__(self, target_reduction_percent: float = 33.0):
        self.target_reduction_percent = target_reduction_percent

    def optimize(self, couche1_payload: dict) -> dict:
        initial = couche1_payload["initial_score"]
        detail = initial["detail"]
        raw = couche1_payload["raw_input"]

        total_initial = initial["total_kgCO2e"]
        target_reduction = total_initial * (self.target_reduction_percent / 100)

        # ── Bornes max par levier ─────────────────────────────────────────────
        km_voiture_mois = raw["transport"]["km_voiture_par_semaine"] * SEMAINES_PAR_MOIS
        heures_clim_jour = raw["energie"]["heures_clim_par_jour"]
        kwh_elec_mois = raw["energie"]["kwh_electricite_par_mois"]
        repas_rouge_mois = raw["alimentation"]["repas_viande_rouge_par_semaine"] * SEMAINES_PAR_MOIS
        repas_blanc_mois = raw["alimentation"]["repas_viande_blanche_par_semaine"] * SEMAINES_PAR_MOIS

        max_bounds = {
            "transport_voiture_vers_bus":
                km_voiture_mois * LEVERS["transport_voiture_vers_bus"]["max_applicable_ratio"],
            "transport_voiture_vers_velo":
                km_voiture_mois * LEVERS["transport_voiture_vers_velo"]["max_applicable_ratio"],
            "energie_reduction_clim":
                min(heures_clim_jour, LEVERS["energie_reduction_clim"]["max_reduction"]),
            "energie_reduction_electricite":
                kwh_elec_mois * LEVERS["energie_reduction_electricite"]["max_reduction_ratio"],
            "alimentation_viande_rouge_vers_vege":
                repas_rouge_mois * LEVERS["alimentation_viande_rouge_vers_vege"]["max_applicable_ratio"],
            "alimentation_viande_blanche_vers_vege":
                repas_blanc_mois * LEVERS["alimentation_viande_blanche_vers_vege"]["max_applicable_ratio"],
        }

        # ── Problème PuLP ─────────────────────────────────────────────────────
        prob = pulp.LpProblem("GreenIA_Carbon_Optimization", pulp.LpMinimize)

        # Variables de décision (quantité appliquée par levier)
        vars = {
            key: pulp.LpVariable(key, lowBound=0, upBound=max_bounds[key])
            for key in LEVERS
        }

        # Objectif : minimiser le total des actions (effort minimal pour atteindre la cible)
        # — on peut aussi maximiser la réduction, selon la philosophie choisie
        prob += pulp.lpSum(vars[k] for k in vars), "Minimiser_effort_total"

        # Contrainte principale : atteindre la réduction cible
        total_reduction_expr = pulp.lpSum(
            vars[k] * LEVERS[k]["impact_per_unit"] for k in LEVERS
        )
        prob += total_reduction_expr >= target_reduction, "Reduction_cible"

        # Contrainte : ne pas dépasser les km voiture disponibles au total
        prob += (
            vars["transport_voiture_vers_bus"] + vars["transport_voiture_vers_velo"]
            <= km_voiture_mois
        ), "Km_voiture_max"

        # ── Résolution ────────────────────────────────────────────────────────
        solver = pulp.PULP_CBC_CMD(msg=0)
        status = prob.solve(solver)

        if pulp.LpStatus[status] != "Optimal":
            # Fallback : réduction max atteignable
            return self._fallback_result(couche1_payload, max_bounds)

        # ── Construction du payload Couche 3 ──────────────────────────────────
        recom_vectors = []
        total_reduction_achieved = 0.0

        for key, var in vars.items():
            val = var.varValue or 0.0
            if val < 0.01:
                continue
            lever = LEVERS[key]
            impact = round(val * lever["impact_per_unit"], 2)
            total_reduction_achieved += impact

            recom_vectors.append({
                "dimension": lever["dimension"],
                "action": lever["action"],
                "delta_input": f"{round(val, 1)} {lever['unite']}",
                "impact_reduction_kgCO2e": impact,
                "description": lever["description"],
            })

        # Trier par impact décroissant
        recom_vectors.sort(key=lambda x: x["impact_reduction_kgCO2e"], reverse=True)

        optimized_score = round(total_initial - total_reduction_achieved, 2)

        return {
            "metadata": couche1_payload["metadata"],
            "metrics": {
                "initial_carbon_score_kgCO2e": total_initial,
                "optimized_carbon_score_kgCO2e": optimized_score,
                "absolute_reduction_kgCO2e": round(total_reduction_achieved, 2),
                "relative_reduction_percent": round(
                    (total_reduction_achieved / total_initial) * 100, 2
                ),
            },
            "recom_vectors": recom_vectors,
            "solver_status": pulp.LpStatus[status],
        }

    def _fallback_result(self, couche1_payload, max_bounds) -> dict:
        """Retourne le maximum atteignable si la cible est irréalisable."""
        initial = couche1_payload["initial_score"]["total_kgCO2e"]
        recom_vectors = []
        total_reduction = 0.0

        for key, max_val in max_bounds.items():
            if max_val < 0.01:
                continue
            lever = LEVERS[key]
            impact = round(max_val * lever["impact_per_unit"], 2)
            total_reduction += impact
            recom_vectors.append({
                "dimension": lever["dimension"],
                "action": lever["action"],
                "delta_input": f"{round(max_val, 1)} {lever['unite']}",
                "impact_reduction_kgCO2e": impact,
                "description": lever["description"],
            })

        recom_vectors.sort(key=lambda x: x["impact_reduction_kgCO2e"], reverse=True)
        optimized = round(initial - total_reduction, 2)

        return {
            "metadata": couche1_payload["metadata"],
            "metrics": {
                "initial_carbon_score_kgCO2e": initial,
                "optimized_carbon_score_kgCO2e": optimized,
                "absolute_reduction_kgCO2e": round(total_reduction, 2),
                "relative_reduction_percent": round((total_reduction / initial) * 100, 2),
            },
            "recom_vectors": recom_vectors,
            "solver_status": "Fallback_MaxReduction",
        }


# ─── Test rapide ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Simule un payload Couche 1
    sample_c1 = {
        "metadata": {"user_id": "usr_test", "timestamp": "2026-06-14T00:00:00Z"},
        "initial_score": {
            "total_kgCO2e": 95.0,
            "transport_kgCO2e": 65.0,
            "energie_kgCO2e": 18.0,
            "alimentation_kgCO2e": 12.0,
            "detail": {
                "transport": {"voiture": 65.0},
                "energie": {"clim": 9.5, "electricite": 8.5},
                "alimentation": {"viande_rouge": 12.0},
            },
        },
        "raw_input": {
            "transport": {"km_voiture_par_semaine": 70, "km_bus_par_semaine": 0,
                          "km_velo_par_semaine": 0, "km_train_par_semaine": 0,
                          "vols_court_courrier_par_an": 0, "vols_long_courrier_par_an": 0},
            "energie": {"heures_clim_par_jour": 4.0,
                        "kwh_electricite_par_mois": 200.0, "kwh_gaz_par_mois": 0.0},
            "alimentation": {"repas_viande_rouge_par_semaine": 4, "repas_viande_blanche_par_semaine": 3,
                             "repas_poisson_par_semaine": 0, "repas_vegetarien_par_semaine": 7},
        },
    }

    optimizer = CarbonOptimizer(target_reduction_percent=33.0)
    result = optimizer.optimize(sample_c1)
    print(json.dumps(result, indent=2, ensure_ascii=False))
