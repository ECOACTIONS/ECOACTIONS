# EcoImpact AI - Backend

## Présentation
EcoImpact AI est une plateforme intelligente de pilotage, d'optimisation et de vulgarisation de l'empreinte environnementale, spécifiquement adaptée au contexte camerounais. Ce backend est propulsé par **FastAPI** pour garantir performance et asynchronisme.

## Organisation de l'Équipe
Le développement du backend est réparti entre deux collaborateurs :
- **Responsable Modules :** En charge de la logique métier (Calculateur GES, Moteur d'optimisation PuLP, Intégration IA Gemini).
- **Responsable Base de Données :** En charge du schéma PostgreSQL, de la persistance des données et de l'intégration ORM (SQLAlchemy).

## Architecture du Projet
Le projet suit une structure modulaire pour une meilleure maintenabilité :
```text
backend/
├── main.py            # Point d'entrée de l'application
├── routes/            # Points d'accès API (Auth, Score, Optimize, Chat)
├── services/          # Logique métier (Calculateur, Optimiseur, LLM)
├── models/            # Définitions des modèles de données
├── database/          # Configuration et connexion à PostgreSQL
└── requirements.txt   # Dépendances Python
```

## Pile Technologique
- **Framework :** FastAPI
- **Optimisation :** PuLP / SciPy (Programmation linéaire)
- **IA :** Google Generative AI (Gemini API)
- **Base de Données :** PostgreSQL via SQLAlchemy
- **Validation :** Pydantic

## Installation et Configuration

### 1. Prérequis
- Python 3.10+
- Un environnement virtuel (recommandé)

### 2. Installation
```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate  # Sur Linux/macOS

# Installer les dépendances
pip install -r backend/requirements.txt
```

### 3. Variables d'Environnement
Créez un fichier `.env` à la racine pour configurer vos clés :
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
GEMINI_API_KEY=votre_cle_api
SECRET_KEY=votre_secret_jwt
```

### 4. Lancement
```bash
# Depuis la racine du projet
export PYTHONPATH=$PYTHONPATH:.
python3 backend/main.py
```
L'API sera accessible sur `http://localhost:8000`. La documentation interactive (Swagger) est disponible sur `/docs`.
