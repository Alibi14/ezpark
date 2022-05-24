from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Date, Time, DateTime, Float, Boolean
from sqlalchemy.orm import declarative_base, relationship
import sqlalchemy.types as types

Base = declarative_base()


class AbstractBaseModel(Base):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, autoincrement=True)


class User(AbstractBaseModel):
    __tablename__ = 'user'

    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    favourite_announcements = Column(types.ARRAY(Integer), nullable=True)

    announcements = relationship("Announcement")


class Announcement(AbstractBaseModel):
    __tablename__ = 'announcement'

    FOR_RENT = 0
    FOR_SALE = 1

    name = Column(String, nullable=False)
    address = Column(String, unique=True)

    price = Column(Float, nullable=True)
    announcement_type = Column(Integer, nullable=False)
    parking_type = Column(types.ARRAY(Integer), nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    announced_date = Column(DateTime, nullable=True)

    image_url = Column(String)

    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship("User", back_populates="announcements")
