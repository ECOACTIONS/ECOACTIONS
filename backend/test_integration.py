import asyncio
import json
from backend.services.calculator import CarbonCalculator
from backend.services.optimizer import ActionOptimizer
from backend.services.llm import LLMService

async def test_backend_flow():
    print("🚀 Démarrage du test d'intégration EcoImpact AI...\n")
    
    # 1. Simulation de données utilisateur (Données camerounaises typiques)
    user_data = {
        "electricity_kwh": 150,      # Consommation mensuelle moyenne
        "generator_liters": 20,     # Usage régulier suite aux délestages
        "gas_kg": 12.5,             # Une bouteille de gaz SCTM/Glocal Gaz
        "motorcycle_km": 100,       # Trajets en Benz-skin
        "shared_taxi_km": 200,      # Trajets quotidiens
        "car_km": 0,
        "solid_waste_kg": 30,       # Production de déchets
        "target_reduction_pct": 25  # Objectif de réduction de 25%
    }
    
    print(f"📊 Données d'entrée : {json.dumps(user_data, indent=2, ensure_ascii=False)}")

    # 2. Test du Calculateur
    calculator = CarbonCalculator()
    assessment = calculator.calculate_total_assessment(user_data)
    print(f"\n✅ Bilan calculé : {assessment['total_co2']} kg CO2e")
    print(f"   (Énergie: {assessment['energy_impact']}, Transport: {assessment['transport_impact']}, Déchets: {assessment['waste_impact']})")

    # 3. Test de l'Optimiseur
    optimizer = ActionOptimizer()
    target_reduction = assessment["total_co2"] * (user_data["target_reduction_pct"] / 100)
    recommendations = optimizer.optimize(assessment, target_reduction)
    
    print(f"\n🎯 Objectif de réduction : {round(target_reduction, 2)} kg CO2e")
    print("✅ Actions recommandées par l'optimiseur :")
    for rec in recommendations:
        print(f"   - {rec['action']} (Effort: {rec['effort']}, Gain: {rec['reduction_estimated']} kg)")

    # 4. Test de l'IA (LLM)
    print("\n🤖 Appel à EcoCoach AI (Gemini)...")
    llm = LLMService()
    # On passe des recommandations formatées pour le prompt
    summary = await llm.generate_educational_summary(assessment, recommendations)
    
    print("\n--- SYNTHÈSE DE L'IA ---")
    print(summary)
    print("------------------------")

if __name__ == "__main__":
    asyncio.run(test_backend_flow())
