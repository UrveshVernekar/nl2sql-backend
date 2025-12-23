from fastapi import APIRouter, HTTPException
from app.auth.security import hash_password, verify_password
from app.auth.jwt import create_access_token
from app.db.users import get_user_by_email, create_user
from app.auth.schemas import RegisterRequest, LoginRequest


router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register")
def register(payload: RegisterRequest):
    if get_user_by_email(payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    password_hash = hash_password(payload.password)
    user_id = create_user(payload.email, password_hash)

    return {
        "id": user_id,
        "message": "User registered successfully",
    }


@router.post("/login")
def login(payload: LoginRequest):
    user = get_user_by_email(payload.email)

    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user["id"])})

    return {
        "access_token": token,
        "token_type": "bearer",
    }