from sqlalchemy import text
import json

import redis

from backend.app.database.db import SessionLocal
from backend.app.utils.hash import (
    hash_password,
    verify_password
)
from backend.app.utils.token import (
    create_access_token
)


redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)


def _upsert_recommendation_profile(user_dict):

    profile = {
        "customer_id": str(user_dict["id"]),
        "favorite_product_type": "Top",
        "season": "Spring",
        "age": float(user_dict.get("age") or 25),
        "purchase_frequency": 1.0,
        "avg_spend": 0.0,
        "repeat_purchase_ratio": 0.0,
        "source": "auth_user",
        "app_user_id": user_dict["id"]
    }

    key = f"user:{user_dict['id']}"

    try:
        existing = redis_client.get(key)
        if existing:
            existing_profile = json.loads(existing)
            existing_profile.update(profile)
            profile = existing_profile

        redis_client.set(key, json.dumps(profile))
    except Exception:
        # non-fatal: auth should still work if Redis is unavailable
        pass


def register_user(user_data):

    db = SessionLocal()

    try:
        existing_user = db.execute(
            text("""
            SELECT * FROM users
            WHERE email = :email
            """),
            {"email": user_data.email}
        ).fetchone()

        if existing_user:
            return {
                "status": "error",
                "message": "Email already exists"
            }

        hashed_password = hash_password(
            user_data.password
        )

        db.execute(
            text("""
            INSERT INTO users
            (
                full_name,
                email,
                age,
                password_hash
            )
            VALUES
            (
                :full_name,
                :email,
                :age,
                :password_hash
            )
            """),
            {
                "full_name":
                user_data.full_name,

                "email":
                user_data.email,

                "age":
                user_data.age,

                "password_hash":
                hashed_password
            }
        )

        db.commit()

        created_user = db.execute(
            text("""
            SELECT *
            FROM users
            WHERE email = :email
            """),
            {"email": user_data.email}
        ).fetchone()

        if created_user:
            _upsert_recommendation_profile(dict(created_user._mapping))

        return {
            "status": "success",
            "message":
            "User registered successfully"
        }

    finally:
        db.close()


def login_user(login_data):

    db = SessionLocal()

    try:
        user = db.execute(
            text("""
            SELECT *
            FROM users
            WHERE email = :email
            """),
            {"email": login_data.email}
        ).fetchone()

        if not user:
            return {
                "status": "error",
                "message":
                "Invalid credentials"
            }

        user_dict = dict(user._mapping)

        is_valid = verify_password(
            login_data.password,
            user_dict["password_hash"]
        )

        if not is_valid:
            return {
                "status": "error",
                "message":
                "Invalid credentials"
            }

        _upsert_recommendation_profile(user_dict)

        token = create_access_token({
            "user_id":
            user_dict["id"] 
        })

        return {
            "status": "success",
            "token": token,
            "user": {
                "id":
                user_dict["id"],

                "customer_id":
                str(user_dict["id"]),

                "full_name":
                user_dict["full_name"],

                "email":
                user_dict["email"],

                "age":
                user_dict["age"]
            }
        }

    finally:
        db.close()