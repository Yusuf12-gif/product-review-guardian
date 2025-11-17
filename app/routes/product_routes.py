from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas, crud, auth
from ..database import get_db
from ..models import User

router = APIRouter(prefix="/products", tags=["products"])


# ------------------- Create Product -------------------
@router.post("/", response_model=schemas.ProductOut)
async def create_product(
    product_in: schemas.ProductCreate,
    db: AsyncSession = Depends(get_db),
):
    return await crud.create_product(db, product_in)


# ------------------- List Products -------------------
@router.get("/", response_model=List[schemas.ProductOut])
async def list_products(db: AsyncSession = Depends(get_db)):
    return await crud.list_products(db)


# ------------------- Get Product by ID -------------------
@router.get("/{product_id}", response_model=schemas.ProductOut)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# ------------------- Delete Product (Admin Only) -------------------
@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth.get_current_user)
):
    # Only admin can delete products
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete products")

    product = await crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Ensure no reviews exist to avoid foreign key issues
    reviews = await crud.list_reviews_by_product(db, product_id)
    if reviews:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete product with existing reviews"
        )

    await crud.delete_product(db, product)
    return {"detail": "Product deleted successfully!"}
