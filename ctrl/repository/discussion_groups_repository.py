from typing import List
from model import DiscussionGroup
from sqlalchemy import exc
from database_connection import db


class DiscussionGroupsRepository:
    @staticmethod
    def get_all_discussion_groups() -> List[DiscussionGroup]:
        """
        :return: a list of all the announcements found in the database
        """
        return DiscussionGroup.query.all()

    @staticmethod
    def get_discussion_group_for_id(discussion_group_id) -> DiscussionGroup:
        """
        :return: the discussion group object corresponding to {discussion_group_id}
        """
        return DiscussionGroup.query.filter(DiscussionGroup.id == discussion_group_id).first()

    @staticmethod
    def add_new_discussion_group(group):
        try:
            db.session.add(group)
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
