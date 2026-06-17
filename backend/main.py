// a mettre a jour dans main.py

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(optimize.router, prefix="/optimize", tags=["Optimization"])
app.include_router(chat.router, prefix="/chat", tags=["AI Chat"])