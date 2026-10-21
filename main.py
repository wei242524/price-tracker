from decimal import Decimal
from fastapi import FastAPI , HTTPException
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Price Tracker is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


class ProductCreate(BaseModel):
    url: HttpUrl
    target_price: Decimal = Field(gt=0)


class ProductUpdate(BaseModel):
    url: HttpUrl | None = None
    target_price: Decimal | None = None


products: dict[int, dict] = {}
next_id = 1


@app.post("/products", status_code=201)
def create_product(product: ProductCreate):
    global next_id

    new_product = {
        "id": next_id,
        "url": str(product.url),
        "target_price": product.target_price
    }

    products[next_id] = new_product

    next_id += 1

    return new_product

@app.get("/products")
def get_products():
    return list(products.values())


@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products[product_id]

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    del products[product_id]
    return None


@app.patch("/products/{product_id}")
def update_product(product_id: int, product_update: ProductUpdate):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    product = products[product_id]

    if product_update.url is not None:
        product["url"] = str(product_update.url)
    if product_update.target_price is not None:
        product["target_price"] = product_update.target_price

    return product