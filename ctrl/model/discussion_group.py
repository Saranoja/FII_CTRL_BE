from sqlalchemy import Integer, String
from database_connection import db


class DiscussionGroup(db.Model):
    __tablename__ = "DiscussionGroups"
    id = db.Column("id", Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", String, nullable=False)
