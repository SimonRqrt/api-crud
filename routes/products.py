from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from typing import List
from models import Product, ProductCreate, ProductUpdate
from db import get_session
from models import Product, ProductCreate
from auth.dependencies import get_current_user
import logging

# Création d'un routeur pour les produits
router = APIRouter()

# Lister tous les produits
@router.get("/products", response_model=List[Product])
def get_products(session: Session = Depends(get_session), 
    user=Depends(get_current_user)
    ):
    """
    Retourne la liste de tous les produits.
    """
    products = session.exec(select(Product)).all()
    return products

# Obtenir un produit par son ID
@router.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, session: Session = Depends(get_session)):
    """
    Retourne un produit spécifique par son ID.
    """
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return product


logger = logging.getLogger("uvicorn.error")

@router.post("/", response_model=Product, summary="Créer un produit")
async def create_product(
    product: ProductCreate, 
    session: Session = Depends(get_session), 
    user=Depends(get_current_user)
):
    try:
        # Vérife si l'utilisateur a les droits nécessaires
        if not user or not user.get('is_admin', False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous n'avez pas les droits pour créer un produit"
            )

        # Création d'un nouveau produit dans la base de données
        new_product = Product.from_orm(product)
        session.add(new_product)
        session.commit()
        session.refresh(new_product)

        return new_product
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création du produit : {str(e)}"
        )

@router.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product_data: ProductUpdate, session: Session = Depends(get_session)):
    """
    Met à jour un produit existant par son ID.
    """
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    
    product_data = product_data.dict(exclude_unset=True)  # Exclure les champs non renseignés
    for key, value in product_data.items():
        setattr(product, key, value)  # Mettre à jour les champs spécifiés
    session.commit()
    session.refresh(product)
    return product


# Supprimer un produit
@router.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, session: Session = Depends(get_session)):
    """
    Supprime un produit par son ID.
    """
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    session.delete(product)
    session.commit()
    return {"detail": "Produit supprimé"}
