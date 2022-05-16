from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from datetime import date, time, datetime


class AbstractBaseModel(BaseModel):
    class Config:
        orm_mode = True


class Announcement(AbstractBaseModel):
    id: int
    name: str
    address: str
    price: Optional[float]
    announcement_type: int
    parking_type: Optional[List[int]] = []
    start_date: date
    end_date: date
    start_time: time
    end_time: time

    announced_date: datetime
    image_url: Optional[str]
    favourite: Optional[bool]


class Announcements(AbstractBaseModel):
    items: List[Announcement] = []
