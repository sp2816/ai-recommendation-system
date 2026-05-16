from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    BigInteger,
    ForeignKey,
    TIMESTAMP,
    DECIMAL
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.app.database.db import Base


# ==========================
# USERS TABLE
# ==========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    age = Column(Integer)
    password_hash = Column(Text, nullable=False)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )


# ==========================
# PRODUCTS TABLE
# ==========================
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(
        BigInteger,
        unique=True,
        nullable=False
    )

    product_name = Column(String(255))
    product_type_name = Column(String(255))
    product_group_name = Column(String(255))
    colour_group_name = Column(String(255))

    price = Column(DECIMAL(10, 2))
    description = Column(Text)

    image_url = Column(Text)
    product_url = Column(Text)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )


# ==========================
# WISHLIST TABLE
# ==========================
class Wishlist(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id")
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )


# ==========================
# VIEW HISTORY TABLE
# ==========================
class ViewHistory(Base):
    __tablename__ = "view_history"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id")
    )

    viewed_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )


# ==========================
# SEARCH HISTORY TABLE
# ==========================
class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    search_query = Column(Text)

    searched_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )


# ==========================
# USER INTERACTIONS TABLE
# ==========================
class UserInteraction(Base):
    __tablename__ = "user_interactions"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id")
    )

    interaction_type = Column(
        String(50)
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )