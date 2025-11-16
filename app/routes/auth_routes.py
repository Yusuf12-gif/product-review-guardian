from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas, crud, auth
from ..database import get_db
from ..config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserOut)
async def register(
    user_in: schemas.UserCreate,
    db: AsyncSession = Depends(get_db),
):
    existing = await crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = auth.get_password_hash(user_in.password)
    user = await crud.create_user(db, user_in.email, hashed)
    return user


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await auth.authenticate_user(
        db,
        form_data.username,  # username = email
        form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = auth.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}
