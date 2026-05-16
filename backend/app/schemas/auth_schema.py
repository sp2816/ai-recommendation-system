from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    age: int
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str