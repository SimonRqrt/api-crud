# API CRUD

## Présentation

API CRUD est une application RESTful développée avec FastAPI et SQLModel, permettant la gestion des produits issus de la base de données AdventureWorks. Elle intègre un système d'authentification sécurisé basé sur JWT et propose des fonctionnalités complètes de gestion des produits via des opérations CRUD (Create, Read, Update, Delete).

## Fonctionnalités principales

### Gestion des produits (CRUD) :

- Récupération de la liste complète des produits.
- Consultation des détails d'un produit spécifique.
- Ajout d'un nouveau produit.
- Mise à jour des informations d'un produit existant.
- Suppression d'un produit.

### Authentification et sécurité :

- Connexion sécurisée avec authentification par tokens JWT.
- Protection des routes sensibles via un système de rôles (`is_admin`).

### Documentation interactive :

- Accès à la documentation détaillée via [Swagger UI](http://127.0.0.1:8000/docs).

## Prérequis

- **Python** : Version 3.9 ou ultérieure.
- **Base de données SQL Server** : Base AdventureWorks disponible localement ou sur Azure.
- **Outils supplémentaires** :
  - `pip` pour la gestion des dépendances.
  - Postman ou cURL pour tester les API (optionnel).

## Installation

### 1. Cloner le projet :

```sh
git clone https://github.com/votre-repo/api-crud.git
cd api-crud
```

### 2. Configurer l'environnement virtuel :

```sh
python -m venv .venv
source .venv/bin/activate  # Sous Windows : .venv\Scripts\activate
```

### 3. Installer les dépendances :

```sh
pip install -r requirements.txt
```

### 4. Configuration des variables d'environnement :

Créez un fichier `.env` à la racine du projet et renseignez les valeurs suivantes :

```env
USER1_PASSWORD=password123
SECRET_KEY=your_super_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
SERVER_NAME=your-sql-server.database.windows.net
BDD_NAME=your-bdd-name
USER=your-db-user
MDP=your-db-password
```

## Utilisation

### Lancement du serveur :

```sh
python3 -m uvicorn main:app --reload
```

L'API est accessible à l'adresse suivante : [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Documentation Swagger :

Consultez et testez les endpoints via [Swagger UI](http://127.0.0.1:8000/docs).

### Authentification :

#### 1. Récupération d'un token JWT :

**Endpoint** : `POST /auth/login`

**Body (x-www-form-urlencoded)** :

```json
{
    "username": "user1",
    "password": "password123"
}
```

**Réponse** :

```json
{
    "access_token": "your_jwt_token",
    "token_type": "bearer"
}
```

#### 2. Utilisation du token :

Ajoutez un header `Authorization` avec la valeur :

```
Bearer your_jwt_token
```


## Structure du projet

```
api-crud/
│── auth/
│   ├── __init__.py  # Gestion des dépendances d'authentification
│   ├── dependencies.py  # Gestion des tokens JWT
│
│── routes/
│   ├── products.py  # Endpoints liés aux produits
│
│── models.py  # Définition des modèles de données
│── config.py  # Gestion des variables d'environnement
│── main.py  # Point d'entrée de l'application
│── requirements.txt  # Liste des dépendances
│── .env  # Fichier de configuration (non inclus dans le repo)
│── README.md  # Documentation du projet
```

## Tests

Vous pouvez tester les endpoints manuellement à l'aide de Swagger, Postman ou cURL.

---

### 📌 Remarque

Ce projet est en développement actif. N'hésitez pas à contribuer ou à signaler tout problème ! 🚀

