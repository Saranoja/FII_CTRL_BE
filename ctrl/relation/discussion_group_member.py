from sqlalchemy import Integer
from database_connection import db


class DiscussionGroupMember(db.Model):
    __tablename__ = "DiscussionGroupsMembers"
    id = db.Column("id", Integer, primary_key=True)
    user_id = db.Column("user_id", Integer, nullable=False, unique=True)
    discussion_group_id = db.Column("discussion_group_id", Integer, nullable=False, unique=True)
