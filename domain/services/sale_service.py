from typing import List, Optional
from domain.repositories.sale_repository import SaleRepository
from domain.entities.sale import Sale


class SaleService:
    def __init__(self, repository: SaleRepository):
        self.repository = repository

    def get_all_sales(self) -> List[Sale]:
        return self.repository.get_all()

    def get_sale_by_id(self, sale_id: int) -> Optional[Sale]:
        return self.repository.get_by_id(sale_id)

    def create_sale(self, sale: Sale) -> Sale:
        if not sale.name or not sale.name.strip():
            raise ValueError("Name cannot be empty")
        if sale.price < 0:
            raise ValueError("Price cannot be negative")
        if sale.delivery < 0:
            raise ValueError("Delivery cannot be negative")
        return self.repository.create(sale)

    def update_sale(self, sale_id: int, sale: Sale) -> Optional[Sale]:
        if not sale.name or not sale.name.strip():
            raise ValueError("Name cannot be empty")
        if sale.price < 0:
            raise ValueError("Price cannot be negative")
        if sale.delivery < 0:
            raise ValueError("Delivery cannot be negative")
        return self.repository.update(sale_id, sale)

    def delete_sale(self, sale_id: int) -> bool:
        return self.repository.delete(sale_id)
