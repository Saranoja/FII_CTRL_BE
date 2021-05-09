from relation import DiscussionGroupMember
from sqlalchemy import exc
from database_connection import db


class DiscussionGroupsMembersRepository:
    @staticmethod
    def get_discussion_groups_for_user(user_id):
        return DiscussionGroupMember.query.filter(DiscussionGroupMember.user_id == user_id).all()

    @staticmethod
    def add_new_member_to_group(user_id, group_id):
        new_member = DiscussionGroupMember(user_id=user_id, discussion_group_id=group_id)
        try:
            db.session.add(new_member)
            db.session.commit()
        except exc.SQLAlchemyError:
            db.session.rollback()
