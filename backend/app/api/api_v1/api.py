from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, users, targets, scans, reports, health, sessions, academy

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(targets.router, prefix="/targets", tags=["targets"])
api_router.include_router(scans.router, prefix="/scans", tags=["scans"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
api_router.include_router(academy.router, prefix="/academy", tags=["academy"])