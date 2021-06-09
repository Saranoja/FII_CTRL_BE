from repository.users_repository import UsersRepository
from repository.references_repository import ReferencesRepository
from repository.articles_repository import ArticlesRepository
from repository.token_blacklist_repository import TokenBlacklistRepository
from repository.announcements_repository import AnnouncementsRepository
from repository.discussion_groups_repository import DiscussionGroupsRepository
from repository.discussion_group_member_repository import DiscussionGroupsMembersRepository
from repository.subjects_repository import SubjectsRepository
from repository.teacher_profile_details_repository import TeachersProfileDetailsRepository
from repository.teacher_subject_repository import TeachersSubjectsRepository
from repository.assignments_repository import AssignmentsRepository
from repository.meetings_repository import MeetingsRepository

__all__ = [UsersRepository, ReferencesRepository, ArticlesRepository, TokenBlacklistRepository, AnnouncementsRepository,
           DiscussionGroupsRepository, DiscussionGroupsMembersRepository, SubjectsRepository,
           TeachersProfileDetailsRepository, TeachersSubjectsRepository, AssignmentsRepository, MeetingsRepository]
