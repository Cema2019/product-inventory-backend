from fastapi import Depends
from sqlalchemy.orm import Session

from infrastructure.database.connection import get_db
from infrastructure.repositories.sale_repository_impl import SaleRepositoryImpl
from domain.services.sale_service import SaleService


def get_sale_service(db: Session = Depends(get_db)) -> SaleService:
    repository = SaleRepositoryImpl(db)
    return SaleService(repository)
