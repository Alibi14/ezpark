from typing import List, Optional, Union
from pydantic import BaseModel, ValidationError
from datetime import date, time, datetime


class AbstractBaseModel(BaseModel):
    class Config:
        orm_mode = True


class User(AbstractBaseModel):
    id: int
    username: str
    email: Optional[Union[str, None]] = None
    phone_number: Optional[Union[str, None]] = None
    full_name: Optional[Union[str, None]] = None
    favourite_announcements: Optional[List[int]] = []


class UserInDatabase(User):
    password: str


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    scopes: List[str] = []


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
    owner_id: int
    longitude: Optional[float] = None
    latitude: Optional[float] = None


class Announcements(AbstractBaseModel):
    items: List[Announcement] = []
