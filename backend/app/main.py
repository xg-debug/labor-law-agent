from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.exceptions import register_exception_handlers
from app.core.logging import setup_logging
from app.routers.auth import router as auth_router
from app.routers.chat import router as chat_router
from app.routers.contract import router as contract_router
from app.routers.document import router as document_router
from app.routers.health import router as health_router

setup_logging()

app = FastAPI(
    title="Labor Law Agent Backend",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(contract_router)
app.include_router(document_router)


@app.get("/", tags=["root"])
async def root() -> dict:
    return {
        "message": "Labor Law Agent Backend is running",
        "docs": "/docs",
    }
