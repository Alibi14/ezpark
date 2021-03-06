from fastapi import HTTPException


class BaseHTTPExceptions(HTTPException):
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserDoesNotExist(BaseHTTPExceptions):
    detail = 'User record does not exist in db'
    status_code = 404


class AnnouncementDoesNotExist(BaseHTTPExceptions):
    detail = 'Announcement record does not exist in db'
    status_code = 404
