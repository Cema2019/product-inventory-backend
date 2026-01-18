from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.sale import Sale


class SaleRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Sale]:
        pass

    @abstractmethod
    def get_by_id(self, sale_id: int) -> Optional[Sale]:
        pass

    @abstractmethod
    def create(self, sale: Sale) -> Sale:
        pass

    @abstractmethod
    def update(self, sale_id: int, sale: Sale) -> Optional[Sale]:
        pass

    @abstractmethod
    def delete(self, sale_id: int) -> bool:
        pass
