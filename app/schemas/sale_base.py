from pydantic import BaseModel, Field


class SaleBase(BaseModel):
    name: str = Field(min_length=1)
    price: float
    delivery: float
