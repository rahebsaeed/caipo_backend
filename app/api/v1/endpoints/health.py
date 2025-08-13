# File: app/api/v1/endpoints/health.py
from fastapi import APIRouter

router = APIRouter()

@router.get("z") # Route will be /api/v1/healthz
def health_check():
    """
    Simple health check.
    """
    return {"status": "ok"}