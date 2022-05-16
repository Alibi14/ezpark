from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


router = APIRouter()


SECRET_KEY = "c1857565452bd707179b5a768bc7eb41557738eedd7eb313023dfcdddbd5a34f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7


fake_users_db = {
    "alibi": {
        "username": "alibi",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
    },
    "developer": {
        "username": "developer",
        "hashed_password": "$2b$12$cersiPbACY7qNDC5iAbpQOrdJdnZOUA1ZuRebgixatZGw7OiaPsRq"
    },
    "marlen": {
        "username": "marlen",
        "hashed_password": "$2b$12$TmKjtYJffxTiuzgGNsjlPerSaCBLFVKvsGvTUbFEdp.bvU04qqnwu"
    },
    "shapagat": {
        "username": "shapagat",
        "hashed_password": "$2b$12$RYh5XeIncX1.z2677n/QseKFnYpW4v2/CJEq7.aSjyHURO4aT4IGK"
    },
    "dauren": {
        "username": "dauren",
        "hashed_password": "$2b$12$DSLKpS399VDWmAmduH5/eer9THSv99ACWc4W2p5/up9q3NxREiuHu"
    },
    "alina": {
        "username": "alina",
        "hashed_password": "$2b$12$yLm./rEIWVsXdJHPIGqxv.z/2Y3cGwGhXYqA61pm2iBc.O8VhUNOi"
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
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
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
