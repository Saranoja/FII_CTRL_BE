import logging
import pdfminer
import requests
from flask_restful import Resource
from flask import make_response, jsonify, request
from services.auth.token_config import token_required
from pdfminer.high_level import extract_text
from repository import ReferencesRepository, ArticlesRepository
from model import Reference, Article
from services.recommend_me.helpers import *
import io
import xxhash
import json

arxiv_api_url = "http://export.arxiv.org/api/query?max_results=10&search_query=ti:"


class PdfBooksController(Resource):
    @staticmethod
    @token_required
    def post(current_user):
        subject_id = request.path.split('/')[2]
        try:
            pdf_file = io.BytesIO(request.get_data())
            pdf_text = extract_text(pdf_file, maxpages=100)
        except pdfminer.pdfparser.PDFSyntaxError:
            return make_response(jsonify({'message': 'File must be a PDF'}), 400)

        hashed_pdf = xxhash.xxh3_64(pdf_text.encode('utf-8')).hexdigest()

        already_processed_file = ReferencesRepository.does_resource_exist(hashed_pdf)

        if already_processed_file:
            logging.info("File present in references cache")
            return make_response(jsonify({'message': already_processed_file.references}), 200)
        else:
            keyphrases_rank = keywords_retriever.get_keyphrases_rank(pdf_text)
            expanded_keyphrases_rank = keywords_retriever.expand_keyphrases_dict(keyphrases_rank)
            books = books_mappings.get_books_from_subject(subject_id)
            retriever = SuggestionRetriever(books, expanded_keyphrases_rank)
            top_reads = retriever.get_top_suggestions()
            new_reference = Reference(hash=hashed_pdf, name=subject_id, references=top_reads)
            ReferencesRepository.add_new_resource(new_reference)
            return make_response(jsonify({'message': top_reads}), 200)


class KeywordsBooksController(Resource):
    @staticmethod
    @token_required
    def post(current_user):
        subject_id = request.path.split('/')[2]

        keyphrases_rank = request.get_json()

        hashed_json = xxhash.xxh3_64(json.dumps(keyphrases_rank).encode('utf-8')).hexdigest()

        already_processed_keywords_set = ReferencesRepository.does_resource_exist(hashed_json)

        if already_processed_keywords_set:
            logging.info("Keywords set present in references cache")
            return make_response(jsonify({'message': already_processed_keywords_set.references}), 200)
        else:
            expanded_keyphrases_rank = keywords_retriever.expand_keyphrases_dict(keyphrases_rank)
            books = books_mappings.get_books_from_subject(subject_id)
            retriever = SuggestionRetriever(books, expanded_keyphrases_rank)
            top_reads = retriever.get_top_suggestions()
            new_reference = Reference(hash=hashed_json, name=subject_id, references=top_reads)
            ReferencesRepository.add_new_resource(new_reference)
            return make_response(jsonify({'message': top_reads}), 200)


class PdfArticlesController(Resource):
    @staticmethod
    @token_required
    def post(current_user):
        try:
            pdf_file = io.BytesIO(request.get_data())
            pdf_text = extract_text(pdf_file, maxpages=100)
        except pdfminer.pdfparser.PDFSyntaxError:
            return make_response(jsonify({'message': 'File must be a PDF'}), 400)

        hashed_json = xxhash.xxh3_64(json.dumps(pdf_text).encode('utf-8')).hexdigest()

        already_processed_keywords_set = ArticlesRepository.does_resource_exist(hashed_json)

        if already_processed_keywords_set:
            logging.info("Keywords set present in articles cache")
            return make_response(
                jsonify({'message': list(map(lambda x: x.reference, already_processed_keywords_set))}), 200)
        else:
            keyphrases_rank = keywords_retriever.get_keyphrases_rank(pdf_text)
            response_list = []

            for keyphrase in keyphrases_rank:
                # encode spaces
                keyphrase: str = keyphrase.replace(' ', '%20')
                # exact keyphrase search
                keyphrase = f'"{keyphrase}"'

                xml_string = requests.get(arxiv_api_url + keyphrase).text
                parsed_response = parse_response(xml_string)
                if parsed_response:
                    response_list.extend(parse_response(xml_string))

            articles = []
            for article in response_list:
                if article not in articles:
                    articles.append(article)

            for article in articles:
                new_reference = Article(hash=hashed_json, reference=article)
                ArticlesRepository.add_new_resource(new_reference)
            return make_response(jsonify({'message': articles}), 200)


class KeywordsArticlesController(Resource):
    @staticmethod
    @token_required
    def post(current_user):
        keyphrases_rank = request.get_json()

        if not keyphrases_rank:
            return make_response(jsonify({'message': 'A JSON must be provided'}), 400)

        hashed_json = xxhash.xxh3_64(json.dumps(keyphrases_rank).encode('utf-8')).hexdigest()

        already_processed_keywords_set = ArticlesRepository.does_resource_exist(hashed_json)

        if already_processed_keywords_set:
            logging.info("Keywords set present in articles cache")
            return make_response(jsonify({'message': list(map(lambda x: x.reference, already_processed_keywords_set))}), 200)
        else:
            response_list = []

            for keyphrase in keyphrases_rank:
                # encode spaces
                keyphrase: str = keyphrase.replace(' ', '%20')
                # exact keyphrase search
                keyphrase = f'"{keyphrase}"'

                xml_string = requests.get(arxiv_api_url + keyphrase).text
                parsed_response = parse_response(xml_string)
                if parsed_response:
                    response_list.extend(parse_response(xml_string))

            articles = []
            for article in response_list:
                if article not in articles:
                    articles.append(article)

            for article in articles:
                new_reference = Article(hash=hashed_json, reference=article)
                ArticlesRepository.add_new_resource(new_reference)
            return make_response(jsonify({'message': articles}), 200)
