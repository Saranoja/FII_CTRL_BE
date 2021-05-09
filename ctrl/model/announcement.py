from sqlalchemy import DateTime, String, Integer
from database_connection import db


class Announcement(db.Model):
    __tablename__ = "Announcements"
    id = db.Column("id", Integer, primary_key=True, autoincrement=True)
    title = db.Column("title", String, nullable=False)
    text = db.Column("text", String, nullable=False)
    author = db.Column("author", String, nullable=False)
    created_at = db.Column("created_at", DateTime, nullable=False)
    discussion_group_id = db.Column("discussion_group_id", Integer, nullable=False)
