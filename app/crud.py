from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from . import models, schemas


# ---------- User CRUD ----------

async def create_user(db: AsyncSession, email: str, hashed_password: str) -> models.User:
    user = models.User(email=email, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalars().first()


# ---------- Product CRUD ----------

async def create_product(db: AsyncSession, product_in: schemas.ProductCreate):
    product = models.Product(**product_in.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def list_products(db: AsyncSession):
    result = await db.execute(select(models.Product))
    return result.scalars().all()


async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(models.Product).where(models.Product.id == product_id)
    )
    return result.scalars().first()


# ---------- Review CRUD ----------

async def create_review(
    db: AsyncSession, user_id: int, review_in: schemas.ReviewCreate
):
    review = models.Review(
        user_id=user_id,
        **review_in.model_dump(),
    )
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review


async def get_review(db: AsyncSession, review_id: int):
    result = await db.execute(
        select(models.Review).where(models.Review.id == review_id)
    )
    return result.scalars().first()


async def list_reviews(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.Review).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def update_review(
    db: AsyncSession, review: models.Review, changes: dict
):
    for key, value in changes.items():
        setattr(review, key, value)
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review


async def delete_review(db: AsyncSession, review: models.Review):
    await db.delete(review)
    await db.commit()
    return True

async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(models.Product).where(models.Product.id == product_id)
    )
    return result.scalar_one_or_none()


async def list_reviews_by_product(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(models.Review).where(models.Review.product_id == product_id)
    )
    return result.scalars().all()


async def delete_product(db: AsyncSession, product: models.Product):
    await db.delete(product)
    await db.commit()

