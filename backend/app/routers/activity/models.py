from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.static_values import sr_regex


class Activity(BaseModel):
    user_id: str = Field(example="cec_id", description="CEC User Id")
    source: str = Field(
        example="BDB Task",
        description="Activity Source Application Name",
    )
    source_url: str = Field(
        example="https://example.com",
        description="Activity Source URL",
    )
    action: str = Field(example="tool", description="What action is being tracked")
    duration: int = Field(example="10", description="Duration of wait time in seconds")
    sr: Optional[str] = Field(
        None,
        example="612345678",
        description="SR Number",
        pattern=sr_regex,
    )


class ResponseStatus(BaseModel):
    id: str


class ResponseActivity(BaseModel):
    created_date: Optional[datetime] = None
    user_id: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    action: Optional[str] = None
    sr: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
