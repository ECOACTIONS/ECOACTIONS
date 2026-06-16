from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value
from typing import List, Dict

class ActionOptimizer:
    """
    Moteur d'optimisation sous contraintes pour suggérer des écogestes.
    Objectif : Minimiser l'effort total tout en atteignant un objectif de réduction CO2.
    """

    def __init__(self):
        # Base de données simplifiée d'écogestes (Impact relatif et Effort de 1 à 5)
        # L'impact est ici un coefficient de réduction potentiel de la catégorie
        self.potential_actions = [
            {"id": "reduce_ac", "name": "Réduire la climatisation (2h/jour)", "category": "energy", "impact_factor": 0.15, "effort": 1},
            {"id": "carpooling", "name": "Pratiquer le covoiturage", "category": "transport", "impact_factor": 0.30, "effort": 3},
            {"id": "reduce_generator", "name": "Limiter l'usage du groupe électrogène", "category": "energy", "impact_factor": 0.20, "effort": 4},
            {"id": "bike_short_dist", "name": "Vélo/Marche pour courtes distances", "category": "transport", "impact_factor": 0.10, "effort": 2},
            {"id": "waste_sorting", "name": "Tri et compostage des déchets", "category": "waste", "impact_factor": 0.25, "effort": 3},
        ]

    def optimize(self, current_impacts: Dict, target_reduction_total: float) -> List[Dict]:
        """
        Résout le problème d'optimisation linéaire.
        """
        # 1. Créer le problème
        prob = LpProblem("Minimize_Effort", LpMinimize)

        # 2. Variables de décision (binaire : on fait l'action ou pas)
        # Dans une version plus complexe, on pourrait utiliser des variables continues (0 à 1)
        action_vars = {a["id"]: LpVariable(f"action_{a['id']}", 0, 1, cat="Binary") for a in self.potential_actions}

        # 3. Fonction objectif : Minimiser l'effort global
        prob += lpSum([action_vars[a["id"]] * a["effort"] for a in self.potential_actions])

        # 4. Contrainte : Atteindre l'objectif de réduction
        # Réduction totale = Somme(Action_Binaire * Impact_Catégorie * Facteur_Action)
        total_reduction = []
        for a in self.potential_actions:
            category_impact = current_impacts.get(f"{a['category']}_impact", 0)
            reduction = action_vars[a["id"]] * (category_impact * a["impact_factor"])
            total_reduction.append(reduction)
            
        prob += lpSum(total_reduction) >= target_reduction_total

        # 5. Résolution
        prob.solve()

        # 6. Formater les résultats
        recommendations = []
        for a in self.potential_actions:
            if value(action_vars[a["id"]]) == 1:
                category_impact = current_impacts.get(f"{a['category']}_impact", 0)
                estimated_reduction = round(category_impact * a["impact_factor"], 2)
                recommendations.append({
                    "action": a["name"],
                    "effort": a["effort"],
                    "reduction_estimated": estimated_reduction
                })

        return recommendations
