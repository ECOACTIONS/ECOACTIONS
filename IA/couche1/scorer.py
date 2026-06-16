"""
COUCHE 1 — Collecte & Scoring Carbone
Calcule le score CO2e initial à partir des habitudes de vie de l'utilisateur.
Facteurs d'émission : Base Empreinte ADEME.
"""

from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime, timezone


# ─── Modèles de données utilisateur ──────────────────────────────────────────

class TransportData(BaseModel):
    km_voiture_par_semaine: float = Field(0.0, ge=0, description="km/semaine en voiture thermique")
    km_bus_par_semaine: float = Field(0.0, ge=0, description="km/semaine en bus")
    km_velo_par_semaine: float = Field(0.0, ge=0, description="km/semaine en vélo/marche")
    km_train_par_semaine: float = Field(0.0, ge=0, description="km/semaine en train")
    vols_court_courrier_par_an: int = Field(0, ge=0, description="Nombre de vols <3h/an")
    vols_long_courrier_par_an: int = Field(0, ge=0, description="Nombre de vols >3h/an")


class EnergyData(BaseModel):
    heures_clim_par_jour: float = Field(0.0, ge=0, le=24, description="Heures de clim/jour")
    kwh_electricite_par_mois: float = Field(0.0, ge=0, description="kWh électricité/mois")
    kwh_gaz_par_mois: float = Field(0.0, ge=0, description="kWh gaz/mois")


class AlimentationData(BaseModel):
    repas_viande_rouge_par_semaine: int = Field(0, ge=0, le=21)
    repas_viande_blanche_par_semaine: int = Field(0, ge=0, le=21)
    repas_poisson_par_semaine: int = Field(0, ge=0, le=21)
    repas_vegetarien_par_semaine: int = Field(0, ge=0, le=21)


class UserInput(BaseModel):
    transport: TransportData
    energie: EnergyData
    alimentation: AlimentationData


# ─── Facteurs d'émission ADEME ────────────────────────────────────────────────

FACTEURS_ADEME = {
    # Transport (kgCO2e/km)
    "voiture_thermique": 0.218,
    "bus_urbain": 0.080,
    "velo_marche": 0.000,
    "train": 0.004,
    "vol_court_courrier": 230.0,   # kgCO2e/vol (aller simple moyen)
    "vol_long_courrier": 1100.0,   # kgCO2e/vol (aller simple moyen)

    # Énergie (kgCO2e/unité)
    "electricite_kwh": 0.052,      # Mix réseau France
    "gaz_kwh": 0.227,
    "clim_heure": 0.078,           # 1.5 kW × 0.052 kgCO2e/kWh

    # Alimentation (kgCO2e/repas)
    "viande_rouge": 6.8,
    "viande_blanche": 1.5,
    "poisson": 1.2,
    "vegetarien": 0.5,
}

# Semaines par mois pour normalisation mensuelle
SEMAINES_PAR_MOIS = 4.33
JOURS_PAR_MOIS = 30.44


class CarbonScorer:
    """Calcule le score carbone mensuel (kgCO2e) à partir des habitudes utilisateur."""

    def __init__(self):
        self.facteurs = FACTEURS_ADEME

    def score_transport(self, data: TransportData) -> dict:
        f = self.facteurs
        scores = {
            "voiture": data.km_voiture_par_semaine * SEMAINES_PAR_MOIS * f["voiture_thermique"],
            "bus": data.km_bus_par_semaine * SEMAINES_PAR_MOIS * f["bus_urbain"],
            "velo": data.km_velo_par_semaine * SEMAINES_PAR_MOIS * f["velo_marche"],
            "train": data.km_train_par_semaine * SEMAINES_PAR_MOIS * f["train"],
            "vols_court": (data.vols_court_courrier_par_an / 12) * f["vol_court_courrier"],
            "vols_long": (data.vols_long_courrier_par_an / 12) * f["vol_long_courrier"],
        }
        scores["total"] = sum(scores.values())
        return scores

    def score_energie(self, data: EnergyData) -> dict:
        f = self.facteurs
        scores = {
            "clim": data.heures_clim_par_jour * JOURS_PAR_MOIS * f["clim_heure"],
            "electricite": data.kwh_electricite_par_mois * f["electricite_kwh"],
            "gaz": data.kwh_gaz_par_mois * f["gaz_kwh"],
        }
        scores["total"] = sum(scores.values())
        return scores

    def score_alimentation(self, data: AlimentationData) -> dict:
        f = self.facteurs
        scores = {
            "viande_rouge": data.repas_viande_rouge_par_semaine * SEMAINES_PAR_MOIS * f["viande_rouge"],
            "viande_blanche": data.repas_viande_blanche_par_semaine * SEMAINES_PAR_MOIS * f["viande_blanche"],
            "poisson": data.repas_poisson_par_semaine * SEMAINES_PAR_MOIS * f["poisson"],
            "vegetarien": data.repas_vegetarien_par_semaine * SEMAINES_PAR_MOIS * f["vegetarien"],
        }
        scores["total"] = sum(scores.values())
        return scores

    def compute(self, user_input: UserInput) -> dict:
        """Retourne le payload complet pour la Couche 2."""
        t = self.score_transport(user_input.transport)
        e = self.score_energie(user_input.energie)
        a = self.score_alimentation(user_input.alimentation)

        total = t["total"] + e["total"] + a["total"]

        return {
            "metadata": {
                "user_id": f"usr_{uuid.uuid4().hex[:8]}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            "initial_score": {
                "total_kgCO2e": round(total, 2),
                "transport_kgCO2e": round(t["total"], 2),
                "energie_kgCO2e": round(e["total"], 2),
                "alimentation_kgCO2e": round(a["total"], 2),
                "detail": {
                    "transport": {k: round(v, 2) for k, v in t.items() if k != "total"},
                    "energie": {k: round(v, 2) for k, v in e.items() if k != "total"},
                    "alimentation": {k: round(v, 2) for k, v in a.items() if k != "total"},
                },
            },
            "raw_input": user_input.model_dump(),
        }


# ─── Test rapide ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import json

    sample = UserInput(
        transport=TransportData(
            km_voiture_par_semaine=70,
            km_bus_par_semaine=10,
            vols_court_courrier_par_an=2,
        ),
        energie=EnergyData(
            heures_clim_par_jour=4,
            kwh_electricite_par_mois=200,
            kwh_gaz_par_mois=50,
        ),
        alimentation=AlimentationData(
            repas_viande_rouge_par_semaine=4,
            repas_viande_blanche_par_semaine=3,
            repas_vegetarien_par_semaine=7,
        ),
    )

    scorer = CarbonScorer()
    result = scorer.compute(sample)
    print(json.dumps(result, indent=2, ensure_ascii=False))
