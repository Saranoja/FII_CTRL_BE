from sqlalchemy import String,JSON
from database_connection import db


class Article(db.Model):
    __tablename__ = "Articles"
    hash = db.Column("hash", String, primary_key=True)
    reference = db.Column("reference", JSON, nullable=False)
