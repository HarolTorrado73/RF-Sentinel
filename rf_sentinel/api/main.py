"""API REST para RF Sentinel."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from rf_sentinel.api.routers import (
    captures_router,
    classification_router,
    detection_router,
    export_router,
    scans_router,
)
from rf_sentinel.core.config import settings

app = FastAPI(
    title="RF Sentinel API",
    description="API para análisis de radiofrecuencia",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scans_router)
app.include_router(captures_router)
app.include_router(detection_router)
app.include_router(classification_router)
app.include_router(export_router)


@app.get("/health")
async def health_check() -> dict:
    return {"status": "healthy", "version": "0.1.0"}
