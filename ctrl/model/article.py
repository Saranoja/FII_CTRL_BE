from sqlalchemy import String, JSON, Integer
from database_connection import db


class Article(db.Model):
    __tablename__ = "Articles"
    id = db.Column("id", Integer, primary_key=True)
    hash = db.Column("hash", String, nullable=False)
    reference = db.Column("reference", JSON, nullable=False)
