from services.users_service.users_service import UsersService
from services.users_service.current_user import CurrentUser
from services.users_service.teaching import Teaching
from services.users_service.teachers_service import TeachersService
from services.users_service.students_service import StudentsService

all = [UsersService, CurrentUser, Teaching, TeachersService, StudentsService]
