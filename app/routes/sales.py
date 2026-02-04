from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import schemas
from app.models import models

from app.main import get_db

router = APIRouter(
    prefix="/sales",
    tags=["sales"],
)


@router.get("/api/sales", response_model=List[schemas.SaleResponse])
def get_all_sales(db: Session = Depends(get_db)):
    sales = db.query(models.Sale).all()
    return [{"id": s.id, "name": s.name, "price": s.price, "delivery": s.delivery, "TOTAL": s.price + s.delivery} for s in sales]


@router.get("/api/sales/{sale_id}", response_model=schemas.SaleResponse)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return {"id": sale.id, "name": sale.name, "price": sale.price, "delivery": sale.delivery, "TOTAL": sale.price + sale.delivery}


@router.post("/api/sales", response_model=schemas.SaleResponse)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    db_sale = models.Sale(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return {"id": db_sale.id, "name": db_sale.name, "price": db_sale.price, "delivery": db_sale.delivery, "TOTAL": db_sale.price + db_sale.delivery}


@router.put("/api/sales/{sale_id}", response_model=schemas.SaleResponse)
def update_sale(sale_id: int, sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    db_sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    for key, value in sale.dict().items():
        setattr(db_sale, key, value)
    db.commit()
    db.refresh(db_sale)
    return {"id": db_sale.id, "name": db_sale.name, "price": db_sale.price, "delivery": db_sale.delivery, "TOTAL": db_sale.price + db_sale.delivery}


@router.delete("/api/sales/{sale_id}", status_code=204)
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    db.delete(db_sale)
    db.commit()
    return
