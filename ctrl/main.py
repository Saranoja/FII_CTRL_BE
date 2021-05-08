from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import *
from flask_restful import Api
from services import *
from repository import TokenBlacklistRepository
from routes import ROUTES
from database_connection import db
from dotenv import load_dotenv

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
api = Api(app)
jwt = JWTManager(app)
cors = CORS(app)
db.init_app(app)

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

if __name__ == '__main__':
    app.run()
