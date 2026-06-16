# 🌿 GreenIA — Stack IA Carbone Complète

Pipeline IA en 3 couches pour le calcul, l'optimisation et l'explication de l'empreinte carbone.

```
User Input → [C1 Scoring] → [C2 Optimisation PuLP] → [C3 XAI LLM] → Plan narratif
```

---

## 📁 Structure du projet

```
greenia/
├── couche1/
│   └── scorer.py          # Scoring carbone (facteurs ADEME)
├── couche2/
│   └── optimizer.py       # Optimisation linéaire PuLP
├── couche3/
│   ├── xai_explainer.py   # Génération narrative Gemini
│   ├── finetune.py        # Fine-tuning QLoRA (GPU local)
│   └── evaluator.py       # Métriques XAI + LLM-as-Judge
├── data/
│   └── finetune_dataset.jsonl  # Dataset exemples (à enrichir)
├── tests/
│   └── test_pipeline.py   # Tests unitaires pytest
├── main.py                # Pipeline complet (CLI)
├── api.py                 # API REST FastAPI
├── requirements.txt
└── .env.example
```

---

## ⚡ Installation

```bash
# 1. Cloner / dézipper le projet
cd greenia

# 2. Environnement virtuel
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate          # Windows

# 3. Dépendances
pip install -r requirements.txt

# 4. Configuration
cp .env.example .env
# → Renseigner GEMINI_API_KEY dans .env
```

---

## 🚀 Lancement

### Pipeline complet (CLI)
```bash
python main.py
```

### API REST
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
# → http://localhost:8000/docs
```

### Tests unitaires
```bash
python -m pytest tests/ -v
```

### Fine-tuning (GPU local requis)
```bash
# 1. Enrichir data/finetune_dataset.jsonl (200+ exemples recommandés)
# 2. Lancer l'entraînement
python couche3/finetune.py
# → Modèle sauvegardé dans ./models/greenia-xai-lora/
```

---

## 🖥️ Configuration GPU recommandée

| Composant | Minimum | Recommandé |
|-----------|---------|------------|
| GPU VRAM | 8 GB | 16 GB |
| RAM système | 16 GB | 32 GB |
| Stockage | 20 GB | 50 GB |
| CUDA | 11.8+ | 12.1+ |

---

## 📊 Workflow IA recommandé

```
1. Prompt engineering (few-shot + CoT)    ← commencer ici
         ↓
2. Évaluation automatique (evaluator.py)
         ↓
3. Annoter les cas ratés → dataset JSONL
         ↓
4. Fine-tuning QLoRA (finetune.py)        ← après 200+ exemples
         ↓
5. Re-évaluation + LLM-as-Judge
```

---

## 🔑 Variables d'environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `GEMINI_API_KEY` | Clé API Google Gemini | **Obligatoire** |
| `GEMINI_MODEL` | Modèle LLM à utiliser | `gemini-1.5-flash` |
| `BASE_MODEL` | Modèle base pour fine-tuning | `mistralai/Mistral-7B-Instruct-v0.3` |
| `FINETUNED_MODEL_PATH` | Chemin du modèle fine-tuné | `./models/greenia-xai-lora` |

---

## 📌 Sources ADEME intégrées

- Voiture thermique : **0,218 kg CO₂e/km**
- Bus urbain : **0,080 kg CO₂e/km**
- Électricité France : **0,052 kg CO₂e/kWh**
- Climatisation : **0,078 kg CO₂e/heure** (1,5 kW nominal)
- Viande rouge : **6,8 kg CO₂e/repas**
- Repas végétarien : **0,5 kg CO₂e/repas**
