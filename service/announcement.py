from typing import Any, Dict, Optional, List
from datetime import date, time, datetime
from enum import Enum
import random
import asyncio
from sqlalchemy.ext.asyncio import async_scoped_session
from service.base import BaseService
from provider import AnnouncementProvider
from service.auth import UserService
import domain
import exceptions


class AnnouncementType(str, Enum):
    for_rent = 'for_rent'
    for_sale = 'for_sale'


class AnnouncementService(BaseService):
    _provider: AnnouncementProvider
    _user_service: UserService

    def __init__(self, session: async_scoped_session):
        super().__init__(session=session)
        self._provider = AnnouncementProvider(session=session)
        self._user_service = UserService(session=session)

    async def create(
        self,
        token: str,
        name: str,
        announcement_type: str,
        start_date: date,
        end_date: date,
        start_time: time,
        end_time: time,
        announced_date: datetime = datetime.now(),
        parking_type: List[int] = [],
        address: str = ...,
        price: float = ...,
        longitude: float = ...,
        latitude: float = ...
    ) -> domain.Announcement:

        user = await self._user_service.get_current_user(token=token)

        image_urls = [
            "https://uploads-ssl.webflow.com/621f6615a4c8a1d5166a4362/62615ca29b7d0a31079ac32e_smart%20parking.jpeg",
            "https://upload.wikimedia.org/wikipedia/commons/1/19/Blue_Disc_Parking_Area_Markings_Blue_Paint.JPG",
            "https://thumbs.dreamstime.com/b/d-render-parking-lot-d-render-parking-lot-auto-parking-area-168894850.jpg",
            "https://thephiladelphiacitizen.org/wp-content/uploads/2019/07/apartments-1265032_960_720.jpg"
        ]

        if announcement_type == AnnouncementType.for_rent:
            announcement_type = 1
        elif announcement_type == AnnouncementType.for_sale:
            announcement_type = 0

        return await self._provider.insert(
            name=name,
            announcement_type=announcement_type,
            parking_type=parking_type,
            address=address,
            price=price,
            start_date=start_date,
            end_date=end_date,
            start_time=start_time,
            end_time=end_time,
            announced_date=announced_date,
            image_url=image_urls[random.randint(0, 3)],
            owner_id=user.id,
            longitude=longitude,
            latitude=latitude
        )

    async def get(
        self,
        id: int = ...,
        name: str = ...
    ) -> domain.Announcement:

        return await self._provider.select_one(
            id=id,
            name=name
        )

    async def select(
        self,
        name: str = ...,
        address: str = ...,
        announcement_type: str = ...,
        parking_type: List = ...,
        min_price: float = ...,
        max_price: float = ...,
        start_date: date = ...,
        start_time: time = ...,
        end_time: time = ...
    ) -> domain.Announcements:

        if announcement_type == AnnouncementType.for_rent:
            announcement_type = 1
        elif announcement_type == AnnouncementType.for_sale:
            announcement_type = 0

        return await self._provider.select_multi(
            name=name,
            announcement_type=announcement_type,
            parking_type=parking_type,
            min_price=min_price,
            max_price=max_price,
            start_date=start_date,
            start_time=start_time,
            end_time=end_time
        )

    async def select_my_announcements(
        self,
        token: str
    ):
        user = await self._user_service.get_current_user(token=token)

        return await self._provider.select_multi(owner_id=user.id)

    async def edit(
        self,
        id: int,
        name: str,
    ) -> domain.Announcement:

        return await self._provider.update(id=id, name=name)

    async def remove(
        self,
        id: int
    ):
        await self._provider.delete(id=id)
        return {'deleted': f'item {id}'}

    async def add_to_favourites(
        self,
        token: str,
        id: int
    ):
        user = await self._user_service.get_current_user(token=token)
        if user.favourite_announcements is None:
            user.favourite_announcements = []
        return await self._user_service.add_to_favourites(
            id=user.id,
            favourite_announcements=user.favourite_announcements,
            announcement_id=id
        )

    async def select_favourite_announcements(
        self,
        token: str
    ):
        user = await self._user_service.get_current_user(token=token)

        return await self._provider.select_multi(favourite_announcements=user.favourite_announcements)
    # async def get_or_create(
    #     self,
    #     url: str
    # ) -> domain.Announcement:
    #     try:
    #         return await self.get(url=url)
    #     except exceptions.UrlDoesNotExist:
    #         return await self.create(url=url)
