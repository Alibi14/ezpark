from typing import Type, List
from sqlalchemy import insert, select, delete, update, func, and_
from sqlalchemy.ext.asyncio import async_scoped_session
from datetime import date, time
import adapters
import domain
import exceptions
import models


class BaseProvider:
    session: async_scoped_session

    def __init__(self, session: async_scoped_session):
        self.session = session

    def clear_from_ellipsis(self, **kwargs):
        data = dict()
        for key, value in kwargs.items():
            if value is not ...:
                data[key] = value

        return data


class AnnouncementProvider(BaseProvider):
    _model: Type[models.Announcement] = models.Announcement

    async def insert(
        self,
        **kwargs
    ) -> domain.Announcement:
        data = self.clear_from_ellipsis(**kwargs)

        insert_stmt = insert(self._model).values(**data).returning(self._model)
        select_stmt = select(self._model).from_statement(insert_stmt)
        print(select_stmt)
        record = await self.session.scalar(select_stmt) # execute
        return adapters.record_to_announcement(record)

    async def select_one(
        self,
        id: int = ...,
        name: str = ...
    ) -> domain.Announcement:

        select_stmt = select(self._model)
        if id is not ...:
            select_stmt = select_stmt.where(self._model.id == id)
        if name is not ...:
            select_stmt = select_stmt.where(self._model.name == name)

        record = await self.session.scalar(select_stmt)
        if not record:
            raise exceptions.AnnouncementDoesNotExist

        return adapters.record_to_announcement(record=record)

    async def select_multi(
        self,
        name: str = ...,
        announcement_type: int = ...,
        parking_type: List = ...,
        min_price: float = ...,
        max_price: float = ...,
        start_date: date = ...,
        start_time: time = ...,
        end_time: time = ...
    ) -> domain.Announcements:

        select_stmt = select(self._model)

        if name is not ...:
            select_stmt = select_stmt.where(self._model.name == name)
        if announcement_type is not ...:
            select_stmt = select_stmt.where(self._model.announcement_type == announcement_type)
        if parking_type is not ...:
            for park in parking_type:
                select_stmt = select_stmt.filter(self._model.parking_type.any(park))
        if min_price is not ...:
            select_stmt = select_stmt.where(self._model.price >= min_price)
        if max_price is not ...:
            select_stmt = select_stmt.where(self._model.price <= max_price)
        if start_date is not ...:
            select_stmt = select_stmt.where(self._model.start_date >= start_date)
        if start_time is not ...:
            select_stmt = select_stmt.where(self._model.start_time >= start_time)
        if end_time is not ...:
            select_stmt = select_stmt.where(self._model.end_time <= end_time)

        records = await self.session.scalars(select_stmt) # db Object
        return adapters.records_to_announcements(records=records) # db Object -> python obJect

    async def update(
        self,
        id: int,
        name: str = ...
    ) -> domain.Announcement:

        if name is not ...:
            update_stmt = update(self._model).where(
                self._model.id == id
            ).values(name=name).returning(self._model)
            select_stmt = select(self._model).from_statement(update_stmt)

        record = await self.session.scalar(select_stmt)
        return adapters.record_to_announcement(record=record)

    async def delete(
        self,
        id: int
    ):
        delete_stmt = delete(self._model).where(self._model.id == id)
        await self.session.execute(delete_stmt)

# class RequestProvider(BaseProvider):
#     _model: Type[models.Request] = models.Request
#
#     async def insert(
#         self,
#         body: str,
#         url_id: int
#     ) -> domain.Request:
#         insert_stmt = insert(self._model).values(
#             body=body,
#             url_id=url_id
#         ).returning(self._model)
#         select_stmt = select(self._model).from_statement(insert_stmt)
#         record = await self.session.scalar(select_stmt)
#         return adapters.request_record_to_request_domain(record=record)
#
#     async def select_one(
#         self,
#         id: int = ...,
#         body: str = ...,
#         url_id: int = ...
#     ) -> domain.Request:
#         select_stmt = select(self._model)
#         if id is not ...:
#             select_stmt = select_stmt.where(self._model.id == id)
#         if body is not ...:
#             select_stmt = select_stmt.where(self._model.body == body)
#         if url_id is not ...:
#             select_stmt = select_stmt.where(self._model.url_id == url_id)
#
#         record = await self.session.scalar(select_stmt)
#         if not record:
#             raise exceptions.RequestDoesNotExist
#
#         return adapters.request_record_to_request_domain(record=record)
#
#     async def select_multi(
#         self,
#         body: str = ...,
#         url_id: int = ...
#     ) -> domain.Requests:
#         select_stmt = select(self._model)
#         if body is not ...:
#             select_stmt = select_stmt.where(self._model.body == body)
#         if url_id is not ...:
#             select_stmt = select_stmt.where(self._model.url_id == url_id)
#
#         records = await self.session.scalars(select_stmt)
#         return adapters.request_records_to_requests_domain(records=records)
#
#     async def delete(
#         self,
#         id: int
#     ):
#         delete_stmt = delete(self._model).where(self._model.id == id)
#         await self.session.execute(delete_stmt)
#
#     async def update(
#         self,
#         id: int,
#         body: str
#     ) -> domain.Request:
#         update_stmt = update(self._model).where(
#             self._model.id == id
#         ).values(body=body).returning(self._model)
#         select_stmt = select(self._model).from_statement(update_stmt)
#
#         record = await self.session.scalar(select_stmt)
#         return adapters.request_record_to_request_domain(record=record)
#
#     async def select_count(self) -> int:
#         select_stmt = select(func.count(self._model.id))
#         count = await self.session.scalar(select_stmt)
#         if count is None:
#             return 0
#         return count
#
#     async def select_duplicates_count(self) -> int:
#         """
#         SQL STATEMENT:
#         SELECT sum(anon_1.group_counts) AS sum_1
#         FROM (SELECT request.body AS body, count(request.body) AS group_counts
#         FROM request GROUP BY request.body
#         HAVING count(request.body) > :count_1) AS anon_1
#         :return:
#         """
#         subquery_alias = select(
#             self._model.body,
#             func.count(self._model.body).label('group_counts')
#         ).group_by(self._model.body).having(
#             func.count(self._model.body) > 1
#         ).subquery().alias()
#         select_stmt = select(func.sum(subquery_alias.c.group_counts)).select_from(subquery_alias)
#
#         duplicates_count = await self.session.scalar(select_stmt)
#         if duplicates_count is None:
#             return 0
#         return duplicates_count