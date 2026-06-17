from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, List
from ..database.postgres import get_db
from ..models.assessment import Assessment
from ..services.optimizer import ActionOptimizer

router = APIRouter(prefix="/optimize", tags=["Optimization"])

class OptimizationRequest(BaseModel):
    assessment_id: int
    target_reduction_pct: float = 20.0

class OptimizationResponse(BaseModel):
    recommendations: List[Dict]
    target_kg: float

optimizer = ActionOptimizer()

@router.post("/", response_model=OptimizationResponse)
async def optimize_actions(request: OptimizationRequest, db: Session = Depends(get_db)):
    # Récupérer l'assessment
    assessment = db.query(Assessment).filter(Assessment.id == request.assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment non trouvé")
    
    # Préparer les impacts actuels
    current_impacts = {
        "energy_impact": assessment.energy_score,
        "transport_impact": assessment.transport_score,
        "waste_impact": assessment.waste_score
    }
    
    target_kg = assessment.total_co2 * (request.target_reduction_pct / 100)
    
    # Optimisation
    recommendations = optimizer.optimize(current_impacts, target_kg)
    
    return {
        "recommendations": recommendations,
        "target_kg": round(target_kg, 2)
    }