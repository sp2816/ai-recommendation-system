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

        db.commit()

        return {
            "status":
            "success"
        }

    finally:
        db.close()