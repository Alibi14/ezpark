from typing import Callable
from fastapi import Request, FastAPI
from database import scoped_session


app = FastAPI()


@app.middleware('http')
async def sqlalchemy_session_handler(request: Request, call_next: Callable):
    session = scoped_session()
    request.state.session = session

    try:
        response = await call_next(request)
        await session.commit()
        await session.close()
        return response
    except BaseException as e:
        await session.rollback()
        await session.close()
        raise e