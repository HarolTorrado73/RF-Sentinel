from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check():
    return {
        "status": "healthy",
        "version": "0.1.0",
        "services": {
            "database": "configured",
            "redis": "configured",
            "celery": "configured",
        },
    }