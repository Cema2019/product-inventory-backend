from pydantic import BaseModel, Field

class SaleBase(BaseModel):
    name: str = Field(min_length=1)
    price: float
    delivery: float

class SaleCreate(SaleBase):
    pass

class SaleResponse(SaleBase):
    id: int
    total: float

    class Config:
        orm_mode = True
