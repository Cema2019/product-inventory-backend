from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.database.connection import Base, engine
from presentation.routes import sales

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Inventory API - Clean Architecture")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sales.router)
