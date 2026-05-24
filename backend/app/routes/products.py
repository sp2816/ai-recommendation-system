from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from backend.app.database.db import SessionLocal

router = APIRouter()


CATEGORY_SEARCH_TERMS = {
    "Dress": ["dress"],
    "Top": ["top", "blouse", "shirt", "sweater", "cardigan", "t-shirt"],
    "Trousers": ["trousers", "jeans", "leggings", "shorts", "pants"],
    "Shoes": ["shoes", "boot", "sneaker", "sandal", "heel", "loafer", "flat"],
    "Nightwear": ["nightwear", "sleep", "pyjama", "pajama", "robe", "underwear", "lingerie"]
}


def build_category_clause(category: str):

    terms = CATEGORY_SEARCH_TERMS.get(
        category,
        [category.lower()]
    )

    clauses = []
    params = {}

    for index, term in enumerate(terms):

        param_name = f"category_term_{index}"

        clauses.append(
            "(" \
            "LOWER(product_name) LIKE :{0} OR " \
            "LOWER(product_type_name) LIKE :{0} OR " \
            "LOWER(product_group_name) LIKE :{0} OR " \
            "LOWER(description) LIKE :{0}" \
            ")".format(param_name)
        )

        params[param_name] = f"%{term}%"

    return "(" + " OR ".join(clauses) + ")", params


@router.get("/products")
def get_products(limit: int = 1000, category: str | None = None):

    db = SessionLocal()

    try:
        article_folder_clause = (
            "("
            "CAST(article_id AS TEXT) LIKE '10%' OR "
            "CAST(article_id AS TEXT) LIKE '11%' OR "
            "CAST(article_id AS TEXT) LIKE '12%' OR "
            "CAST(article_id AS TEXT) LIKE '13%' OR "
            "CAST(article_id AS TEXT) LIKE '14%'"
            ")"
        )

        where_clauses = [
            article_folder_clause
        ]

        query_params = {
            "limit": limit
        }

        if category:

            category_clause, category_params = build_category_clause(
                category
            )

            where_clauses.append(
                category_clause
            )

            query_params.update(
                category_params
            )

        else:

            where_clauses.extend([
                "LOWER(product_type_name) NOT LIKE '%bra%'",
                "LOWER(product_type_name) NOT LIKE '%stocking%'",
                "LOWER(product_type_name) NOT LIKE '%underwear%'",
                "LOWER(product_type_name) NOT LIKE '%tights%'",
                "LOWER(product_type_name) NOT LIKE '%leggings%'",
                "LOWER(product_type_name) NOT LIKE '%sock%'"
            ])

        query = text(f"""
            SELECT
                article_id,
                product_name,
                product_type_name,
                product_group_name,
                colour_group_name,
                price,
                description
            FROM products

            WHERE
                {' AND '.join(where_clauses)}

            ORDER BY article_id

            LIMIT :limit
        """)

        result = db.execute(
            query,
            query_params
        )

        products = []

        for row in result:

            product = dict(
                row._mapping
            )

            article_id = str(
                product["article_id"]
            )

            # Example:
            # 108775015 -> 010
            # 110065001 -> 011
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

            products.append(product)

        return {
            "status": "success",
            "count": len(products),
            "products": products
        }

    finally:
        db.close()

@router.get("/products/search")
def search_products(
    query: str
):

    db = SessionLocal()

    try:

        result = db.execute(
            text("""
                SELECT
                    article_id,
                    product_name,
                    product_type_name,
                    product_group_name,
                    colour_group_name,
                    price,
                    description

                FROM products

                WHERE

                LOWER(product_name)
                LIKE LOWER(:query)

                OR LOWER(product_type_name)
                LIKE LOWER(:query)

                OR LOWER(description)
                LIKE LOWER(:query)

                LIMIT 20
            """),
            {
                "query":
                f"%{query}%"
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


@router.get("/products/trending")
def get_trending_products(category: str | None = None):

    db = SessionLocal()

    try:

        where_clauses = []
        query_params = {}

        if category:

            category_clause, category_params = build_category_clause(
                category
            )

            where_clauses.append(
                category_clause
            )

            query_params.update(
                category_params
            )

        else:

            where_clauses.append(
                "LOWER(product_type_name) NOT LIKE '%bra%'"
            )

        query = text(f"""
            SELECT
                article_id,
                product_name,
                product_type_name,
                product_group_name,
                colour_group_name,
                price,
                description

            FROM products

            WHERE
                {' AND '.join(where_clauses)}

            LIMIT 8
        """)

        result = db.execute(
            query,
            query_params
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

@router.get("/product/{article_id}")
def get_product(article_id: int):

    db = SessionLocal()

    try:
        query = text("""
            SELECT *
            FROM products
            WHERE article_id = :article_id
        """)

        result = db.execute(
            query,
            {
                "article_id":
                article_id
            }
        )

        product = result.fetchone()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        product = dict(
            product._mapping
        )

        article_id_str = str(
            product["article_id"]
        )

        folder = (
            f"0{article_id_str[:2]}"
        )

        image_name = (
            f"0{article_id_str}.jpg"
        )

        product["image_url"] = (
            "http://127.0.0.1:8000/"
            f"images/{folder}/"
            f"{image_name}"
        )

        return {
            "status": "success",
            "product": product
        }

    finally:
        db.close()