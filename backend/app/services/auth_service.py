from sqlalchemy import text

from backend.app.database.db import SessionLocal
from backend.app.utils.hash import (
    hash_password,
    verify_password
)
from backend.app.utils.token import (
    create_access_token
)


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