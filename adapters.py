from typing import Iterable
import models
import domain


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
