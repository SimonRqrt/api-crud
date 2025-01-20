import os
import logging
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
from config import settings

load_dotenv()

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

logger = logging.getLogger("auth")

users_db = {
    settings.USERNAME: {
        "username": settings.USERNAME,
        "hashed_password": pwd_context.hash(settings.PASSWORD)
    }
}

# Crée un token d'accès
def create_access_token(data: dict):

    to_encode = data.copy()
    expire = datetime.utcnow() + (timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise JWTError
        logger.info("Token décodé avec succès.")
        return username
    except JWTError:
        logger.warning("Échec du décodage du token.")
        return None

# Dépendance pour obtenir l'utilisateur actuel
def get_current_user(token: str = Depends(oauth2_scheme)):
    username = decode_token(token)
    if username is None:
        logger.warning("Pas d'authentification de l'utilisateur.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": username}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user["hashed_password"]):
        logger.warning("Tentative de connexion échouée pour l'utilisateur : %s", form_data.username)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password"
        )
    access_token = create_access_token(data={"sub": user["username"]})
    logger.info("Connexion réussie pour l'utilisateur : %s", user["username"])
    return {"access_token": access_token, "token_type": "bearer"}
