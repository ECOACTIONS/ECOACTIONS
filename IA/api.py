"""
API REST — GreenIA
Expose le pipeline complet via FastAPI.
POST /analyze → retourne score + plan optimisé + explication XAI
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from couche1.scorer import CarbonScorer, UserInput, TransportData, EnergyData, AlimentationData
from couche2.optimizer import CarbonOptimizer
from couche3.xai_explainer import XAIExplainer

app = FastAPI(title="GreenIA API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

scorer = CarbonScorer()
optimizer = CarbonOptimizer()
explainer = XAIExplainer()


class AnalyzeRequest(BaseModel):
    user_input: UserInput
    target_reduction_percent: float = 33.0


@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        c1 = scorer.compute(request.user_input)
        c2 = optimizer.optimize(c1)
        c3 = explainer.generate(c2)
        return {
            "score_initial": c1["initial_score"]["total_kgCO2e"],
            "score_optimise": c2["metrics"]["optimized_carbon_score_kgCO2e"],
            "reduction_kgco2e": c2["metrics"]["absolute_reduction_kgCO2e"],
            "reduction_percent": c2["metrics"]["relative_reduction_percent"],
            "actions": c2["recom_vectors"],
            "narrative": c3["xai_narrative"],
            "validation": c3["validation"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}
