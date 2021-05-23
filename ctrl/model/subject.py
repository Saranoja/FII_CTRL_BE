from sqlalchemy import Integer, String, Boolean
from database_connection import db


class Subject(db.Model):
    __tablename__ = "Subjects"
    id = db.Column("id", Integer, primary_key=True)
    code = db.Column("code", String, nullable=False)
    name = db.Column("name", String, nullable=False)
