from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.routes.products import (
    router as products_router
)

from backend.app.routes.auth import (
    router as auth_router
)

from backend.app.routes.wishlist import (
    router as wishlist_router
)

from backend.app.routes.search import (
    router as search_router
)

app = FastAPI(
    title="AI Recommendation System API"
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(products_router)
app.include_router(auth_router)
app.include_router(wishlist_router)
app.include_router(search_router)

# Serve H&M Images
app.mount(
    "/images",
    StaticFiles(
        directory="ml/data/raw/images"
    ),
    name="images"
)

@app.get("/")
def home():
    return {
        "message": "API is working!"
    }