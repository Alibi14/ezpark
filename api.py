import base64
from fastapi import Request, Depends
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)
from service.auth import UserService
from service.announcement import AnnouncementService
from payload import AnnouncementCreatePayload, AnnouncementListPayload, AnnouncementGetOneElementPayload, \
    UserRegistrationPayload
import domain
from middleware import app


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token"
)


# User Authentication
@app.post('/token', response_model=domain.Token)
async def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    service = UserService(session=request.state.session)
    return await service.login_for_access_token(form_data)


@app.get("/users/me/", response_model=domain.User)
async def read_users_me(
        reqeust: Request,
        current_user: str = Depends(oauth2_scheme)
) -> domain.User:
    service = UserService(session=reqeust.state.session)
    return await service.get_current_user(token=current_user)


@app.post('/registration', response_model=domain.User)
async def registration(
        request: Request
):
    body = await request.json()
    payload = UserRegistrationPayload(**body)
    service = UserService(session=request.state.session)
    return await service.registration(**payload.dict(exclude_unset=True))


# Announcements
@app.post('/api/announcement/add')
async def create(request: Request, current_user: str = Depends(oauth2_scheme)) -> domain.Announcement:
    body = await request.json()
    print(current_user, 'current_user ')
    payload = AnnouncementCreatePayload(**body)
    service = AnnouncementService(session=request.state.session)
    return await service.create(**payload.dict(exclude_unset=True), token=current_user)


@app.post('/api/announcement/add_or_remove_from_favourites')
async def create(request: Request, current_user: str = Depends(oauth2_scheme)) -> domain.Announcement:
    body = await request.json()
    payload = AnnouncementGetOneElementPayload(**body)
    service = AnnouncementService(session=request.state.session)
    return await service.add_to_favourites(**payload.dict(exclude_unset=True), token=current_user)


@app.post('/api/announcement/get')
async def get_one_element(request: Request) -> domain.Announcement:
    body = await request.json()
    service = AnnouncementService(session=request.state.session)
    return await service.get(**body)


@app.post('/api/announcement/select')
async def select_multiple(request: Request) -> domain.Announcements:
    body = await request.json()
    payload = AnnouncementListPayload(**body)
    service = AnnouncementService(session=request.state.session)
    return await service.select(**payload.dict(exclude_unset=True))


@app.post('/api/announcement/my_announcements')
async def select_multiple(request: Request, current_user: str = Depends(oauth2_scheme)) -> domain.Announcements:
    service = AnnouncementService(session=request.state.session)
    return await service.select_my_announcements(token=current_user)


@app.post('/api/announcement/favourites')
async def select_multiple(request: Request, current_user: str = Depends(oauth2_scheme)) -> domain.Announcements:
    service = AnnouncementService(session=request.state.session)
    return await service.select_favourite_announcements(token=current_user)


@app.put('/api/announcement/edit')
async def edit(request: Request) -> domain.Announcement:
    body = await request.json()
    service = AnnouncementService(session=request.state.session)
    return await service.edit(**body)


@app.delete('/api/announcement/remove')
async def remove(request: Request) -> dict:
    body = await request.json()
    service = AnnouncementService(session=request.state.session)
    return await service.remove(**body)
