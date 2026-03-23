from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="My FastAPI Application",
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # 允许所有来源
    allow_credentials=True,  # 允许发送 cookies
    allow_methods=["*"],     # 允许所有 HTTP 方法
    allow_headers=["*"],     # 允许所有 HTTP 头
)

@app.get("/", tags=["root"])
async def root() -> dict:
    return {"message": "Hello, World!"}

@app.get("/health", tags=["health"])
async def health_check() -> dict:
    return {
        "status": "ok",
        "service": "labor-law-agent-backend",
    }


# 后续在这里注册各种业务路由