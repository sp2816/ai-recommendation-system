from fastapi import APIRouter

from backend.app.schemas.auth_schema import (
    RegisterRequest,
    LoginRequest
)

from backend.app.services.auth_service import (
    register_user,
    login_user
)

router = APIRouter(
    prefix="/api"
)


@router.post("/register")
def register(data: RegisterRequest):
    return register_user(data)


@router.post("/login")
def login(data: LoginRequest):
    return login_user(data)