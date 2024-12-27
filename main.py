from fastapi import FastAPI, Depends, HTTPException, status
from routes import products  # Importer les routes des produits
from models import SQLModel, ProductCategory, Product, ProductModel, ProductCreate
from db import engine, get_session
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import timedelta
from typing import List
from auth.dependencies import create_access_token, authenticate_user, get_current_user

# Initialiser l'application FastAPI
app = FastAPI(
    title="AdventureWorks API",
    description="API CRUD pour gérer les produits AdventureWorks",
    version="1.0.0",
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@app.post("/token", response_model=dict, tags=["Authentification"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    try:
        authenticate_user(form_data.username, form_data.password)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": form_data.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erreur d'authentification",
        )


@app.get("/protected/", response_model=dict, tags=["Produits"])
async def protected_route(current_user: dict = Depends(get_current_user)):

    return {"message": f"Welcome, {current_user['username']}!"}


@app.get("/products/", response_model=List[Product], tags=["Produits"])
async def list_products(
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):

    statement = select(Product)
    results = session.exec(statement).all()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun produit trouvé")
    return results


@app.get("/products/{product_id}", response_model=Product, tags=["Produits"])
async def get_product(
    product_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):

    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produit non trouvé")
    return product


@app.post("/products/", response_model=Product, tags=["Produits"])
async def create_product(
    product: ProductCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):

    if not current_user.get('is_admin', False):  # Vérification si l'utilisateur est admin
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès interdit")
    
    new_product = Product.from_orm(product)
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product


@app.put("/products/{product_id}", response_model=Product, tags=["Produits"])
async def update_product(
    product_id: int,
    product: ProductCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):

    if not current_user.get('is_admin', False):  # Vérification si l'utilisateur est admin
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès interdit")
    
    existing_product = session.get(Product, product_id)
    if not existing_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produit non trouvé")
    
    for key, value in product.dict(exclude_unset=True).items():
        setattr(existing_product, key, value)
    
    session.add(existing_product)
    session.commit()
    session.refresh(existing_product)
    return existing_product


@app.delete("/products/{product_id}", response_model=dict, tags=["Produits"])
async def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):

    if not current_user.get('is_admin', False):  # Vérification si l'utilisateur est admin
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès interdit")
    
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produit non trouvé")
    
    session.delete(product)
    session.commit()
    return {"message": f"Produit {product_id} supprimé avec succès"}
