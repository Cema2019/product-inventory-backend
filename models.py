from sqlalchemy import Column, Integer, String, Float
from db import Base

class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    price = Column(Float)
    delivery = Column(Float)
