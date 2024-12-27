from sqlmodel import create_engine, Session
from config import settings
import logging

# Crée l'engine de connexion à la base de données
engine = create_engine(
    settings.database_url,
    echo=settings.app_name == "API CRUD avec Authentification",  
)

# Configure le logger pour capturer les erreurs éventuelles
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_session():
    """
    Gère la création et la fermeture de la session de base de données.

    Utilise le contexte de gestion de session pour garantir la fermeture correcte
    de la session même en cas d'exception.
    """
    try:
        # Démarrer une session
        with Session(engine) as session:
            yield session
    except Exception as e:
        logger.error(f"Erreur lors de la gestion de la session de base de données : {str(e)}")
        raise  
    finally:
        pass

# Vérification de la connexion à la base de données
def check_database_connection():
    """Vérifie la connexion à la base de données"""
    try:
        with Session(engine) as session:
            # Effectuer une simple requête pour tester la connexion
            session.execute("SELECT 1")
            logger.info("Connexion à la base de données réussie.")
    except Exception as e:
        logger.error(f"Erreur de connexion à la base de données : {str(e)}")
        raise ValueError("Échec de la connexion à la base de données. Vérifiez la configuration.")