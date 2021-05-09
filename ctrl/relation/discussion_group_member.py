from sqlalchemy import Integer
from database_connection import db


class DiscussionGroupMember(db.Model):
    __tablename__ = "DiscussionGroupsMembers"
    user_id = db.Column("user_id", Integer, primary_key=True)
    discussion_group_id = db.Column("discussion_group_id", Integer, primary_key=True)
