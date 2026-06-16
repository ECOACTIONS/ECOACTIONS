from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.calculator import CarbonCalculator
from backend.services.optimizer import ActionOptimizer
from backend.services.llm import LLMService

router = APIRouter()
calculator = CarbonCalculator()
optimizer = ActionOptimizer()
llm = LLMService()

class UserActivityData(BaseModel):
    electricity_kwh: float = 0
    generator_liters: float = 0
    gas_kg: float = 0
    motorcycle_km: float = 0
    shared_taxi_km: float = 0
    car_km: float = 0
    solid_waste_kg: float = 0
    target_reduction_pct: float = 20.0  # Objectif par défaut : 20%

@router.post("/calculate")
async def calculate_and_optimize(data: UserActivityData):
    """
    Calcule le bilan, optimise les actions et génère un conseil IA.
    """
    # 1. Calcul du bilan brut
    assessment = calculator.calculate_total_assessment(data.model_dump())
    
    # 2. Calcul de l'objectif de réduction en kg CO2
    target_kg = assessment["total_co2"] * (data.target_reduction_pct / 100)
    
    # 3. Optimisation des actions
    recommendations = optimizer.optimize(assessment, target_kg)
    
    # 4. Génération de la synthèse par l'IA
    ai_summary = await llm.generate_educational_summary(assessment, recommendations)
    
    return {
        "assessment": assessment,
        "recommendations": recommendations,
        "ai_summary": ai_summary
    }
