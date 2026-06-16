"""
COUCHE 3 — Évaluation & Métriques XAI
Mesure la qualité des explications générées :
- Fidélité factuelle (chiffres corrects)
- Similarité sémantique (BERTScore)
- Détection d'hallucinations numériques
- LLM-as-Judge (Gemini évalue Gemini)
"""

import json
import re
import os
from typing import Optional
from dotenv import load_dotenv
from bert_score import score
from rouge_score import rouge_scorer

load_dotenv()


# ─── 1. Métriques automatiques ───────────────────────────────────────────────

def factual_grounding_score(generated_text: str, json_payload: dict) -> float:
    """
    Vérifie que les chiffres clés du JSON sont bien présents dans le texte généré.
    Retourne un score entre 0.0 et 1.0.
    """
    metrics = json_payload.get("metrics", {})
    key_values = [
        str(metrics.get("initial_carbon_score_kgCO2e", "")),
        str(metrics.get("optimized_carbon_score_kgCO2e", "")),
        str(metrics.get("absolute_reduction_kgCO2e", "")),
    ]
    # Ajouter les impacts des recommandations
    for vec in json_payload.get("recom_vectors", []):
        key_values.append(str(vec.get("impact_reduction_kgCO2e", "")))

    key_values = [v for v in key_values if v and v != "0"]
    if not key_values:
        return 0.0

    found = sum(1 for v in key_values if v in generated_text)
    return round(found / len(key_values), 3)


def hallucination_rate(generated_text: str, json_payload: dict) -> dict:
    """
    Détecte les chiffres dans le texte qui n'existent pas dans le payload source.
    """
    authorized = set(re.findall(r'\d+\.?\d*', json.dumps(json_payload)))
    generated = set(re.findall(r'\d+\.?\d*', generated_text))

    # Exclure les chiffres "courants" non significatifs (1, 2, 3... années, etc.)
    common_numbers = {"1", "2", "3", "4", "5", "10", "100", "0"}
    suspicious = generated - authorized - common_numbers

    return {
        "hallucination_rate": round(len(suspicious) / max(len(generated), 1), 3),
        "suspicious_values": sorted(list(suspicious))[:10],
        "total_numbers_generated": len(generated),
    }


def structure_compliance(generated_text: str) -> dict:
    """
    Vérifie que les 3 sections obligatoires sont présentes.
    """
    required_markers = {
        "synthese": "🌱",
        "axe_prioritaire": "🚀",
        "impact_concret": "✅",
    }
    results = {k: marker in generated_text for k, marker in required_markers.items()}
    results["score"] = sum(results.values()) / len(required_markers)
    return results


def compute_rouge_l(hypothesis: str, reference: str) -> float:
    """ROUGE-L : similarité de séquence la plus longue commune."""
    try:
        scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
        result = scorer.score(reference, hypothesis)
        return round(result["rougeL"].fmeasure, 3)
    except ImportError:
        print("⚠️ rouge-score non installé : pip install rouge-score")
        return -1.0


def compute_bert_score(hypothesis: str, reference: str) -> float:
    """BERTScore F1 (similarité sémantique profonde)."""
    try:
       
        P, R, F1 = score([hypothesis], [reference], lang="fr", verbose=False)
        return round(F1.mean().item(), 3)
    except ImportError:
        print("⚠️ bert-score non installé : pip install bert-score")
        return -1.0


# ─── 2. Évaluation complète d'un exemple ────────────────────────────────────

def evaluate_xai_output(
    generated_text: str,
    json_payload: dict,
    reference_text: Optional[str] = None,
) -> dict:
    """
    Évalue une sortie XAI sur tous les critères disponibles.

    Args:
        generated_text: texte généré par le LLM
        json_payload: payload Couche 2 source
        reference_text: texte de référence validé humainement (optionnel)

    Returns:
        dict avec tous les scores
    """
    results = {
        "factual_grounding": factual_grounding_score(generated_text, json_payload),
        "hallucination": hallucination_rate(generated_text, json_payload),
        "structure": structure_compliance(generated_text),
    }

    if reference_text:
        results["rouge_l"] = compute_rouge_l(generated_text, reference_text)
        results["bert_score_f1"] = compute_bert_score(generated_text, reference_text)

    # Score global (moyenne pondérée)
    scores = [
        results["factual_grounding"] * 0.35,
        (1 - results["hallucination"]["hallucination_rate"]) * 0.35,
        results["structure"]["score"] * 0.30,
    ]
    results["global_score"] = round(sum(scores), 3)
    results["quality_label"] = (
        "🟢 Excellent" if results["global_score"] >= 0.85 else
        "🟡 Acceptable" if results["global_score"] >= 0.65 else
        "🔴 À revoir"
    )

    return results


# ─── 3. LLM-as-Judge ─────────────────────────────────────────────────────────

