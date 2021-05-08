from services.sanity import SanityCheck
from services.users_service import UsersService, CurrentUser, Teaching
from services.auth import Login, TokenRefresh, Logout
from services.recommend_me import PdfBooksController, KeywordsBooksController, KeywordsArticlesController, \
    PdfArticlesController

all = [SanityCheck, UsersService, CurrentUser, Teaching, Login, TokenRefresh, Logout, PdfBooksController,
       KeywordsBooksController, KeywordsArticlesController, PdfArticlesController]
