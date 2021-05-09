from sqlalchemy import String, Integer, DateTime
from database_connection import db


class TokenBlacklist(db.Model):
    __tablename__ = "TokenBlacklist"
    id = db.Column("id", Integer, primary_key=True, autoincrement=True)
    jti = db.Column("jti", String(36), nullable=False)
    created_at = db.Column("created_at", DateTime, nullable=False)
