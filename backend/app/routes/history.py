from fastapi import APIRouter
from sqlalchemy import text

from backend.app.database.db import SessionLocal

router = APIRouter(prefix="/api")


@router.get("/history/recommendations/{user_id}")
def get_recommendation_history(user_id: int):

    db = SessionLocal()

    try:

        result = db.execute(
            text("""
                SELECT
                    p.article_id,
                    p.product_name,
                    p.product_type_name,
                    p.product_group_name,
                    p.colour_group_name,
                    p.price,
                    p.description,
                    p.image_url,
                    p.product_url,
                    ui.created_at
                FROM user_interactions ui
                JOIN products p
                    ON ui.product_id = p.id
                WHERE ui.user_id = :user_id
                AND ui.interaction_type = 'recommendation'
                ORDER BY ui.created_at DESC
                LIMIT 50
            """),
            {"user_id": user_id}
        )

        products = []

        for row in result:

            product = dict(row._mapping)

            products.append(product)

        return {
            "status": "success",
            "count": len(products),
            "products": products
        }

    finally:
        db.close()