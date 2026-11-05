from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


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
