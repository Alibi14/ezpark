# from sqlalchemy.ext.asyncio import async_scoped_session
# from provider import UserProvider
# from service.base import BaseService
#
#
# class UserService(BaseService):
#     _provider: UserProvider
#
#     def __init__(self, session: async_scoped_session):
#         super().__init__(session=session)
#         self._provider = UserProvider(session=session)
#
from datetime import datetime, timedelta
from typing import Union


from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from domain import User, UserInDatabase, Token, TokenData
from provider import UserProvider

router = APIRouter()

SECRET_KEY = 'd20649f1be6ae39dc7994b01ab503ec888876307fff702082bc75f9ca8fb87f2'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(session, username: str):
    provider = UserProvider(session=session)
    user = await provider.user_with_password(username)
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(session, username: str, password: str):
    provider = UserProvider(session=session)
    user = await provider.user_with_password(username)
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def fake_decode_token(session, token) -> UserInDatabase:

    provider = UserProvider(session=session)
    user = await provider.user_with_password(username=token)
    return user


@router.get("/users/me")
async def get_current_user(request: Request):
    token = request.headers['Authorization']
    token: str = token.split(' ')[1]

    credenetials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credenetials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credenetials_exception

    user = await get_user(session=request.state.session, username=token_data.username)
    print(user)
    return user


@router.post('/token', response_model=Token)
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(request.state.session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"token": access_token, "token_type": "Bearer"}
