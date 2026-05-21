from fastapi import APIRouter
from sqlalchemy import text

from backend.app.database.db import SessionLocal

router = APIRouter(
    prefix="/api"
)


@router.post("/wishlist/add")
def add_to_wishlist(data: dict):

    db = SessionLocal()

    try:

        db.execute(
            text("""
                INSERT INTO wishlist
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
                "user_id":
                data["user_id"],

                "article_id":
                data["article_id"]
            }
        )

        db.commit()

        return {
            "status":
            "success",
            "message":
            "Added to wishlist"
        }

    finally:
        db.close()


@router.get("/wishlist/{user_id}")
def get_wishlist(user_id: int):

    db = SessionLocal()

    try:

        result = db.execute(
            text("""
                SELECT
                    p.*
                FROM wishlist w
                JOIN products p
                ON w.article_id =
                p.article_id

                WHERE
                w.user_id =
                :user_id
            """),
            {
                "user_id":
                user_id
            }
        )

        products = []

        for row in result:

            product = dict(
                row._mapping
            )

            article_id = str(
                product["article_id"]
            )

            folder = (
                f"0{article_id[:2]}"
            )

            image_name = (
                f"0{article_id}.jpg"
            )

            product["image_url"] = (
                "http://127.0.0.1:8000/"
                f"images/{folder}/"
                f"{image_name}"
            )

            products.append(
                product
            )

        return {
            "status":
            "success",
            "products":
            products
        }

    finally:
        db.close()

@router.delete("/wishlist/remove")
def remove_wishlist_item(
    user_id: int,
    article_id: int
):

    db = SessionLocal()

    try:

        db.execute(
            text("""
                DELETE FROM wishlist
                WHERE user_id = :user_id
                AND article_id = :article_id
            """),
            {
                "user_id":
                user_id,

                "article_id":
                article_id
            }
        )

        db.commit()

        return {
            "status":
            "success",
            "message":
            "Removed from wishlist"
        }

    finally:
        db.close()