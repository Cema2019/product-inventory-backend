from typing import List
from fastapi import APIRouter, Depends, HTTPException

from domain.entities.sale import Sale
from domain.services.sale_service import SaleService
from presentation.schemas.sale_schemas import SaleCreate, SaleResponse
from presentation.config.dependencies import get_sale_service


router = APIRouter(prefix="/api/sales", tags=["sales"])


@router.get("", response_model=List[SaleResponse])
def get_all_sales(service: SaleService = Depends(get_sale_service)):
    sales = service.get_all_sales()
    return [
        {
            "id": sale.id,
            "name": sale.name,
            "price": sale.price,
            "delivery": sale.delivery,
            "TOTAL": sale.total
        }
        for sale in sales
    ]


@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(sale_id: int, service: SaleService = Depends(get_sale_service)):
    sale = service.get_sale_by_id(sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return {
        "id": sale.id,
        "name": sale.name,
        "price": sale.price,
        "delivery": sale.delivery,
        "TOTAL": sale.total
    }


@router.post("", response_model=SaleResponse)
def create_sale(sale: SaleCreate, service: SaleService = Depends(get_sale_service)):
    try:
        domain_sale = Sale(name=sale.name, price=sale.price, delivery=sale.delivery)
        created_sale = service.create_sale(domain_sale)
        return {
            "id": created_sale.id,
            "name": created_sale.name,
            "price": created_sale.price,
            "delivery": created_sale.delivery,
            "TOTAL": created_sale.total
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{sale_id}", response_model=SaleResponse)
def update_sale(sale_id: int, sale: SaleCreate, service: SaleService = Depends(get_sale_service)):
    try:
        domain_sale = Sale(name=sale.name, price=sale.price, delivery=sale.delivery)
        updated_sale = service.update_sale(sale_id, domain_sale)
        if not updated_sale:
            raise HTTPException(status_code=404, detail="Sale not found")
        return {
            "id": updated_sale.id,
            "name": updated_sale.name,
            "price": updated_sale.price,
            "delivery": updated_sale.delivery,
            "TOTAL": updated_sale.total
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{sale_id}", status_code=204)
def delete_sale(sale_id: int, service: SaleService = Depends(get_sale_service)):
    deleted = service.delete_sale(sale_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sale not found")
    return
