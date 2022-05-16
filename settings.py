import os
from dotenv import load_dotenv


# Postgresql config
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = 5432
POSTGRES_NAME = 'postgres'
POSTGRES_USER = 'root'
POSTGRES_PASSWORD = 'secret'


SQLALCHEMY_SYNC_URL = f'postgresql+psycopg2://' \
                      f'{POSTGRES_USER}:{POSTGRES_PASSWORD}@' \
                      f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}'
SQLALCHEMY_ASYNC_URL = f'postgresql+asyncpg://' \
                       f'{POSTGRES_USER}:{POSTGRES_PASSWORD}@' \
                       f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}'
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_MAX_OVERFLOW = 10
SQLALCHEMY_ECHO = False