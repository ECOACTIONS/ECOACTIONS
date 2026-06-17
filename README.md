## Spécifications d'Intégration Front-End / Back-End (pour l'equipe back-end)

Le formulaire de calcul de l'empreinte carbone (`CalculateurPage.tsx`) est entierement modulaire et centralise ses données dans un etat unique. Lors de la soumission finale, l'application exécute un payload JSON pret a etre intercepte par l'API Backend.

### Structure du Payload JSON (POST)

L'API doit exposer un endpoint (ex: `/api/v1/calculate`) capable de receptionner la structure ci dessous :

```json
{
  "transportType": "none",
  "motoTaxiUsage": "modere",
  "climatisation": "oui",
  "factureElectricite": "medium",
  "alimentationType": "mixed",
  "dechetsGestion": "bac"
}

donc le format de reponse attendu en front-end qui a ete configure est :

{
  "status": "success",
  "carbonScore": 2.4,
  "reductionPotential": 30,
  "financialSavingsXAF": 15000,
  "recommendations": [
    "Optimiser les trajets en moto-taxi collectifs",
    "Réguler l'usage du climatiseur pendant les heures de pic"
  ]
}


nb : bien couloir consulter le code contenu dans :'calculateurPage' pour avoir un appercu du referentiel des valeurs acceptes
