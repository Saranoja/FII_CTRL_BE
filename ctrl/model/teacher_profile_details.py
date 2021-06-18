from sqlalchemy import Integer, String
from database_connection import db


class TeacherProfileDetails(db.Model):
    __tablename__ = "TeachersProfileDetails"
    user_id = db.Column("user_id", Integer, primary_key=True)
    degree = db.Column("degree", String, nullable=True)
    secondary_email = db.Column("secondary_email", String, nullable=True)
    phone_number = db.Column("phone_number", String, nullable=True)
    office_number = db.Column("office_number", String, nullable=True)
    schedule_url = db.Column("schedule_url", String, nullable=True)
    interest_field = db.Column("interest_field", String, nullable=True)
    thesis_examples = db.Column("thesis_examples", String, nullable=True)
