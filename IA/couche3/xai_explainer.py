"""
COUCHE 3 — XAI via LLM (Gemini)
Traduit le payload brut de la Couche 2 en plan d'action narratif,
pédagogique et motivant pour l'utilisateur final.
"""

import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai
import time

load_dotenv()

# ─── Few-shot examples (améliore le suivi de format) ─────────────────────────

FEW_SHOT_EXAMPLES = """
--- EXEMPLE DE SORTIE ATTENDUE ---
INPUT MÉTRIQUES : {"initial": 95.0, "optimisé": 63.0, "réduction": 32.0 kgCO2e, "pourcentage": 33.68%}
INPUT ACTIONS : [Transport: -14.7 kgCO2e | Énergie: -11.2 kgCO2e]

## 🌱 Synthèse de votre bilan carbone
Votre empreinte carbone mensuelle actuelle est de 95 kg CO₂e. Grâce aux recommandations personnalisées
de notre algorithme d'optimisation, elle peut être ramenée à 63 kg CO₂e, soit une réduction de
32 kg CO₂e (−33,7%). C'est l'équivalent de la séquestration annuelle d'un jeune arbre pendant 16 mois.

## 🚀 Axe prioritaire : Transport (impact le plus fort)
L'action la plus efficace est la substitution de vos trajets en voiture vers les transports en commun.
En changeant de mode de déplacement sur 70 km de vos trajets mensuels, vous évitez l'émission de 14,7 kg
CO₂e — soit 46% de votre objectif de réduction total. Selon la Base Empreinte® ADEME, le bus urbain
émet 0,080 kg CO₂e/km contre 0,218 kg CO₂e/km pour un véhicule thermique de segment B/C.

## ✅ Impact concret et équivalences
- 🚌 Substituer 70 km voiture → bus = économiser 14,7 kg CO₂e/mois
- ❄️ Réduire la clim de 4h/jour = économiser 11,2 kg CO₂e/mois
- 🌍 Total : -32 kg CO₂e = conduire 147 km en moins chaque mois
"""


# ─── Prompt système (zéro hallucination) ─────────────────────────────────────

SYSTEM_INSTRUCTION = """
Vous êtes le module d'Explicabilité (XAI) de l'application GreenIA, expert en transition bas-carbone.
Votre rôle : traduire les résultats bruts d'une optimisation linéaire en un plan d'action narratif,
pédagogique et motivant, destiné à un utilisateur non-expert.

RÈGLES ABSOLUES (violations = réponse invalide) :
1. Ne citez AUCUN chiffre, quantité ou pourcentage qui ne figure pas explicitement dans le JSON fourni.
2. Fondez vos équivalences d'impact EXCLUSIVEMENT sur les données ADEME fournies.
3. Adoptez un ton professionnel, bienveillant et orienté solutions.
4. Structurez TOUJOURS la réponse en 3 sections exactes avec ces titres emoji :
   - ## 🌱 Synthèse de votre bilan carbone
   - ## 🚀 Axe prioritaire : [NOM DIMENSION] (impact le plus fort)
   - ## ✅ Impact concret et équivalences
5. Rédigez en français, langage accessible, paragraphes courts.
6. N'inventez aucune donnée contextuelle (météo, région, profession, etc.).
7. Chaque section fait entre 3 et 6 phrases.

Voici un exemple de sortie de qualité attendue :
""" + FEW_SHOT_EXAMPLES


class XAIExplainer:
    """Génère les explications narratives XAI via Gemini."""

    def __init__(self, model_name: str = None):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY manquante dans .env")

        genai.configure(api_key=api_key)
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=SYSTEM_INSTRUCTION,
        )



    def generate(self, couche2_payload: dict) -> dict:
        user_prompt = f"""
    Voici les données d'optimisation carbone calculées par l'algorithme à analyser et à expliquer :

    {json.dumps(couche2_payload, indent=2, ensure_ascii=False)}

    Génère maintenant le plan d'action narratif structuré en respectant strictement les 3 sections demandées.
    """
        # Retry automatique sur quota 429
        for attempt in range(3):
            try:
                response = self.model.generate_content(
                    user_prompt,
                    generation_config={
                        "temperature": 0.1,
                        "top_p": 0.95,
                        "max_output_tokens": 1024,
                    },
                )
                break
            except Exception as e:
                if "429" in str(e) and attempt < 2:
                    wait = 60 * (attempt + 1)
                    print(f"⏳ Quota atteint, attente {wait}s...")
                    time.sleep(wait)
                else:
                    raise

        generated_text = response.text
        validation = self._validate_output(generated_text, couche2_payload)
        return {
            "xai_narrative": generated_text,
            "model_used": self.model_name,
            "validation": validation,
            "metadata": couche2_payload.get("metadata", {}),
        }
    def _validate_output(self, text: str, payload: dict) -> dict:
        """
        Post-validation : vérifie la cohérence factuelle du texte généré.
        Détecte les hallucinations numériques.
        """
        # Chiffres autorisés (présents dans le payload)
        authorized_numbers = set(
            re.findall(r'\d+\.?\d*', json.dumps(payload))
        )
        # Chiffres présents dans le texte généré
        generated_numbers = set(re.findall(r'\d+\.?\d*', text))
        suspicious = generated_numbers - authorized_numbers

        # Vérification des 3 sections obligatoires
        sections_ok = all(
            marker in text
            for marker in ["🌱", "🚀", "✅"]
        )

        # Vérification que les métriques clés sont mentionnées
        metrics = payload.get("metrics", {})
        initial = str(metrics.get("initial_carbon_score_kgCO2e", ""))
        optimized = str(metrics.get("optimized_carbon_score_kgCO2e", ""))
        key_figures_present = initial in text and optimized in text

        return {
            "sections_structure_ok": sections_ok,
            "key_figures_present": key_figures_present,
            "suspicious_numbers": list(suspicious)[:10],  # max 10 pour lisibilité
            "hallucination_risk": len(suspicious) > 5,
        }


# ─── Test rapide ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sample_c2 = {
        "metadata": {"user_id": "usr_test", "timestamp": "2026-06-14T00:00:00Z"},
        "metrics": {
            "initial_carbon_score_kgCO2e": 95.0,
            "optimized_carbon_score_kgCO2e": 63.0,
            "absolute_reduction_kgCO2e": 32.0,
            "relative_reduction_percent": 33.68,
        },
        "recom_vectors": [
            {
                "dimension": "transport",
                "action": "Substitution Véhicule Individuel → Bus",
                "delta_input": "70.0 km/mois",
                "impact_reduction_kgCO2e": 14.7,
            },
            {
                "dimension": "energie",
                "action": "Modération utilisation climatisation",
                "delta_input": "4.0 heures/jour",
                "impact_reduction_kgCO2e": 11.2,
            },
        ],
        "solver_status": "Optimal",
    }

    explainer = XAIExplainer()
    result = explainer.generate(sample_c2)
    print("\n" + "="*60)
    print(result["xai_narrative"])
    print("\n── Validation ──")
    print(json.dumps(result["validation"], indent=2, ensure_ascii=False))
