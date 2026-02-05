from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.sale_create import SaleCreate
from app.schemas.sale_response import SaleResponse
from app.models.sales import Sale
from app.core.db import get_db

router = APIRouter(
    prefix="/sales",
)


@router.get("/", response_model=List[SaleResponse])
def get_all_sales(db: Session = Depends(get_db)):
    sales = db.query(Sale).all()
    return [{"id": s.id, "name": s.name, "price": s.price, "delivery": s.delivery, "TOTAL": s.price + s.delivery} for s in sales]


@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return {"id": sale.id, "name": sale.name, "price": sale.price, "delivery": sale.delivery, "TOTAL": sale.price + sale.delivery}


@router.post("/", response_model=SaleResponse)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    db_sale = Sale(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return {"id": db_sale.id, "name": db_sale.name, "price": db_sale.price, "delivery": db_sale.delivery, "TOTAL": db_sale.price + db_sale.delivery}


@router.put("/{sale_id}", response_model=SaleResponse)
def update_sale(sale_id: int, sale: SaleCreate, db: Session = Depends(get_db)):
    db_sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    for key, value in sale.dict().items():
        setattr(db_sale, key, value)
    db.commit()
    db.refresh(db_sale)
    return {"id": db_sale.id, "name": db_sale.name, "price": db_sale.price, "delivery": db_sale.delivery, "TOTAL": db_sale.price + db_sale.delivery}


@router.delete("/{sale_id}", status_code=204)
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    db.delete(db_sale)
    db.commit()
    return
