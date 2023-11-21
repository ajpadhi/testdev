from datetime import datetime, timedelta
from typing import Any

import requests
from bson.objectid import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Path, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import settings
from app.static_values import mongo_id_regex
from app.utilities.db import db
from app.utilities.get_common import (
    CommonMongoGetQueryParams,
    get_cisco_auth_token,
    get_records,
)
from app.utilities.logger import logger

from .models import Activity, ResponseActivity, ResponseStatus

router = APIRouter()
security = HTTPBearer()


@router.post("", response_model=ResponseStatus)
async def create_activity(payload: Activity) -> dict[str, Any]:
    """
    Create a new activity record
    """
    data = payload.model_dump()
    current_date = datetime.utcnow()

    duration_seconds = float(data.get("duration", 0))
    start_time = current_date - timedelta(seconds=duration_seconds)
    # removing duration field which should not be stored in database
    data.pop("duration")
    data["start_time"] = start_time
    data["end_time"] = current_date

    if not data.get("user_id"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    access_token = get_cisco_auth_token()
    resp = requests.get(
        "https://scripts.cisco.com/orgstats/api/1/entries",
        params={"users": data["user_id"]},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    # If the user doesn't exist throw an exception.
    if not resp.json():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    r = db.acts.insert_one(
        {
            "created_date": current_date,
            **data,
        }
    )
    logger.debug(f"Created New Activity: {r.inserted_id}")

    return {"id": str(r.inserted_id)}


@router.get(
    "", response_model=list[ResponseActivity], response_model_exclude_unset=True
)
async def get_activity(
    mongo_params: CommonMongoGetQueryParams = Depends(CommonMongoGetQueryParams),
    access_token: HTTPAuthorizationCredentials = Security(security),
) -> Any:
    """
    Get Query to fetch db records using filteration and sorting
    """
    header_token = access_token.credentials

    if header_token != settings.static_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )

    results = get_records(db, "acts", mongo_params)
    for item in results:
        if not item.get("sr"):
            item["sr"] = "-777777777"

    return results


@router.put("/{id}", response_model=ResponseStatus)
async def update_activity(
    id: str = Path(description="Activity ID", regex=mongo_id_regex),
) -> dict[str, Any]:
    """
    Update an existing activity
    """

    activity_id = ObjectId(id)

    current_activity = db.acts.find_one({"_id": activity_id})
    if not current_activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found",
        )

    update_data = {
        "end_time": datetime.utcnow(),
    }

    db.acts.update_one({"_id": activity_id}, {"$set": update_data})
    logger.debug(f"Updated Activity: {activity_id}")

    return {"id": id}
