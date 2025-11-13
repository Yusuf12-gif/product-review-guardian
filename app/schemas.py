from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: str

    class Config:
        orm_mode = True


class ProductCreate(BaseModel):
    name: str
    category: Optional[str]
    description: Optional[str]


class ProductOut(BaseModel):
    id: int
    name: str
    category: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True


class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    review_text: str = Field(..., min_length=1)


class ReviewCreate(ReviewBase):
    product_id: int


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    review_text: Optional[str]


class ReviewOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    rating: int
    review_text: str
    sentiment_score: Optional[float]
    toxicity_score: Optional[float]
    spam_flag: bool
    ai_summary: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
