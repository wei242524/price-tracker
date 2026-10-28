from decimal import Decimal

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Price Tracker is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


class ProductCreate(BaseModel):
    url: HttpUrl
    target_price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class ProductUpdate(BaseModel):
    url: HttpUrl | None = None
    target_price: Decimal | None = Field(
        default=None, gt=0, max_digits=10, decimal_places=2
    )


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    url: str
    target_price: Decimal


def get_product_or_404(product_id: int, db: Session) -> models.Product:
    product = db.get(models.Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products", status_code=201, response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(url=str(product.url), target_price=product.target_price)

    db.add(db_product)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="Product with this URL already exists"
        )
    db.refresh(db_product)

    return db_product


@app.get("/products", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.scalars(select(models.Product)).all()


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return get_product_or_404(product_id, db)


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_or_404(product_id, db)
    db.delete(product)
    db.commit()


@app.patch("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)
):
    product = get_product_or_404(product_id, db)
    
    if product_update.url is not None:
        product.url = str(product_update.url)
    if product_update.target_price is not None:
        product.target_price = product_update.target_price

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="Product with this URL already exists"
        )
    db.refresh(product)

    return product
