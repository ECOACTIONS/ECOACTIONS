from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from ..services.llm import LLMService

router = APIRouter(prefix="/chat", tags=["AI Chat"])

llm_service = LLMService()

class ChatRequest(BaseModel):
    assessment: Dict
    recommendations: List[Dict]
    user_message: str = None  # Pour futur chat interactif

@router.post("/summary")
async def generate_summary(request: ChatRequest):
    """
    Génère une synthèse pédagogique via Gemini
    """
    if not request.assessment or not request.recommendations:
        raise HTTPException(status_code=400, detail="Données d'assessment et recommandations requises")
    
    summary = await llm_service.generate_educational_summary(
        request.assessment, 
        request.recommendations
    )
    
    return {
        "ai_summary": summary,
        "status": "success"
    }

# Route future pour un chat conversationnel
@router.post("/message")
async def chat_message(request: ChatRequest):
    """
    À développer : chat interactif avec contexte
    """
    return {
        "response": "Fonctionnalité de chat interactif en cours de développement.",
        "note": "Utilise /chat/summary pour le moment."
    }