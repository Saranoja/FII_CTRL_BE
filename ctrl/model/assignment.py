from sqlalchemy import DateTime, String, Integer
from database_connection import db


class Assignment(db.Model):
    __tablename__ = "Assignments"
    id = db.Column("id", Integer, primary_key=True, autoincrement=True)
    title = db.Column("title", String, nullable=False)
    description = db.Column("description", String, nullable=False)
    deadline = db.Column("deadline", DateTime, nullable=False)
    author_id = db.Column("author_id", Integer, nullable=False)
    created_at = db.Column("created_at", DateTime, nullable=False)
    discussion_group_id = db.Column("discussion_group_id", Integer, nullable=False)
    file_url = db.Column("file_url", String, nullable=True)
    subject_id = db.Column("subject_id", Integer, nullable=False)
