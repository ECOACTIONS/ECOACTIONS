from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from ..database.postgres import get_db
from ..models.user import User
import hashlib

router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Vérifier si l'utilisateur existe déjà
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="Un utilisateur avec cet email existe déjà"
        )
    
    # Hash du mot de passe (simple pour le MVP - à remplacer par bcrypt en prod)
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    
    db_user = User(email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return {"message": "Utilisateur créé avec succès", "user_id": db_user.id}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or hashlib.sha256(form_data.password.encode()).hexdigest() != user.password_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Pour le MVP : token simplifié (à remplacer par JWT réel)
    return {"access_token": f"fake-jwt-{user.id}", "token_type": "bearer"}