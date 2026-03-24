from fastapi import APIRouter, Header

from app.core.exceptions import AppException
from app.models.schemas import (
    AuthLoginRequest,
    AuthLoginResponse,
    AuthRegisterRequest,
    AuthUserInfo,
)
from app.services.auth_service import AuthService


router = APIRouter(prefix="/api/auth", tags=["auth"])
auth_service = AuthService()


@router.post("/register", response_model=AuthLoginResponse)
async def register(request: AuthRegisterRequest) -> AuthLoginResponse:
    return auth_service.register(request)


@router.post("/login", response_model=AuthLoginResponse)
async def login(request: AuthLoginRequest) -> AuthLoginResponse:
    return auth_service.login(request)


@router.get("/me", response_model=AuthUserInfo)
async def me(authorization: str = Header(default="")) -> AuthUserInfo:
    if not authorization.startswith("Bearer "):
        raise AppException("unauthorized", "缺少登录令牌", 401)
    token = authorization.replace("Bearer ", "", 1).strip()
    if not token:
        raise AppException("unauthorized", "缺少登录令牌", 401)
    return auth_service.me(token)
