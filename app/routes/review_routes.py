from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas, crud, auth
from ..database import get_db
from ..ai.ai_service import analyze_review_text
from ..models import User

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("/", response_model=schemas.ReviewOut)
async def create_review(
    review_in: schemas.ReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth.get_current_user),
):
    ai_meta = await analyze_review_text(review_in.review_text)
    review = await crud.create_review(db, current_user.id, review_in)
    updated = await crud.update_review(db, review, ai_meta)
    return updated


@router.get("/", response_model=List[schemas.ReviewOut])
async def list_reviews(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    return await crud.list_reviews(db, skip=skip, limit=limit)


@router.get("/{review_id}", response_model=schemas.ReviewOut)
async def get_review(review_id: int, db: AsyncSession = Depends(get_db)):
    review = await crud.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.put("/{review_id}", response_model=schemas.ReviewOut)
async def replace_review(
    review_id: int,
    review_in: schemas.ReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth.get_current_user),
):
    review = await crud.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if review.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not permitted")

    ai_meta = await analyze_review_text(review_in.review_text)
    changes = review_in.model_dump()
    changes.update(ai_meta)

    updated = await crud.update_review(db, review, changes)
    return updated


@router.patch("/{review_id}", response_model=schemas.ReviewOut)
async def patch_review(
    review_id: int,
    review_in: schemas.ReviewUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth.get_current_user),
):
    review = await crud.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if review.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not permitted")

    changes = review_in.model_dump(exclude_unset=True)

    if "review_text" in changes:
        ai_meta = await analyze_review_text(changes["review_text"])
        changes.update(ai_meta)

    updated = await crud.update_review(db, review, changes)
    return updated


@router.delete("/{review_id}")
async def delete_review(
    review_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth.get_current_user),
):
    review = await crud.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if review.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not permitted")

    await crud.delete_review(db, review)
    return {"detail": "Deleted"}
