from typing import List
from model import Announcement
from sqlalchemy import exc
from database_connection import db


class AnnouncementsRepository:
    @staticmethod
    def get_all_announcements() -> List[Announcement]:
        """
        :return: a list of all the announcements found in the database
        """
        return Announcement.query.all()

    @staticmethod
    def get_announcement_with_id(announcement_id: int) -> Announcement:
        f"""
        :return: the announcement with id {announcement_id}
        """
        return Announcement.query.filter(Announcement.id == announcement_id).first()

    @staticmethod
    def get_announcements_for_group(group_id: int):
        f"""
        :return: a list of all the announcements found in the database corresponding to the group with {group_id}
        """
        return Announcement.query.filter(Announcement.discussion_group_id == group_id).all()

    @staticmethod
    def add_new_announcement(announcement: Announcement):
        try:
            db.session.add(announcement)
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            raise exc.SQLAlchemyError

    @staticmethod
    def update_announcement(announcement_id: int, updated_announcement: dict):
        try:
            target_announcement = Announcement.query.filter(Announcement.id == announcement_id)
            target_announcement.update(updated_announcement)
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            raise exc.SQLAlchemyError
        except KeyError:
            raise KeyError

    @staticmethod
    def delete_announcement(announcement_id: int):
        try:
            target_announcement = Announcement.query.filter(Announcement.id == announcement_id).first()
            db.session.delete(target_announcement)
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            raise exc.SQLAlchemyError
