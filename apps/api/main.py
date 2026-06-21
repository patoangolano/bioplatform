import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import engine
from routers.sequences import router as sequences_router
from routers.auth import router as auth_router
from routers.blast import router as blast_router
from routers.admin import router as admin_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("bioplatform-api starting up")
    yield
    logger.info("bioplatform-api shutting down")
    await engine.dispose()


app = FastAPI(title="bioplatform", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────
app.include_router(auth_router, prefix="/api/v1")
app.include_router(sequences_router, prefix="/api/v1")
app.include_router(blast_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "bioplatform-api"}


@app.get("/")
async def root():
    return {
        "name": "bioplatform",
        "version": "0.1.0",
        "docs": "/docs",
        "endpoints": ["/api/v1/sequences"],
    }
