from services.sanity import SanityCheck
from services.users_service import UsersService, CurrentUser, Teaching, TeachersService, StudentsService
from services.auth import Login, TokenRefresh, Logout
from services.recommend_me import PdfBooksController, KeywordsBooksController, KeywordsArticlesController, \
    PdfArticlesController
from services.announcements_service import AnnouncementsController
from services.groups_service import GroupsController
from services.profile_service import ProfileController
from services.groups_members_controller import GroupsMembersController
from services.groups_service import GroupsController
from services.file_storage import FilesManager
from services.assignments_service import AssignmentsController
from services.meetings_service import MeetingsController

all = [SanityCheck, UsersService, CurrentUser, Teaching, Login, TokenRefresh, Logout, PdfBooksController,
       KeywordsBooksController, KeywordsArticlesController, PdfArticlesController,
       AnnouncementsController, ProfileController, TeachersService, StudentsService, GroupsMembersController,
       GroupsController, FilesManager, AssignmentsController, MeetingsController]
