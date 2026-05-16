from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routes.products import (
    router as products_router
)

from backend.app.routes.auth import (
    router as auth_router
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

app.include_router(products_router)
app.include_router(auth_router)

@app.get("/")
def home():
    return {
        "message": "API is working!"
    }