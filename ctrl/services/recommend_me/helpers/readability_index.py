import pdfminer
from textstat import textstat
import requests
from pdfminer.high_level import extract_text
import io


def get_readability_score_from_link(link: str) -> float:
    pdf_content = requests.get(link).content
    pdf_file = io.BytesIO(pdf_content)
    try:
        pdf_text = extract_text(pdf_file)
    except pdfminer.pdfparser.PDFSyntaxError:
        return -1
    return textstat.flesch_reading_ease(pdf_text)