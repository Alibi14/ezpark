from datetime import datetime, timedelta
from typing import Union, List
from fastapi import HTTPException, status

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import async_scoped_session
from service.base import BaseService

from jose import JWTError, jwt
from passlib.context import CryptContext
from domain import User, TokenData
from provider import UserProvider

SECRET_KEY = 'd20649f1be6ae39dc7994b01ab503ec888876307fff702082bc75f9ca8fb87f2'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService(BaseService):
    _provider: UserProvider

    def __init__(self, session: async_scoped_session):
        super().__init__(session=session)
        self._provider = UserProvider(session=session)

    def get_password_hash(
            self,
            password
    ) -> str:
        return pwd_context.hash(password)

    async def get_user(
            self,
            username: str
    ) -> User:
        user = await self._provider.user_with_password(username)
        return user

    def verify_password(
            self,
            plain_password,
            hashed_password
    ):
        return pwd_context.verify(plain_password, hashed_password)

    async def authenticate_user(
            self,
            username: str,
            password: str
    ):
        user = await self._provider.user_with_password(username)
        if not self.verify_password(password, user.password):
            return False
        return user

    def create_access_token(
            self,
            data: dict,
            expires_delta: Union[timedelta, None] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def get_current_user(
            self,
            token: str
    ) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = await self.get_user(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user

    async def login_for_access_token(
            self,
            form_data: OAuth2PasswordRequestForm
    ):
        user = await self.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        access_token = self.create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "Bearer"}

    async def add_to_favourites(
            self,
            id: int,
            announcement_id: int,
            favourite_announcements: List[int] ,
    ):
        if announcement_id not in favourite_announcements:
            favourite_announcements.append(announcement_id)
        else:
            favourite_announcements.remove(announcement_id)

        favourite_announcements.sort()
        return await self._provider.update(id=id, favourite_announcements=favourite_announcements)


