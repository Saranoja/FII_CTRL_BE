from typing import List
from model import Meeting
from sqlalchemy import exc
from database_connection import db


class MeetingsRepository:
    @staticmethod
    def get_all_meetings() -> List[Meeting]:
        """
        :return: a list of all the meetings found in the database
        """
        return Meeting.query.all()

    @staticmethod
    def get_meeting_for_id(meeting_id) -> Meeting:
        """
        :return: the meeting object corresponding to {meeting_id}
        """
        return Meeting.query.filter(Meeting.id == meeting_id).first()

    @staticmethod
    def get_meetings_for_group(group_id: int):
        f"""
        :return: a list of all the meetings found in the database corresponding to the group with {group_id}
        """
        return Meeting.query.filter(Meeting.group_id == group_id).all()

    @staticmethod
    def get_meetings_by_author(author_id: int):
        f"""
            :return: a list of all the meetings posted by the author with {author_id}
            """
        return Meeting.query.filter(Meeting.author_id == author_id).all()

    @staticmethod
    def add_new_meeting(meeting):
        try:
            db.session.add(meeting)
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
        return meeting.id

    @staticmethod
    def update_meeting(meeting_id: int, updated_meeting_data: dict):
        try:
            target_meeting = Meeting.query.filter(Meeting.id == meeting_id)
            target_meeting.update(updated_meeting_data)
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            raise exc.SQLAlchemyError
        except KeyError:
            raise KeyError

    @staticmethod
    def delete_meeting(meeting_id: int):
        try:
            target_meeting = Meeting.query.filter(Meeting.id == meeting_id).first()
            db.session.delete(target_meeting)
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
            raise exc.SQLAlchemyError
