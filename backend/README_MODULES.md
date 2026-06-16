# Documentation des Modules - EcoImpact AI

Ce répertoire contient le cœur logique du backend (Module 1, 2 et 3).

## 1. Description des Modules

### Module 1 : Calculateur GES (`services/calculator.py`)
Ce module convertit les activités de l'utilisateur (kWh, Litres, Km) en émissions de CO2.
- **Spécificité :** Facteurs d'émission adaptés au Cameroun (Mix électrique, motos-taxis, groupes électrogènes).
- **Retourne :** Un dictionnaire avec l'impact ventilé par catégorie (énergie, transport, déchets) et le total.

### Module 2 : Moteur d'Optimisation (`services/optimizer.py`)
Utilise la programmation linéaire (**PuLP**) pour trouver les meilleures actions à entreprendre.
- **Logique :** Minimise l'effort global tout en garantissant que l'objectif de réduction (en kg CO2) est atteint.
- **Retourne :** Une liste d'actions recommandées avec leur score d'effort et le gain estimé.

### Module 3 : EcoCoach AI (`services/llm.py`)
Proxy vers l'API Gemini pour transformer les données techniques en conseils motivants.
- **Rôle :** Synthèse pédagogique utilisant des expressions et références locales camerounaises.
- **Prérequis :** Nécessite une clé `GEMINI_API_KEY` dans le fichier `.env`.

## 2. Usage de l'API

### Endpoint : `POST /score/calculate`
**Entrée (JSON) :**
```json
{
  "electricity_kwh": 150,
  "generator_liters": 20,
  "gas_kg": 12.5,
  "motorcycle_km": 100,
  "shared_taxi_km": 200,
  "car_km": 0,
  "solid_waste_kg": 30,
  "target_reduction_pct": 25
}
```

**Sortie (JSON) :**
```json
{
  "assessment": { "total_co2": 186.13, ... },
  "recommendations": [ { "action": "...", "effort": 1, ... } ],
  "ai_summary": "..."
}
```

## 3. Tests d'Intégration
Un script de validation complet est disponible à la racine du backend.
```bash
export PYTHONPATH=$PYTHONPATH:.
source venv/bin/activate
python3 backend/test_integration.py
```
Le test simule un parcours complet et affiche les résultats du calcul, de l'optimisation et la réponse de l'IA (si configurée).
