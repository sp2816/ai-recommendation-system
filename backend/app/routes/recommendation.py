from fastapi import APIRouter
import redis
import json
import os
from collections import Counter

from sqlalchemy import text

from backend.app.database.db import SessionLocal
from ml.src.ann_search import (
    get_recommendations
)

from ml.src.product_lookup import (
    get_product_details
)


router = APIRouter(
    prefix="/recommend",
    tags=["Recommendation"]
)


redis_client = redis.Redis(
    host=os.getenv(
        "REDIS_HOST",
        "redis"
    ),
    port=int(
        os.getenv(
            "REDIS_PORT",
            6379
        )
    ),
    password=os.getenv(
        "REDIS_PASSWORD"
    ),
    db=0,
    decode_responses=True
)


def _build_default_profile(user_id, db):

    # user_id may be a string (external id) or an int (DB id). Try to coerce
    # to int for DB lookups; if coercion fails, treat as missing and return
    # a default cold-start profile.
    try:
        db_user_id = int(user_id)
    except Exception:
        db_user_id = None

    user_row = None
    if db_user_id is not None:
        user_row = db.execute(
            text("""
                SELECT id, age
                FROM users
                WHERE id = :user_id
            """),
            {"user_id": db_user_id}
        ).fetchone()

    age = 25
    if user_row:
        age = user_row._mapping.get("age") or 25

    return {
        "customer_id": str(user_id),
        "favorite_product_type": "Top",
        "interest_categories": ["Top"],
        "season": "Spring",
        "age": float(age),
        "purchase_frequency": 1.0,
        "avg_spend": 0.0,
        "repeat_purchase_ratio": 0.0,
        "source": "default_cold_start",
        "app_user_id": user_id
    }


def _extract_interest_categories(user_id, db):

    category_scores = Counter()

    # Only query view_history/search_history when user_id maps to an integer
    try:
        db_user_id = int(user_id)
    except Exception:
        db_user_id = None

    viewed_types = []
    if db_user_id is not None:
        viewed_types = db.execute(
            text("""
                SELECT p.product_type_name
                FROM view_history vh
                JOIN products p ON vh.product_id = p.id
                WHERE vh.user_id = :user_id
                ORDER BY vh.viewed_at DESC
                LIMIT 25
            """),
            {"user_id": db_user_id}
        ).fetchall()

    for index, row in enumerate(viewed_types):
        product_type = row._mapping.get("product_type_name")
        if product_type:
            category_scores[product_type] += max(1, 5 - min(index, 4))

    searches = []
    if db_user_id is not None:
        searches = db.execute(
            text("""
                SELECT search_query
                FROM search_history
                WHERE user_id = :user_id
                ORDER BY searched_at DESC
                LIMIT 25
            """),
            {"user_id": db_user_id}
        ).fetchall()

    from backend.app.routes.products import CATEGORY_SEARCH_TERMS

    for index, search_row in enumerate(searches):
        query_text = (search_row._mapping.get("search_query") or "").lower()
        search_weight = max(1, 4 - min(index, 3))

        for category, terms in CATEGORY_SEARCH_TERMS.items():
            if any(term in query_text for term in terms):
                category_scores[category] += search_weight
                break

    if not category_scores:
        return ["Top"]

    ranked_categories = [
        category
        for category, _ in category_scores.most_common(4)
    ]

    if "Top" not in ranked_categories:
        ranked_categories.append("Top")

    return ranked_categories


def _apply_recent_activity(user_profile, user_id, db):

    interest_categories = _extract_interest_categories(user_id, db)
    user_profile["interest_categories"] = interest_categories
    user_profile["favorite_product_type"] = interest_categories[0]

    return user_profile


def _build_category_pool(user_profile, db, target_count=10):

    interest_categories = user_profile.get("interest_categories") or [
        user_profile.get("favorite_product_type", "Top")
    ]

    category_slots = {}
    remaining = target_count

    for index, category in enumerate(interest_categories[:3]):
        slots = 4 if index == 0 else 3 if index == 1 else 2
        allocated = min(slots, remaining)
        if allocated <= 0:
            continue
        category_slots[category] = allocated
        remaining -= allocated

    if remaining > 0:
        category_slots["Top"] = category_slots.get("Top", 0) + remaining

    pool = []
    seen_ids = set()

    for category, limit in category_slots.items():
        rows = db.execute(
            text("""
                SELECT article_id
                FROM products
                WHERE product_type_name = :category
                ORDER BY article_id
                LIMIT :limit
            """),
            {
                "category": category,
                "limit": limit * 5
            }
        ).fetchall()

        for row in rows:
            article_id = str(row._mapping["article_id"])
            if article_id in seen_ids:
                continue

            pool.append(article_id)
            seen_ids.add(article_id)

            if len(pool) >= target_count + 20:
                return pool

    return pool


