import asyncio
from fastapi import FastAPI
from .database import engine, Base
from .routes import auth_routes, review_routes
from .config import settings
 
app = FastAPI(title="Product Review Guardian")
 
# Include routers
app.include_router(auth_routes.router)
app.include_router(review_routes.router)
 
@app.on_event("startup")
async def on_startup():
    # create DB tables - simple approach for demo (use alembic for production migrations)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
 
@app.get("/")
async def root():
    return {"message": "Product Review Guardian API"}