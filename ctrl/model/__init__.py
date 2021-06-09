from model.user import User
from model.reference import Reference
from model.article import Article
from model.token_blacklist import TokenBlacklist
from model.announcement import Announcement
from model.discussion_group import DiscussionGroup
from model.subject import Subject
from model.teacher_profile_details import TeacherProfileDetails
from database_connection import db
from model.assignment import Assignment
from model.meeting import Meeting

__all__ = [User, Reference, Article, TokenBlacklist, Announcement, DiscussionGroup, Subject, TeacherProfileDetails,
           Assignment, Meeting, db]
