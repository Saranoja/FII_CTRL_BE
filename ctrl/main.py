from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import *
from config import JWT_SECRET_KEY
from flask_restful import Api
from services import *
from routes import ROUTES
from database_connection import db
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = JWT_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}'

api = Api(app)
jwt = JWTManager(app)
cors = CORS(app)
db.init_app(app)


# Generating tables before first request is fetched
@app.before_first_request
def create_tables():
    db.create_all()
    db.session.commit()


api.add_resource(SanityCheck, ROUTES['sanity'])
api.add_resource(UsersService, ROUTES['users'])
api.add_resource(Login, ROUTES['login'])
api.add_resource(CurrentUser, ROUTES['current_user'])
api.add_resource(Teaching, ROUTES['teaching'])
api.add_resource(TokenRefresh, ROUTES['refresh'])
api.add_resource(PdfBooksController, ROUTES['resources'])
api.add_resource(KeywordsBooksController, ROUTES['resources-keywords'])
api.add_resource(PdfArticlesController, ROUTES['articles'])
api.add_resource(KeywordsArticlesController, ROUTES['articles-keywords'])

if __name__ == '__main__':
    app.run()
