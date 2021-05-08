import re
import spacy
from statistics import mean

word_tokenizer = re.compile("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+")
with open("services/recommend_me/helpers/stopwords_english.txt", encoding="utf-8") as stopwords_file:
    stopwords_english = stopwords_file.read().split("\n")


def get_keyphrases_rank(text, no_of_keyphrases=20):
    # load a spaCy model, depending on language, scale, etc.
    nlp = spacy.load("en_core_web_sm")

    # add PyTextRank to the spaCy pipeline
    # tr = pytextrank.TextRank()
    nlp.add_pipe("textrank")

    doc = nlp(text)

    # examine the top k-ranked phrases in the document
    # keyword_sentences = [p.text for phrase_number, p in enumerate(doc._.phrases) if phrase_number < keywords_number]
    keyphrase_rank = {p.text.lower(): p.rank for phrase_index, p in enumerate(doc._.phrases) if
                      phrase_index < no_of_keyphrases}

    return keyphrase_rank


def expand_keyphrases_dict(keyphrases_rank: dict) -> dict:
    mean_rank = mean(keyphrases_rank.values())
    mean_rank -= 0.1 * mean_rank
    expanded_keyphrases_rank_set = keyphrases_rank.copy()

    for keyphrase in keyphrases_rank.keys():
        for keyword in word_tokenizer.findall(keyphrase):
            if keyword not in stopwords_english and keyword not in expanded_keyphrases_rank_set:
                expanded_keyphrases_rank_set[keyword] = mean_rank
        mean_rank -= 0.05 * mean_rank

    return expanded_keyphrases_rank_set
