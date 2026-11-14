from decimal import Decimal
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, HttpUrl

from app.scrapers import SUPPORTED_HOSTS


def check_supported_host(url: HttpUrl) -> HttpUrl:
    if url.host not in SUPPORTED_HOSTS:
        raise ValueError(f"Unsupported website: {url.host}")

    return url


SupportedUrl = Annotated[HttpUrl, AfterValidator(check_supported_host)]


class ProductCreate(BaseModel):
    url: SupportedUrl
    target_price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class ProductUpdate(BaseModel):
    url: SupportedUrl | None = None
    target_price: Decimal | None = Field(
        default=None, gt=0, max_digits=10, decimal_places=2
    )


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    url: str
    target_price: Decimal
