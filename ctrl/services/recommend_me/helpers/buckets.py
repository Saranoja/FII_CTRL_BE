from PyPDF2 import PdfFileReader as reader
from collections import OrderedDict


class SuggestionRetriever:
    def __init__(self, book_names, word_rank):
        self.book_names = book_names
        self.word_rank = word_rank
        self.keyphrases = list(word_rank.keys())

    def get_top_suggestions(self):
        chapters = {}
        for book in self.book_names:
            pdf_file_path = f'services/recommend_me/resources/books/{book}.pdf'
            buckets_with_word_cluster = self._create_buckets(pdf_file_path)
            buckets_with_score = {bucket: self._get_bucket_score(word_cluster)
                                  for bucket, word_cluster in buckets_with_word_cluster.items()}
            list_buckets_with_score_sorted = sorted(buckets_with_score.items(), key=lambda item: item[1], reverse=True)
            no_of_buckets = 3
            if int(len(list_buckets_with_score_sorted) * 0.05) >= 3:
                no_of_buckets = int(len(list_buckets_with_score_sorted) * 0.05)

            top_buckets = OrderedDict(list_buckets_with_score_sorted[0:no_of_buckets])
            chapters[book] = top_buckets
        return chapters

    def _get_bucket_score(self, bucket_words):
        score = 0
        for word in bucket_words:
            score += self.word_rank[word]
        return score

    def _create_buckets(self, pdf_file_path: str):
        buckets = {}
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_reader = reader(pdf_file)
            pages = pdf_reader.getNumPages()
            print(f"Analyzing book: {pdf_file_path} ...")
            print(f"Number of pages: {pages}")

            first_page_of_cluster = 10

            word_cluster = []
            no_of_empty_pages = 0
            for page_number in range(10, pages - 50):
                page_text: str = pdf_reader.getPage(page_number).extractText().lower()
                page_number += 1  # make page_number correspond to page from PDF viewer

                is_page_empty = True
                no_of_words_on_current_page = 0
                for keyword in self.keyphrases:
                    if keyword in page_text:
                        no_of_words_on_current_page += 1
                        no_of_empty_pages = 0
                        if len(word_cluster) == 0:
                            first_page_of_cluster = page_number
                        for i in range(page_text.count(keyword)):
                            word_cluster.append(keyword)

                if no_of_words_on_current_page > int(len(self.keyphrases) * 0.13):
                    is_page_empty = False

                if is_page_empty:
                    no_of_empty_pages += 1

                if no_of_empty_pages == 1:
                    last_page_of_cluster = page_number
                    if first_page_of_cluster < last_page_of_cluster:
                        buckets[f"{first_page_of_cluster}-{last_page_of_cluster}"] = word_cluster
                    word_cluster = []
        return buckets
