# Product Inventory API - FastAPI Backend

## Overview

This is a FastAPI backend for managing a product inventory, including basic CRUD operations for sales items. It connects to a MySQL database and provides endpoints to create, read, update, and delete products.

## Table of Contents

* [Setup](#setup)
* [Environment Variables](#environment-variables)
* [Database](#database)
* [API Endpoints](#api-endpoints)
* [Running the Server](#running-the-server)
* [CORS Configuration](#cors-configuration)

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd product-inventory-BE
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy the `.env.example` file to `.env` and fill in your configuration:

```bash
cp .env.example .env
```

## Environment Variables

Required variables in `.env`:

```env
DB_HOST=your_database_host_here
DB_USER=your_database_user_here
DB_PASSWORD=your_database_password_here
DB_NAME=your_database_name_here
PORT=your_port_here
```

## Database

The backend uses SQLAlchemy with a MySQL database.

* `db.py` sets up the connection.
* `models.py` defines the `Sale` table.
* Tables are automatically created on server start if they do not exist.

## API Endpoints

### Get all sales

```
GET /api/sales
```

Returns a list of all sales items.

### Get sale by ID

```
GET /api/sales/{sale_id}
```

Returns a single sale by ID.

### Create a sale

```
POST /api/sales
```

Request body:

```json
{
  "name": "Product Name",
  "price": 100.0,
  "delivery": 10.0
}
```

### Update a sale

```
PUT /api/sales/{sale_id}
```

Request body (same as create):

```json
{
  "name": "Updated Name",
  "price": 120.0,
  "delivery": 15.0
}
```

### Delete a sale

```
DELETE /api/sales/{sale_id}
```

Deletes a sale by ID.

## Running the Server

```bash
uvicorn main:app --reload --port 3000
```

Replace `3000` with your configured port in `.env`.

## CORS Configuration

The backend allows requests from the frontend running on `http://localhost:5173`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Adjust `allow_origins` to match your frontend deployment URL.

---

**Note:** Make sure to keep your `.env` file secret and do not commit it to version control.
