import json
from datetime import datetime
from json import JSONDecodeError
from typing import Any, Optional, Union

import pymongo
import requests
from bson.json_util import loads as bson_loads
from fastapi import HTTPException, Query, status
from pymongo.database import Database
from requests.auth import HTTPBasicAuth

from app.config import settings

from .logger import logger


class CommonMongoGetQueryParams:
    def __init__(
        self,
        filter: Optional[str] = Query(
            None,
            description="JSON Mongo Filter compliant with "
            "[JSON to BSON format]"
            "(https://pymongo.readthedocs.io/en/stable/api/bson/json_util.html)",
        ),
        projection: Optional[str] = Query(
            None,
            description="CSV of fields to return or a JSON projection object",
        ),
        limit: Optional[int] = Query(
            200, gt=0, le=2000, description="Number of items to return"
        ),
        skip: Optional[int] = Query(0, ge=0, description="Number of items to skip"),
        sort_key: Optional[str] = Query(None, description="Field to sort on"),
        sort_ascending: Optional[bool] = Query(False, description="Sort direction"),
    ):
        self.filter = self.validate_filter(filter)
        self.projection = self.validate_projection(projection)
        self.limit = limit
        self.skip = skip
        self.sort_key = sort_key
        self.sort_ascending = sort_ascending

    @staticmethod
    def validate_filter(
        value: Optional[str],
    ) -> Optional[dict[str, Union[str, int, datetime]]]:
        query_filter = None

        if value:
            try:
                query_filter = bson_loads(value)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="The provided filter is not valid BSON/JSON format",
                )

        return query_filter

    @staticmethod
    def validate_projection(
        value: Optional[str],
    ) -> Optional[Any]:
        if value:
            try:
                p = json.loads(value)
                logger.debug(f"projection was JSON: {p}")
                return p
            except (JSONDecodeError, TypeError):
                logger.debug("Looks like our projection wasnt JSON")

            # TODO: we should do better about santizing nonsense here
            fields = {e.strip(): 1 for e in value.split(",") if e.strip()}
            if fields:
                p = {"_id": 1, **fields}
                logger.debug(f"projection was csv, here is what we got: {p}")
                return p

        return None


def get_records(
    db_instance: Database[Any],
    collection_name: str,
    mongo_params: CommonMongoGetQueryParams,
    exclude_id: bool = True,
) -> list[dict[str, Any]]:
    """
    Get records from a mongo db using the common collection
    level options and removing the `_id` ObjectId from the
    records
    """
    results = []
    sort_method = (
        pymongo.ASCENDING if mongo_params.sort_ascending else pymongo.DESCENDING
    )
    for entry in db_instance[collection_name].find(
        filter=mongo_params.filter,
        projection=mongo_params.projection,
        limit=mongo_params.limit,
        skip=mongo_params.skip,
        sort=[(mongo_params.sort_key, sort_method)] if mongo_params.sort_key else None,
    ):
        if entry:
            if exclude_id:
                del entry["_id"]
            results.append(entry)

    return results


def get_cisco_auth_token() -> str:
    """
    Authenticate to get access token
    """
    try:
        ACTS_GEN_USER = settings.acts_gen_user
        ACTS_GEN_PASSWORD = settings.acts_gen_password
        r = requests.get(
            "https://scripts.cisco.com/api/v2/auth/login",
            auth=HTTPBasicAuth(ACTS_GEN_USER, ACTS_GEN_PASSWORD),
        )

        r.raise_for_status()
        access_token = r.headers["access_token"]
        return access_token
    except requests.exceptions.HTTPError as err:
        raise HTTPException(
            status_code=err.response.status_code,
            detail=err.response.text,
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err)
        )
