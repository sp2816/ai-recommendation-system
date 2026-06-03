from fastapi import APIRouter
from sqlalchemy import text

from backend.app.database.db import SessionLocal

router = APIRouter(
    prefix="/api"
)


@router.post("/search/save")
def save_search(
    data: dict
):

    db = SessionLocal()

    try:

        db.execute(
            text("""
                INSERT INTO
                search_history
                (
                    user_id,
                    search_query
                )
                VALUES
                (
                    :user_id,
                    :search_query
                )
            """),
            {
                "user_id":
                data["user_id"],

                "search_query":
                data["search_query"]
            }
        )

        # keep a lightweight interaction record for recommendation signals
        db.execute(
            text("""
                INSERT INTO
                user_interactions
                (
                    user_id,
                    article_id,
                    interaction_type
                )
                VALUES
                (
                    :user_id,
                    NULL,
                    'search'
                )
            """),
            {
                "user_id": data["user_id"]
            }
        )

        db.commit()

        return {
            "status":
            "success"
        }

    finally:
        db.close()


@router.post("/views/save")
def save_view(
    data: dict
):

    db = SessionLocal()

    try:

        product_row = db.execute(
            text("""
                SELECT id
                FROM products
                WHERE article_id = :article_id
            """),
            {
                "article_id": data["article_id"]
            }
        ).fetchone()

        if not product_row:
            return {
                "status": "error",
                "message": "Product not found"
            }

        db.execute(
            text("""
                INSERT INTO view_history
                (
                    user_id,
                    article_id
                )
                VALUES
                (
                    :user_id,
                    :article_id
                )
            """),
            {
                "user_id": data["user_id"],
                "article_id": data["article_id"]
            }
        )

        db.execute(
            text("""
                INSERT INTO user_interactions
                (
                    user_id,
                    article_id,
                    interaction_type
                )
                VALUES
                (
                    :user_id,
                    :article_id,
                    'view'
                )
            """),
            {
                "user_id": data["user_id"],
                "article_id": product_row._mapping["id"]
            }
        )

        db.commit()

        return {
            "status": "success"
        }

    finally:
        db.close()