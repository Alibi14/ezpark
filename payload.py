from typing import Any, Dict, List, Optional, Union, Literal
from pydantic import BaseModel, ValidationError, validator
from datetime import date, time, datetime


class UserRegistrationPayload(BaseModel):

    username: str
    password1: str
    password2: str
    email: Optional[str] = None
    phone_number: Optional[str] = None

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if v != values['password1']:
            raise ValueError('passwords do not match')
        return v


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
    longitude: Optional[float]
    latitude: Optional[float]


class AnnouncementListPayload(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
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
