from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from typing import List
from models import Product, ProductCreate, ProductUpdate
from config import get_session
from auth.dependencies import get_current_user
import logging

# Création d'un routeur pour les produits
router = APIRouter()

# Configuration du logger
logger = logging.getLogger("uvicorn.error")

# Lister tous les produits
@router.get("/", response_model=List[Product], summary="Lister tous les produits")
def list_products(
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"Utilisateur {current_user} a demandé la liste des produits.")
    products = session.exec(select(Product)).all()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Aucun produit trouvé"
        )
    return products

# Obtenir un produit par ID
@router.get("/{product_id}", response_model=Product, summary="Obtenir un produit par ID")
def get_product(
    product_id: int,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"Utilisateur {current_user} a demandé le produit {product_id}.")
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produit non trouvé"
        )
    return product

# Créer un nouveau produit
@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED, summary="Créer un produit")
def create_product(
    product: ProductCreate,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"Utilisateur {current_user} tente de créer un produit.")
    # Vérification des permissions (admin uniquement)
    if current_user != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Accès interdit"
        )

    # Création du produit
    try:
        new_product = Product.from_orm(product)
        session.add(new_product)
        session.commit()
        session.refresh(new_product)
        logger.info(f"Produit créé avec succès : {new_product}")
        return new_product
    except Exception as e:
        logger.error(f"Erreur lors de la création du produit : {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur lors de la création du produit",
        )

# Mettre à jour un produit
@router.put("/{product_id}", response_model=Product, summary="Mettre à jour un produit")
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"Utilisateur {current_user} tente de mettre à jour le produit {product_id}.")
    # Vérification des permissions (admin uniquement)
    if current_user != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Accès interdit"
        )

    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produit non trouvé"
        )

    updated_data = product_data.dict(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(product, key, value)
    session.commit()
    session.refresh(product)
    logger.info(f"Produit {product_id} mis à jour avec succès.")
    return product

# Supprimer un produit
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Supprimer un produit")
def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    logger.info(f"Utilisateur {current_user} tente de supprimer le produit {product_id}.")
    # Vérification des permissions
    if current_user != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Accès interdit"
        )

    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produit non trouvé"
        )
    session.delete(product)
    session.commit()
    logger.info(f"Produit {product_id} supprimé avec succès.")
    return {"message": f"Produit {product_id} supprimé avec succès"}
