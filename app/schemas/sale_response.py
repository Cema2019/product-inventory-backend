from pydantic import Field
from app.schemas.sale_base import SaleBase


class SaleResponse(SaleBase):
    id: int
    TOTAL: float = Field(..., alias="TOTAL")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
