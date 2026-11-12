from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.schemas import ProductCreate, ProductResponse, ProductUpdate

app = FastAPI()

DbSession = Annotated[Session, Depends(get_db)]


@app.get("/")
def read_root():
    return {"message": "Price Tracker is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


def get_product_or_404(product_id: int, db: Session) -> models.Product:
    product = db.get(models.Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products", status_code=201, response_model=ProductResponse)
def create_product(product: ProductCreate, db: DbSession):
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
def get_products(  db: DbSession  ):
    return db.scalars(select(models.Product)).all()


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: DbSession):
    return get_product_or_404(product_id, db)


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: DbSession):
    product = get_product_or_404(product_id, db)
    db.delete(product)
    db.commit()


@app.patch("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_update: ProductUpdate, db: DbSession):
    product = get_product_or_404(product_id, db)
    update_data = product_update.model_dump(exclude_unset=True)

    if None in update_data.values():
        raise HTTPException(status_code=422, detail="Null values are not allowed")
    if "url" in update_data:
        update_data["url"] = str(update_data["url"])

    for field, value in update_data.items():
        setattr(product, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="Product with this URL already exists"
        )
    db.refresh(product)

    return product
