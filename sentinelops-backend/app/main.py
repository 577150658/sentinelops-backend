from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import init_db
from app.routers import api_router
from app.routers.ws import ws_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    from app.db.seed_extra import seed_extra_if_empty
    seed_extra_if_empty()
    print(f"[startup] {settings.APP_NAME} 已就绪")
    yield
    print("[shutdown] 服务停止")


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
app.include_router(ws_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.APP_NAME}


@app.get("/")
async def root():
    return {"service": settings.APP_NAME, "docs": "/docs", "health": "/health"}
