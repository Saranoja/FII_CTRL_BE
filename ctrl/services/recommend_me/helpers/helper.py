from PyPDF2 import PdfFileReader as reader

word = "planar graphs"
with open("../resources/books/Graph Theory by Reinhard Diestel.pdf", "rb") as pdf_file:
    pdf = reader(pdf_file)
    pages = pdf.getNumPages()
    print(f"Analyzing book...")
    print(f"Number of pages: {pages}")
    occurrences = 0

    for page_number in range(pages):
        page = pdf.getPage(page_number)
        page_text = page.extractText()
        occurrences += page_text.lower().count(word)
        if page_number % 20 == 19:
            print(f"Occurrences of {word} for page {page_number}: {occurrences}")
            occurrences = 0
