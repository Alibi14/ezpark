from typing import List, Optional, Union
from pydantic import BaseModel
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


class UserInDatabase(User):
    password: str


class Token(BaseModel):
    token: str


class TokenData(BaseModel):
    username: Union[str, None] = None


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
