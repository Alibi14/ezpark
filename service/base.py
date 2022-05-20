from sqlalchemy.ext.asyncio import async_scoped_session


class BaseService:
    def __init__(self, session: async_scoped_session):
        pass