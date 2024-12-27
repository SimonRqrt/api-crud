from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone
import uuid

# Modèle pour les catégories de produits
class ProductCategory(SQLModel, table=True):
    __tablename__ = "ProductCategory"
    __table_args__ = {"schema": "SalesLT"}  # Schéma utilisé dans la base de données

    ProductCategoryID: int = Field(primary_key=True)
    Name: str = Field(..., max_length=255)
    ParentProductCategoryID: Optional[int] = Field(default=None, foreign_key="SalesLT.ProductCategory.ProductCategoryID")
    rowguid: uuid.UUID = Field(default_factory=uuid.uuid4)
    ModifiedDate: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    Products: List["Product"] = Relationship(back_populates="Category")


# Modèle pour les modèles de produits
class ProductModel(SQLModel, table=True):
    __tablename__ = "ProductModel"
    __table_args__ = {"schema": "SalesLT"}  # Schéma utilisé dans la base de données

    ProductModelID: int = Field(primary_key=True)
    Name: str = Field(..., max_length=255)
    CatalogDescription: Optional[str] = None
    rowguid: uuid.UUID = Field(default_factory=uuid.uuid4)
    ModifiedDate: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    Products: List["Product"] = Relationship(back_populates="Model")


# Modèle de base pour les produits
class ProductBase(SQLModel):
    """
    Modèle de base pour les produits, utilisé lors de la création ou de la mise à jour d'un produit.
    """
    Name: str = Field(..., max_length=255)  
    ProductNumber: str = Field(..., unique=True, max_length=50)  
    Color: Optional[str] = None
    StandardCost: Optional[float] = None
    ListPrice: Optional[float] = None
    Size: Optional[str] = None
    Weight: Optional[float] = None
    ProductCategoryID: Optional[int] = None
    ProductModelID: Optional[int] = None
    SellStartDate: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    SellEndDate: Optional[datetime] = None
    DiscontinuedDate: Optional[datetime] = None
    ThumbnailPhotoFileName: Optional[str] = None
    rowguid: uuid.UUID = Field(default_factory=uuid.uuid4)
    ModifiedDate: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))



# Modèle pour les produits
class Product(ProductBase, table=True):
    """
    Modèle représentant un produit dans la base de données.
    """
    __tablename__ = "Product"
    __table_args__ = {"schema": "SalesLT"}

    ProductID: int = Field(primary_key=True)
    ProductCategoryID: Optional[int] = Field(default=None, foreign_key="SalesLT.ProductCategory.ProductCategoryID")
    ProductModelID: Optional[int] = Field(default=None, foreign_key="SalesLT.ProductModel.ProductModelID")

    Category: Optional[ProductCategory] = Relationship(back_populates="Products")
    Model: Optional[ProductModel] = Relationship(back_populates="Products")


# Modèle pour la création des produits
class ProductCreate(SQLModel):
    """
    Modèle utilisé pour la création de nouveaux produits.
    Exclut les champs générés automatiquement comme ProductID, rowguid, et ModifiedDate.
    """
    Name: str = Field(..., max_length=255)
    ProductNumber: str = Field(..., max_length=50)
    Color: Optional[str] = None
    StandardCost: Optional[float] = None
    ListPrice: float  # Ce champ est requis pour la création
    Size: Optional[str] = None
    Weight: Optional[float] = None
    ProductCategoryID: Optional[int] = None
    ProductModelID: Optional[int] = None
    SellStartDate: datetime = Field(default_factory=datetime)


# Modèle pour la mise à jour des produits
class ProductUpdate(SQLModel):
    """
    Modèle utilisé pour la mise à jour des produits.
    Tous les champs sont optionnels pour permettre des mises à jour partielles.
    """
    Name: Optional[str] = None
    ProductNumber: Optional[str] = None
    Color: Optional[str] = None
    StandardCost: Optional[float] = None
    ListPrice: Optional[float] = None
    Size: Optional[str] = None
    Weight: Optional[float] = None
    ProductCategoryID: Optional[int] = None
    ProductModelID: Optional[int] = None
    SellStartDate: Optional[datetime] = None
    SellEndDate: Optional[datetime] = None
    DiscontinuedDate: Optional[datetime] = None