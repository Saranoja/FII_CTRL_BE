import json
from typing import List


def get_books_from_subject(subject: str) -> List[str]:
    with open('services/recommend_me/books.json') as books_file:
        books_json = json.loads(books_file.read())
        for dictionary in books_json:
            if subject.lower() in dictionary["subjects"]:
                return dictionary["books"]
        return []
