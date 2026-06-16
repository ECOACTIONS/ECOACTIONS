from typing import Dict

# Facteurs d'émission (kg CO2e par unité) adaptés au contexte du Cameroun
# Sources estimées selon le Rapport Technique (v2.0)
EMISSION_FACTORS = {
    "energy": {
        "electricity_kwh": 0.35,  # Mix énergétique Cameroun (Réseau Interconnecté Sud)
        "generator_liter": 2.67, # Diesel pour groupe électrogène
        "gas_kg": 2.93           # Gaz domestique (Butane)
    },
    "transport": {
        "motorcycle_km": 0.12,   # Moto-taxi (Benz-skin)
        "shared_taxi_km": 0.08,  # Taxi partagé (en moyenne par passager)
        "private_car_gasoline_km": 0.22,
        "bus_km": 0.05
    },
    "waste": {
        "solid_waste_kg": 0.52   # Gestion informelle/décharges
    }
}

class CarbonCalculator:
    """
    Service de calcul de l'empreinte carbone basé sur les facteurs d'émission locaux.
    """
    
    @staticmethod
    def calculate_energy_impact(electricity_kwh: float = 0, generator_liters: float = 0, gas_kg: float = 0) -> float:
        impact = (electricity_kwh * EMISSION_FACTORS["energy"]["electricity_kwh"]) + \
                 (generator_liters * EMISSION_FACTORS["energy"]["generator_liter"]) + \
                 (gas_kg * EMISSION_FACTORS["energy"]["gas_kg"])
        return round(impact, 2)

    @staticmethod
    def calculate_transport_impact(motorcycle_km: float = 0, shared_taxi_km: float = 0, car_km: float = 0) -> float:
        impact = (motorcycle_km * EMISSION_FACTORS["transport"]["motorcycle_km"]) + \
                 (shared_taxi_km * EMISSION_FACTORS["transport"]["shared_taxi_km"]) + \
                 (car_km * EMISSION_FACTORS["transport"]["private_car_gasoline_km"])
        return round(impact, 2)

    @staticmethod
    def calculate_waste_impact(solid_waste_kg: float = 0) -> float:
        impact = solid_waste_kg * EMISSION_FACTORS["waste"]["solid_waste_kg"]
        return round(impact, 2)

    def calculate_total_assessment(self, data: Dict) -> Dict:
        """
        Calcule l'impact total ventilé par catégorie.
        """
        energy = self.calculate_energy_impact(
            data.get("electricity_kwh", 0),
            data.get("generator_liters", 0),
            data.get("gas_kg", 0)
        )
        transport = self.calculate_transport_impact(
            data.get("motorcycle_km", 0),
            data.get("shared_taxi_km", 0),
            data.get("car_km", 0)
        )
        waste = self.calculate_waste_impact(data.get("solid_waste_kg", 0))
        
        total = energy + transport + waste
        
        return {
            "energy_impact": energy,
            "transport_impact": transport,
            "waste_impact": waste,
            "total_co2": round(total, 2)
        }
