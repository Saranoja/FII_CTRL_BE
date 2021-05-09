from services.sanity import SanityCheck
from services.users_service import UsersService, CurrentUser, Teaching
from services.auth import Login, TokenRefresh, Logout
from services.recommend_me import PdfBooksController, KeywordsBooksController, KeywordsArticlesController, \
    PdfArticlesController
from services.announcements_service import DiscussionGroupsController, AnnouncementsController

all = [SanityCheck, UsersService, CurrentUser, Teaching, Login, TokenRefresh, Logout, PdfBooksController,
       KeywordsBooksController, KeywordsArticlesController, PdfArticlesController, DiscussionGroupsController,
       AnnouncementsController]
