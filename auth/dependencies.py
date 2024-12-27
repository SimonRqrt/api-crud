
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional

load_dotenv()

# Récupére des variables depuis le fichier .env 
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
HASHED_PASSWORD = os.getenv("HASHED_PASSWORD")

# Vérifie la présence des variables d'environnement critiques
if not SECRET_KEY:
    raise ValueError("La variable SECRET_KEY n'est pas définie dans le fichier .env.")
if not HASHED_PASSWORD:
    raise ValueError("La variable HASHED_PASSWORD n'est pas définie dans le fichier .env.")

# Gestion des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dépendance OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Vérifie si le mot de passe est correct
def verify_password(plain_password: str, hashed_password: str) -> bool:

    return pwd_context.verify(plain_password, hashed_password)


# Authentifie un utilisateur
def authenticate_user(username: str, password: str) -> bool:

    if username != "testuser":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nom d'utilisateur incorrect",
        )
    if not verify_password(password, HASHED_PASSWORD):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mot de passe incorrect",
        )
    return True


# Crée un token d'accès
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:

    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Dépendance pour obtenir l'utilisateur actuel
async def get_current_user(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les informations d'identification",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Décodage du token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Vérifie que l'utilisateur est valide
    if username != "testuser":
        raise credentials_exception
    
    return {"username": username}
