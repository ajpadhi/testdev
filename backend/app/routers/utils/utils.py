from typing import Any

from fastapi import APIRouter

from .models import APIStatus

router = APIRouter()


@router.get("/api-status", response_model=APIStatus)
async def get_api_status() -> Any:
    """
    This is used to test the availability of the API
    """
    return {"status": "success"}
