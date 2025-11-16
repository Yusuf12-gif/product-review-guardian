from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=schemas.ProductOut)
async def create_product(
    product_in: schemas.ProductCreate,
    db: AsyncSession = Depends(get_db),
):
    return await crud.create_product(db, product_in)


@router.get("/", response_model=List[schemas.ProductOut])
async def list_products(db: AsyncSession = Depends(get_db)):
    return await crud.list_products(db)


@router.get("/{product_id}", response_model=schemas.ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
