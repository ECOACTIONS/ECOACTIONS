from fastapi import FastAPI
from backend.routes import score

app = FastAPI(
    title="EcoImpact AI API",
    description="Plateforme intelligente de pilotage et d'optimisation de l'empreinte environnementale au Cameroun.",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API EcoImpact AI"}

# Inclusion des routes
app.include_router(score.router, prefix="/score", tags=["Score"])
# app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# app.include_router(optimize.router, prefix="/optimize", tags=["Optimization"])
# app.include_router(chat.router, prefix="/chat", tags=["AI Chat"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
