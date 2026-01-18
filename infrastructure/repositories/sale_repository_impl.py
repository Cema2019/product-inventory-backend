from typing import List, Optional
from sqlalchemy.orm import Session
from domain.repositories.sale_repository import SaleRepository
from domain.entities.sale import Sale
from infrastructure.database.models import SaleModel


class SaleRepositoryImpl(SaleRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Sale]:
        db_sales = self.db.query(SaleModel).all()
        return [
            Sale(
                id=s.id,
                name=s.name,
                price=s.price,
                delivery=s.delivery
            )
            for s in db_sales
        ]

    def get_by_id(self, sale_id: int) -> Optional[Sale]:
        db_sale = self.db.query(SaleModel).filter(SaleModel.id == sale_id).first()
        if not db_sale:
            return None
        return Sale(
            id=db_sale.id,
            name=db_sale.name,
            price=db_sale.price,
            delivery=db_sale.delivery
        )

    def create(self, sale: Sale) -> Sale:
        db_sale = SaleModel(
            name=sale.name,
            price=sale.price,
            delivery=sale.delivery
        )
        self.db.add(db_sale)
        self.db.commit()
        self.db.refresh(db_sale)
        return Sale(
            id=db_sale.id,
            name=db_sale.name,
            price=db_sale.price,
            delivery=db_sale.delivery
        )

    def update(self, sale_id: int, sale: Sale) -> Optional[Sale]:
        db_sale = self.db.query(SaleModel).filter(SaleModel.id == sale_id).first()
        if not db_sale:
            return None
        db_sale.name = sale.name
        db_sale.price = sale.price
        db_sale.delivery = sale.delivery
        self.db.commit()
        self.db.refresh(db_sale)
        return Sale(
            id=db_sale.id,
            name=db_sale.name,
            price=db_sale.price,
            delivery=db_sale.delivery
        )

    def delete(self, sale_id: int) -> bool:
        db_sale = self.db.query(SaleModel).filter(SaleModel.id == sale_id).first()
        if not db_sale:
            return False
        self.db.delete(db_sale)
        self.db.commit()
        return True
