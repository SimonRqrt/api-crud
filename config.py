from pydantic_settings import BaseSettings
from typing import Optional
from sqlalchemy import text
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = "API Authentification"
    secret_key: str  
    algorithm: str = "HS256"  
    access_token_expire_minutes: int = 30  # Durée de validité des tokens

    server_name: str = Field(..., env="SERVER_NAME")
    bdd_name: str = Field(..., env="BDD_NAME")  
    user: str = Field(..., env="USER") 
    mdp: str = Field(..., env="MDP") 
    port: int = Field(default=1433, env="PORT")  # Port utilisé par le serveur

    # Mot de passe hashé pour l'authentification user
    hashed_password: str

    @property
    def database_url(self) -> str:
        return (
            f"mssql+pyodbc://{self.user}:{self.mdp}@{self.server_name}:{self.port}/"
            f"{self.bdd_name}?driver=ODBC+Driver+18+for+SQL+Server"
        ).replace(" ", "+")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

    def validate(self):
        # Vérifie si la clé secrète est présente et valide
        if not self.secret_key:
            raise ValueError("La clé secrète est manquante.")
        
        # Vérifie si les informations pour la base de données sont définies
        if not all([self.server_name, self.bdd_name, self.user, self.mdp]):
            raise ValueError("Certaines informations essentielles pour la bdd manquent dans le .env.")
        
        # Vérifie la configuration du mot de passe
        if not self.hashed_password:
            raise ValueError("Le 'hashed_password' est manquant dans le .env.")


settings = Settings()


settings.validate()