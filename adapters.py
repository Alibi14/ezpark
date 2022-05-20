from typing import Iterable
import models
import domain


def record_to_user_with_password(
        record: models.User
) -> domain.UserInDatabase:
    return domain.UserInDatabase.from_orm(record)


def record_to_user_without_password(
        record: models.User
) -> domain.User:
    return domain.User.from_orm(record)


def record_to_announcement(
        record: models.Announcement
) -> domain.Announcement:
    return domain.Announcement.from_orm(record)


def records_to_announcements(
        records: Iterable[models.Announcement]
) -> domain.Announcements:
    announcements = domain.Announcements()
    for record in records:
        announcements.items.append(record_to_announcement(record=record))
    return announcements
