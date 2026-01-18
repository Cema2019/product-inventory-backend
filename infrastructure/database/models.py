from sqlalchemy import Column, Float, Integer, String

from infrastructure.database.connection import Base


class SaleModel(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    price = Column(Float)
    delivery = Column(Float)
