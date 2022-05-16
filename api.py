import base64
from fastapi import Request
from service.announcement import AnnouncementService
from service import auth
from payload import AnnouncementCreatePayload, AnnouncementListPayload
import domain
from middleware import app


app.include_router(auth.router, prefix='/auth')


@app.post('/api/announcement/add')
async def create(request: Request) -> domain.Announcement:
    body = await request.json()
    payload = AnnouncementCreatePayload(**body)
    print(payload.dict())
    service = AnnouncementService(session=request.state.session)
    return await service.create(**payload.dict(exclude_unset=True))


@app.post('/api/announcement/get')
async def get_one_element(request: Request) -> domain.Announcement:
    body = await request.json()
    service = AnnouncementService(session=request.state.session)
    return await service.get(**body)


@app.post('/api/announcement/select')
async def select_multiple(request: Request) -> domain.Announcements:
    body = await request.json()
    print(request.headers)
    payload = AnnouncementListPayload(**body)
    service = AnnouncementService(session=request.state.session)
    return await service.select(**payload.dict(exclude_unset=True))


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
