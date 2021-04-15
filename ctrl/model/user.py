from sqlalchemy import Integer, String, Boolean
from database_connection import db


class User(db.Model):
    __tablename__ = "Users"
    id = db.Column("id", Integer, primary_key=True)
    username = db.Column("email", String, nullable=False)
    password = db.Column("password", String, nullable=False)
    admin = db.Column("admin", Boolean, nullable=False)
    teaching = db.Column("teaching", Boolean, nullable=False)
    first_name = db.Column("first_name", String, nullable=False)
    last_name = db.Column("last_name", String, nullable=False)
    year = db.Column("_year", String, nullable=True)
    group = db.Column("_group", String, nullable=True)