def llm_judge(generated_text: str, json_payload: dict) -> dict:
    """
    Utilise Gemini Flash pour évaluer la sortie XAI automatiquement.
    Retourne des notes sur 5 par critère.
    """
    import google.generativeai as genai

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"error": "GEMINI_API_KEY manquante"}

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

    judge_prompt = f"""
Tu es un évaluateur expert en IA explicable (XAI) et transition carbone.
Évalue l'explication XAI ci-dessous sur 5 critères. Note chaque critère de 1 (très mauvais) à 5 (excellent).

EXPLICATION XAI GÉNÉRÉE :
---
{generated_text}
---

DONNÉES SOURCE (vérité terrain) :
---
{json.dumps(json_payload, indent=2, ensure_ascii=False)}
---

CRITÈRES D'ÉVALUATION :
1. fidelite_factuelle : Tous les chiffres cités correspondent-ils exactement aux données JSON ?
2. clarte_pedagogique : Le texte est-il compréhensible par un non-expert en carbone ?
3. actionabilite : Les actions proposées sont-elles concrètes et réalisables au quotidien ?
4. absence_hallucination : Aucun chiffre ou fait inventé par rapport aux données source ?
5. respect_structure : Les 3 sections (🌱 Synthèse, 🚀 Axe prioritaire, ✅ Impact concret) sont-elles présentes et bien remplies ?

Réponds UNIQUEMENT avec un objet JSON valide, sans markdown, sans backticks :
{{"fidelite_factuelle": X, "clarte_pedagogique": X, "actionabilite": X, "absence_hallucination": X, "respect_structure": X, "commentaire": "..."}}
"""

    try:
        response = model.generate_content(
            judge_prompt,
            generation_config={"temperature": 0.0, "max_output_tokens": 512},
        )
        text = response.text.strip()
        # Nettoyer les éventuels backticks
        text = re.sub(r"```json|```", "", text).strip()
        scores = json.loads(text)
        scores["score_moyen"] = round(
            sum(v for k, v in scores.items() if isinstance(v, (int, float))) / 5, 2
        )
        return scores
    except Exception as e:
        return {"error": str(e), "raw": response.text if "response" in dir() else ""}


# ─── 4. Évaluation en batch sur le dataset ───────────────────────────────────

def evaluate_batch(dataset_path: str, xai_explainer) -> list:
    """
    Évalue le modèle XAI sur l'ensemble du dataset de test.
    Retourne les métriques agrégées.
    """
    results = []
    with open(dataset_path, "r", encoding="utf-8") as f:
        examples = [json.loads(line) for line in f]

    for i, ex in enumerate(examples):
        print(f"[{i+1}/{len(examples)}] Évaluation en cours...")
        payload = json.loads(ex["input"])
        reference = ex.get("output", None)

        generated = xai_explainer.generate(payload)
        text = generated["xai_narrative"]

        metrics = evaluate_xai_output(text, payload, reference)
        metrics["example_id"] = i
        results.append(metrics)

    # Agrégation
    avg_global = sum(r["global_score"] for r in results) / len(results)
    avg_grounding = sum(r["factual_grounding"] for r in results) / len(results)

    print(f"\n📊 RÉSULTATS GLOBAUX ({len(results)} exemples) :")
    print(f"   Score global moyen    : {avg_global:.3f}")
    print(f"   Factual grounding moy : {avg_grounding:.3f}")

    return results


# ─── Test rapide ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sample_payload = {
        "metrics": {
            "initial_carbon_score_kgCO2e": 95.0,
            "optimized_carbon_score_kgCO2e": 63.0,
            "absolute_reduction_kgCO2e": 32.0,
            "relative_reduction_percent": 33.68,
        },
        "recom_vectors": [
            {"dimension": "transport", "action": "Bus", "impact_reduction_kgCO2e": 14.7},
        ],
    }

    sample_generated = """
## 🌱 Synthèse de votre bilan carbone
Votre empreinte carbone mensuelle actuelle est de 95 kg CO₂e.
Elle peut être ramenée à 63 kg CO₂e, soit une réduction de 32 kg CO₂e (−33,68%).

## 🚀 Axe prioritaire : Transport (impact le plus fort)
Substituer vos trajets voiture par le bus permet d'économiser 14.7 kg CO₂e par mois.

## ✅ Impact concret et équivalences
- 🚌 Changer de mode de transport = -14.7 kg CO₂e/mois
- 🌍 Total : -32 kg CO₂e mensuels atteignables grâce à ce plan.
"""

    print("── Métriques automatiques ──")
    metrics = evaluate_xai_output(sample_generated, sample_payload)
    print(json.dumps(metrics, indent=2, ensure_ascii=False))

    print("\n── LLM-as-Judge ──")
    judge_result = llm_judge(sample_generated, sample_payload)
    print(json.dumps(judge_result, indent=2, ensure_ascii=False))
