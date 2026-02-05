from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.db import SessionLocal, engine
from app.routes.sales import router as sales_router
import models

# Create tables (if they don’t exist)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Inventory API - FastAPI Version")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(sales_router, prefix="/api")
