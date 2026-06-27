from sqlalchemy import text
from backend.app.database.db import engine


def get_product_details(article_ids):

    if not article_ids:
        return []

    placeholders = ", ".join(
        [f":id{i}" for i in range(len(article_ids))]
    )

    query = text(f"""
        SELECT
            article_id,
            product_name,
            product_type_name,
            product_group_name,
            colour_group_name,
            image_url,
            product_url,
            description,
            price
        FROM products
        WHERE article_id IN ({placeholders})
    """)

    params = {
        f"id{i}": str(article_ids[i])
        for i in range(len(article_ids))
    }

    with engine.connect() as conn:

        result = conn.execute(query, params)

        return [
            dict(row._mapping)
            for row in result
        ]