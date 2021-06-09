from sqlalchemy import Integer, DateTime, String, Boolean, Interval
from database_connection import db


class Meeting(db.Model):
    __tablename__ = "Meetings"
    id = db.Column("id", Integer, primary_key=True, autoincrement=True)
    title = db.Column("title", String, nullable=False)
    url = db.Column("url", String, nullable=False)
    timestamp = db.Column("timestamp", DateTime, nullable=False)
    recurrent = db.Column("recurrent", Boolean, nullable=False)
    recurrence_interval = db.Column("recurrence_interval", Interval, nullable=False)
    group_id = db.Column("group_id", Integer, nullable=False)
    author_id = db.Column("author_id", Integer, nullable=False)