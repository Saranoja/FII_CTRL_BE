from sqlalchemy import Integer
from database_connection import db


class TeacherSubject(db.Model):
    __tablename__ = "TeachersSubjects"
    teacher_id = db.Column("teacher_id", Integer, primary_key=True)
    subject_id = db.Column("subject_id", Integer, primary_key=True)
