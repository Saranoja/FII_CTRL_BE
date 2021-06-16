import copy

from flask_restful import Resource
from flask import make_response, jsonify, request
from services.auth.token_config import token_required
import json


class BibliographyController(Resource):
    @staticmethod
    @token_required
    def post(current_user):
        subject = request.path.split('/')[2]
        book = request.get_json()

        with open('services/recommend_me/books.json', 'r+') as books_file:
            initial_books = json.loads(books_file.read())
            books_json = copy.deepcopy(initial_books)
            for dictionary in books_json:
                if subject.lower() in dictionary["subjects"]:
                    if book["hash"] not in list(map(lambda x: x["hash"], dictionary["books"])):
                        dictionary["books"].append(book)
            if not initial_books == books_json:
                books_file.seek(0)
                books_file.write(json.dumps(books_json))
                books_file.truncate()

        return make_response(jsonify({"message": "Resource posted successfully."}), 202)
