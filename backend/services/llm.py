import os
import google.generativeai as genai
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class LLMService:
    """
    Service d'intégration avec Gemini pour la vulgarisation pédagogique.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None

    async def generate_educational_summary(self, assessment_data: Dict, recommendations: List[Dict]) -> str:
        """
        Génère une synthèse pédagogique et encourageante.
        """
        if not self.model:
            return "Note : L'IA n'est pas configurée (Clé API manquante). Voici vos recommandations brutes."

        # Construction du prompt
        prompt = f"""
        Tu es 'EcoCoach AI', un expert en environnement bienveillant et pédagogue spécialisé dans le contexte du Cameroun.
        Ton rôle est d'expliquer les résultats d'un bilan carbone à un citoyen et de le motiver à agir.

        DONNÉES DU BILAN :
        - Impact Énergie : {assessment_data['energy_impact']} kg CO2e
        - Impact Transport : {assessment_data['transport_impact']} kg CO2e
        - Impact Déchets : {assessment_data['waste_impact']} kg CO2e
        - Impact Total : {assessment_data['total_co2']} kg CO2e

        PLAN D'ACTION SUGGÉRÉ :
        {recommendations}

        CONSIGNES :
        1. Utilise un ton encourageant, simple et pédagogique.
        2. Intègre des références locales camerounaises (ex: parler du "benz-skin", des taxis partagés, du climat local, ou d'expressions comme 'on est ensemble').
        3. Explique concrètement pourquoi ces actions sont bénéfiques pour le portefeuille de l'utilisateur ET pour l'environnement au pays.
        4. Ta réponse doit être en français, structurée et concise.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Erreur lors de la génération du conseil : {str(e)}"