def _diversify_recommendations(recommended_products, interest_categories, target_count=10):

    if not recommended_products:
        return recommended_products

    ordered_categories = []
    for category in interest_categories or []:
        if category and category not in ordered_categories:
            ordered_categories.append(category)

    if "Top" not in ordered_categories:
        ordered_categories.append("Top")

    buckets = {}
    for product in recommended_products:
        category = product.get("product_type_name") or "Other"
        buckets.setdefault(category, []).append(product)

    diversified = []
    used_ids = set()

    primary_limits = {
        category: 3 if index == 0 else 2 if index == 1 else 2
        for index, category in enumerate(ordered_categories[:3])
    }

    for category in ordered_categories:
        limit = primary_limits.get(category, 1)
        bucket = buckets.get(category, [])

        for product in bucket[:limit]:
            article_id = product.get("article_id")
            if article_id in used_ids:
                continue
            diversified.append(product)
            used_ids.add(article_id)

            if len(diversified) >= target_count:
                return diversified[:target_count]

    for product in recommended_products:
        article_id = product.get("article_id")
        if article_id in used_ids:
            continue
        diversified.append(product)
        used_ids.add(article_id)

        if len(diversified) >= target_count:
            break

    return diversified[:target_count]


def _log_recommendation_history(user_id, recommended_products, db):

    if not recommended_products:
        return

    try:
        db_user_id = int(user_id)
    except Exception:
        db_user_id = None

    if db_user_id is None:
        # cannot log without a numeric DB user id
        return

    user_exists = db.execute(
        text("""
            SELECT id
            FROM users
            WHERE id = :user_id
        """),
        {"user_id": db_user_id}
    ).fetchone()

    if not user_exists:
        return

    for product in recommended_products[:10]:
        article_id = product.get("article_id")
        if not article_id:
            continue

        product_row = db.execute(
            text("""
                SELECT id
                FROM products
                WHERE article_id = :article_id
            """),
            {"article_id": article_id}
        ).fetchone()

        if not product_row:
            continue

        db.execute(
            text("""
                INSERT INTO user_interactions
                (
                    user_id,
                    product_id,
                    interaction_type
                )
                VALUES
                (
                    :user_id,
                    :product_id,
                    'recommendation'
                )
            """),
            {
                "user_id": db_user_id,
                "product_id": product_row._mapping["id"]
            }
        )
    db.commit()


@router.get("/{user_id}")
def recommend(
    user_id: str
):

    db = SessionLocal()

    try:
        # Try to fetch a cached user profile from Redis. If Redis is
        # unavailable (e.g. not running locally) fall back to the default
        # cold-start profile so the recommendation endpoint remains usable.
        user_profile = None
        try:
            user_profile = redis_client.get(f"user:{user_id}")
        except Exception:
            user_profile = None

        if user_profile:
            try:
                user_profile = json.loads(user_profile)
            except Exception:
                user_profile = _build_default_profile(user_id, db)
        else:
            user_profile = _build_default_profile(user_id, db)

        user_profile = _apply_recent_activity(user_profile, user_id, db)

        # get a larger candidate set from the ANN search
        recommended_ids = get_recommendations(
            user_profile,
            top_k=20
        )

        # blend in explicit category pools from searches/views so newer intent
        # can mix with the cold-start baseline instead of replacing it outright
        category_pool = _build_category_pool(user_profile, db, target_count=10)
        if category_pool:
            recommended_ids = category_pool + [
                item_id
                for item_id in recommended_ids
                if item_id not in category_pool
            ]

        # Augment candidate pool with items of the user's favorite product type
        try:
            from ml.src import product_lookup
            interest_categories = user_profile.get("interest_categories") or [
                user_profile.get('favorite_product_type')
            ]
            for category in interest_categories[:3]:
                if not category:
                    continue
                fav_candidates = (
                    product_lookup.articles_df[product_lookup.articles_df['product_type_name'] == category]
                    ['article_id']
                    .astype(str)
                    .tolist()
                )
                extra = [i for i in fav_candidates if i not in recommended_ids][:20]
                if extra:
                    recommended_ids = recommended_ids + extra
        except Exception:
            # non-fatal: proceed without augmentation if lookup unavailable
            pass

        recommended_products = (
            get_product_details(
                recommended_ids
            )
        )

        # Simple rerank using metadata: prefer favorite type and season
        n = len(recommended_products)
        if n:
            base_scores = [ (n - i) / n for i in range(n) ]
            interest_categories = user_profile.get('interest_categories') or [
                user_profile.get('favorite_product_type')
            ]
            season = user_profile.get('season')
            fav_boost = 0.45
            secondary_boost = 0.2
            season_boost = 0.4
            for i, p in enumerate(recommended_products):
                type_match = 1.0 if p.get('product_type_name') == interest_categories[0] else 0.0
                secondary_match = 1.0 if p.get('product_type_name') in interest_categories[1:3] else 0.0
                season_match = 1.0 if p.get('season') == season else 0.0
                p['_base_score'] = base_scores[i]
                p['_final_score'] = base_scores[i] + fav_boost * type_match + secondary_boost * secondary_match + season_boost * season_match
            recommended_products = sorted(recommended_products, key=lambda x: x.get('_final_score', 0), reverse=True)

        recommended_products = _diversify_recommendations(
            recommended_products,
            user_profile.get('interest_categories') or [user_profile.get('favorite_product_type')],
            target_count=10
        )

        _log_recommendation_history(user_id, recommended_products, db)
        db.commit()

        return {

            "user_profile":
                user_profile,

            "recommendations":
                recommended_products
        }

    finally:
        db.close()