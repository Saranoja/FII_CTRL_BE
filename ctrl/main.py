from flask import Flask
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO, join_room, leave_room, send
from flask_cors import CORS
from config import *
from flask_restful import Api
from services import *
from routes import ROUTES
from database_connection import db
from dotenv import load_dotenv
from io_socket import AnnouncementsNamespace
import logging

logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)
load_dotenv()


def generate_connection_string():
    try:
        if os.environ['ENGINE'] == 'App_Engine':
            return f'postgresql://{PGUSER}:{PGPASSWORD}@/{PGDATABASE}?host=/cloudsql/{PGCONNECTION}'
    except KeyError:
        return f'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}'


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES

app.config['SQLALCHEMY_DATABASE_URI'] = generate_connection_string()
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}
api = Api(app)
jwt = JWTManager(app)
cors = CORS(app)
socketIO = SocketIO(app, cors_allowed_origins='*')
db.init_app(app)

socketIO.on_namespace(AnnouncementsNamespace(''))

api.add_resource(SanityCheck, ROUTES['sanity'])
api.add_resource(UsersService, ROUTES['users'])

api.add_resource(Login, ROUTES['login'])
api.add_resource(Logout, ROUTES['logout'])
api.add_resource(TokenRefresh, ROUTES['refresh'])

api.add_resource(CurrentUser, ROUTES['current_user'])
api.add_resource(Teaching, ROUTES['teaching'])
api.add_resource(PdfBooksController, ROUTES['resources'])
api.add_resource(KeywordsBooksController, ROUTES['resources-keywords'])
api.add_resource(PdfArticlesController, ROUTES['articles'])
api.add_resource(KeywordsArticlesController, ROUTES['articles-keywords'])

api.add_resource(DiscussionGroupsController, ROUTES['discussion-groups'])
api.add_resource(AnnouncementsController, ROUTES['announcements'])
api.add_resource(ProfileController, ROUTES['profile'])

api.add_resource(StudentsService, ROUTES['students'])
api.add_resource(TeachersService, ROUTES['teachers'])

api.add_resource(GroupsMembersController, ROUTES['groups_members'])
api.add_resource(GroupsController, ROUTES['groups'])

api.add_resource(FilesManager, ROUTES['files'])

if __name__ == '__main__':
    socketIO.run(app)
