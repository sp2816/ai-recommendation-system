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

            article_id = str(product["article_id"])

            folder = f"0{article_id[:2]}"
            image_name = f"0{article_id}.jpg"

            product["image_url"] = (
                "http://127.0.0.1:8000/"
                f"images/{folder}/"
                f"{image_name}"
            )

            products.append(product)

        return {
            "status": "success",
            "count": len(products),
            "products": products
        }

    finally:
        db.close()