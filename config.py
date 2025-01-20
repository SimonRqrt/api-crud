from pydantic_settings import BaseSettings
from typing import Optional
from sqlmodel import SQLModel
from pydantic import Field
from sqlmodel import create_engine, Session

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    USERNAME: str
    PASSWORD: str
    DB_URL: str


    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()

# Crée l'engine de connexion à la base de données
engine = create_engine(
    settings.DB_URL,
    echo=True  
)


def get_session():
        # Démarrer une session
    with Session(engine) as session:
        yield session

