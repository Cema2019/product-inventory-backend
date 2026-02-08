from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.db import engine, Base
from app.routes.sales import router as sales_router

# Import models so SQLAlchemy registers them
from app.models.sales import Sale  # <-- important

# Create tables (dev-only)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Inventory API - FastAPI Version")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sales_router, prefix="/api")
