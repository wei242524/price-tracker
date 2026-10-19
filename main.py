from decimal import Decimal
from fastapi import FastAPI
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()




@app.get("/")
def read_root():
    return {"message": "Price Tracker is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}


class ProductCreate(BaseModel):
    url : HttpUrl
    target_price : Decimal = Field(gt = 0)

products : dict[int, dict] = {}
next_id = 1

@app.post("/products", status_code = 201)
def create_product(product: ProductCreate):
    global next_id

    new_product = {
        "id": next_id,
        "url" : product.url,
        "target_price" : product.target_price
    }

    products[next_id] = new_product

    next_id += 1

    return new_product