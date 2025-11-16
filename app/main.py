import asyncio

from fastapi import FastAPI

from .database import engine, Base
from .routes import auth_routes, product_routes, review_routes

app = FastAPI(title="Product Review Guardian")


@app.on_event("startup")
async def on_startup():
    # Create tables at startup (for demo).
    # In real projects use Alembic migrations.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Routers
app.include_router(auth_routes.router)
app.include_router(product_routes.router)
app.include_router(review_routes.router)


@app.get("/")
async def root():
    return {"message": "Product Review Guardian API is running"}
