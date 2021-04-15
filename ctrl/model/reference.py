from sqlalchemy import String,JSON
from database_connection import db


class Reference(db.Model):
    __tablename__ = "References"
    hash = db.Column("hash", String, primary_key=True)
    name = db.Column("id", String, nullable=False)
    references = db.Column("references", JSON, nullable=False)
