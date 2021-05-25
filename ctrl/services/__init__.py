from services.sanity import SanityCheck
from services.users_service import UsersService, CurrentUser, Teaching, TeachersService, StudentsService
from services.auth import Login, TokenRefresh, Logout
from services.recommend_me import PdfBooksController, KeywordsBooksController, KeywordsArticlesController, \
    PdfArticlesController
from services.announcements_service import DiscussionGroupsController, AnnouncementsController
from services.profile_service import ProfileController
from services.groups_members_controller import GroupsMembersController
from services.groups_service import GroupsController
from services.file_storage import FilesManager

all = [SanityCheck, UsersService, CurrentUser, Teaching, Login, TokenRefresh, Logout, PdfBooksController,
       KeywordsBooksController, KeywordsArticlesController, PdfArticlesController, DiscussionGroupsController,
       AnnouncementsController, ProfileController, TeachersService, StudentsService, GroupsMembersController,
       GroupsController, FilesManager]
