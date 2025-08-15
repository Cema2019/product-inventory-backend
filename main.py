import os
import asyncio
from typing import List, Optional
from dotenv import load_dotenv

import aiomysql
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

# --- Database Connection Pool Setup ---
# This section replaces your db.js file. We create a global pool.
async def get_db_pool():
    """
    Creates and returns a database connection pool using credentials
    from the environment variables. This is a best practice for
    asynchronous applications.
    """
    try:
        pool = await aiomysql.create_pool(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            db=os.getenv('DB_NAME'),
            autocommit=True, # Automatically commit changes after each query
            loop=asyncio.get_event_loop(),
            port=3306,
            minsize=1,
            maxsize=10
        )
        print("Database connection pool created successfully.")
        return pool
    except Exception as e:
        print(f"Failed to create database pool: {e}")
        # Re-raise the exception to prevent the application from starting
        raise e

# Create the FastAPI app instance
app = FastAPI()

# --- CORS Middleware ---
# This replaces the `app.use(cors())` from your index.js file.
# It allows your React frontend to communicate with this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allows all headers
)

# --- Pydantic Models for Data Validation ---
# These models define the structure of the data for requests and responses.
# This replaces the manual type-checking you had in Express.
class SaleBase(BaseModel):
    name: str
    price: float
    delivery: float

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    TOTAL: float

    class Config:
        from_attributes = True

# --- Application Startup Event ---
# This is a key FastAPI feature. It ensures the database pool is
# created as soon as the application starts, making it available
# for all endpoints.
@app.on_event("startup")
async def startup_event():
    """
    Called when the application starts up. This is where we
    initialize our database connection pool.
    """
    try:
        app.state.db_pool = await get_db_pool()
    except Exception as e:
        # In case of an error, we print and re-raise to stop the app
        print(f"Application startup failed due to database connection error: {e}")
        raise

# --- API Endpoints (Replicating salesRoutes.js) ---
# This router will handle all endpoints for the /api/sales path.
# We'll include it in the main app at the bottom.
# This is the equivalent of `const router = express.Router()`
from fastapi import APIRouter
router = APIRouter()

@router.get('/')
async def get_all_sales() -> List[Sale]:
    """
    Handles GET /api/sales - Retrieve all sales records.
    """
    async with app.state.db_pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            try:
                # The query is almost identical to your Express.js code.
                await cur.execute('SELECT id, name, price, delivery, price + delivery AS TOTAL FROM sales')
                results = await cur.fetchall()
                # Return the results as a list of Sale objects.
                return [Sale.model_validate(result) for result in results]
            except Exception as e:
                print(f"Error fetching sales: {e}")
                raise HTTPException(status_code=500, detail="Failed to fetch sales")

@router.get('/{sale_id}')
async def get_sale_by_id(sale_id: int) -> Sale:
    """
    Handles GET /api/sales/{id} - Retrieve a sale by ID.
    """
    async with app.state.db_pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            try:
                await cur.execute('SELECT id, name, price, delivery, price + delivery AS TOTAL FROM sales WHERE id = %s', (sale_id,))
                result = await cur.fetchone()
                if not result:
                    # Raises an HTTPException with a 404 status code,
                    # which is what your Express app did with `res.status(404).json`.
                    raise HTTPException(status_code=404, detail="Sale not found")
                return Sale.model_validate(result)
            except Exception as e:
                print(f"Error fetching sale: {e}")
                raise HTTPException(status_code=500, detail="Failed to fetch sale")

@router.post('/')
async def create_sale(sale: SaleCreate) -> Sale:
    """
    Handles POST /api/sales - Create a new sale.
    The `sale: SaleCreate` parameter automatically validates the request body.
    """
    async with app.state.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            try:
                await cur.execute(
                    'INSERT INTO sales (name, price, delivery) VALUES (%s, %s, %s)',
                    (sale.name, sale.price, sale.delivery)
                )
                # `cur.lastrowid` gets the ID of the newly inserted row.
                new_id = cur.lastrowid
                return Sale(
                    id=new_id,
                    name=sale.name,
                    price=sale.price,
                    delivery=sale.delivery,
                    TOTAL=sale.price + sale.delivery
                )
            except Exception as e:
                print(f"Error creating sale: {e}")
                raise HTTPException(status_code=500, detail="Failed to create sale")

@router.put('/{sale_id}')
async def update_sale(sale_id: int, sale: SaleCreate) -> Sale:
    """
    Handles PUT /api/sales/{id} - Update a sale by ID.
    """
    async with app.state.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            try:
                await cur.execute(
                    'UPDATE sales SET name = %s, price = %s, delivery = %s WHERE id = %s',
                    (sale.name, sale.price, sale.delivery, sale_id)
                )
                # `cur.rowcount` is the number of rows affected.
                if cur.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Sale not found")
                return Sale(
                    id=sale_id,
                    name=sale.name,
                    price=sale.price,
                    delivery=sale.delivery,
                    TOTAL=sale.price + sale.delivery
                )
            except Exception as e:
                print(f"Error updating sale: {e}")
                raise HTTPException(status_code=500, detail="Failed to update sale")

@router.delete('/{sale_id}', status_code=204)
async def delete_sale(sale_id: int) -> Response:
    """
    Handles DELETE /api/sales/{id} - Delete a sale by ID.
    Returns a 204 No Content response on success.
    """
    async with app.state.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            try:
                await cur.execute('DELETE FROM sales WHERE id = %s', (sale_id,))
                if cur.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Sale not found")
                # Return a Response with a 204 status code, matching your Express app.
                return Response(status_code=204)
            except Exception as e:
                print(f"Error deleting sale: {e}")
                raise HTTPException(status_code=500, detail="Failed to delete sale")

# Include the sales router into the main application.
# This makes all the endpoints under `router` available at /api/sales.
# This is the equivalent of `app.use('/api/sales', salesRoutes)`
app.include_router(router, prefix="/api/sales")

# --- Root Endpoint (Equivalent to `app.get('/')`) ---
@app.get("/")
async def read_root():
    return {"message": "Sales API is running (FastAPI version)"}

# --- Uvicorn Server Command ---
# To run this file, you would typically use:
# uvicorn main:app --reload
