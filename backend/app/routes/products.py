from fastapi import APIRouter
from sqlalchemy import text

from backend.app.database.db import SessionLocal

router = APIRouter()

@router.get("/products")
def get_products(limit: int = 20):

    db = SessionLocal()

    try:
        query = text("""
            SELECT *
            FROM products
            LIMIT :limit
        """)

        result = db.execute(
            query,
            {"limit": limit}
        )

        products = []

        for row in result:
            products.append(dict(row._mapping))

        return {
            "status": "success",
            "count": len(products),
            "products": products
        }

    finally:
        db.close()