from typing import Any, Dict, List, Optional, Union, Literal
from pydantic import BaseModel
from datetime import date, time, datetime


class AnnouncementCreatePayload(BaseModel):
    name: str
    announcement_type: str
    start_date: date
    end_date: date
    start_time: time
    end_time: time
    parking_type: Optional[List[int]] = []
    address: str
    price: Optional[float]


class AnnouncementListPayload(BaseModel):
    name: Optional[str] = None
    announcement_type: Optional[Literal['for_sale', 'for_rent']] = None
    parking_type: Optional[List[int]] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    start_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    announcement_date: Optional[datetime] = None


class AnnouncementGetOneElementPayload(BaseModel):
    id: int


class AnnouncementDeletePayload(BaseModel):
    id: int
