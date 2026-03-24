import hashlib
import json
import secrets
from pathlib import Path

from app.core.exceptions import AppException
from app.models.schemas import (
    AuthLoginRequest,
    AuthLoginResponse,
    AuthRegisterRequest,
    AuthUserInfo,
)


class AuthService:
    def __init__(self) -> None:
        self.base_dir = Path(__file__).resolve().parents[2]
        self.data_dir = self.base_dir / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.users_file = self.data_dir / "users.json"
        self.tokens: dict[str, str] = {}
        self.users: dict[str, dict] = self._load_users()

    def _load_users(self) -> dict[str, dict]:
        if not self.users_file.exists():
            return {}
        try:
            content = json.loads(self.users_file.read_text(encoding="utf-8"))
            if isinstance(content, dict):
                return content
        except Exception:
            return {}
        return {}

    def _save_users(self) -> None:
        self.users_file.write_text(
            json.dumps(self.users, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        return hashlib.sha256(f"{salt}:{password}".encode("utf-8")).hexdigest()

    def register(self, request: AuthRegisterRequest) -> AuthLoginResponse:
        account = request.account.strip().lower()
        nickname = request.nickname.strip()
        if account in self.users:
            raise AppException("account_exists", "该账号已注册", 409)

        salt = secrets.token_hex(8)
        password_hash = self._hash_password(request.password, salt)
        self.users[account] = {
            "account": account,
            "nickname": nickname,
            "salt": salt,
            "password_hash": password_hash,
        }
        self._save_users()
        return self._build_login_result(account)

    def login(self, request: AuthLoginRequest) -> AuthLoginResponse:
        account = request.account.strip().lower()
        user = self.users.get(account)
        if not user:
            raise AppException("invalid_credentials", "账号或密码错误", 401)
        password_hash = self._hash_password(request.password, user["salt"])
        if password_hash != user["password_hash"]:
            raise AppException("invalid_credentials", "账号或密码错误", 401)
        return self._build_login_result(account)

    def me(self, token: str) -> AuthUserInfo:
        account = self.tokens.get(token)
        if not account:
            raise AppException("unauthorized", "登录状态失效，请重新登录", 401)
        user = self.users.get(account)
        if not user:
            raise AppException("unauthorized", "账号不存在", 401)
        return AuthUserInfo(account=user["account"], nickname=user["nickname"])

    def _build_login_result(self, account: str) -> AuthLoginResponse:
        user = self.users[account]
        token = secrets.token_urlsafe(24)
        self.tokens[token] = account
        return AuthLoginResponse(
            token=token,
            user=AuthUserInfo(account=user["account"], nickname=user["nickname"]),
        )
