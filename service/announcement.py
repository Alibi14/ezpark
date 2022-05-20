import asyncio
import random
from typing import Any, Dict, Optional, List
from sqlalchemy.ext.asyncio import async_scoped_session
from service.base import BaseService
from provider import AnnouncementProvider
from enum import Enum
import domain
import exceptions
from datetime import date, time, datetime


class AnnouncementType(str, Enum):
    for_rent = 'for_rent'
    for_sale = 'for_sale'


class AnnouncementService(BaseService):
    _provider: AnnouncementProvider

    def __init__(self, session: async_scoped_session):
        super().__init__(session=session)
        self._provider = AnnouncementProvider(session=session)

    async def create(
        self,
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
    ) -> domain.Announcement:

        image_urls = [
            "https://uploads-ssl.webflow.com/621f6615a4c8a1d5166a4362/62615ca29b7d0a31079ac32e_smart%20parking.jpeg",
            "https://circontrol.com/wp-content/uploads/2019/02/180125-Circontrol-BAIXA-80.jpg",
            "https://thumbs.dreamstime.com/b/d-render-parking-lot-d-render-parking-lot-auto-parking-area-168894850.jpg",
            "https://thephiladelphiacitizen.org/wp-content/uploads/2019/07/apartments-1265032_960_720.jpg"
        ]

        if announcement_type == AnnouncementType.for_rent:
            announcement_type = 0
        elif announcement_type == AnnouncementType.for_sale:
            announcement_type = 1

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
            favourite=bool(random.getrandbits(1))
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
        announcement_type: str = ...,
        parking_type: List = ...,
        min_price: float = ...,
        max_price: float = ...,
        start_date: date = ...,
        start_time: time = ...,
        end_time: time = ...
    ) -> domain.Announcements:

        if announcement_type == AnnouncementType.for_rent:
            announcement_type = 0
        elif announcement_type == AnnouncementType.for_sale:
            announcement_type = 1

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
    # async def get_or_create(
    #     self,
    #     url: str
    # ) -> domain.Announcement:
    #     try:
    #         return await self.get(url=url)
    #     except exceptions.UrlDoesNotExist:
    #         return await self.create(url=url)
