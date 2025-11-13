from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from .database import get_db
from .config import settings
from . import crud, models, auth

# Extract user from JWT and fetch from DB
async def get_current_user(
    token: str = Depends(auth.oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await crud.get_user_by_email(db, email)
    if user is None:
        raise credentials_exception

    return user


# Optional: ensure user is admin
async def get_admin_user(current_user: models.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
