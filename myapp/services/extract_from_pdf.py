
import PyPDF2
import re
import textract


from .preprocess import preprocess
from .nlp import sentiment, ner
from .save_to_db import sendToNeo4j
from .get_title import get_title


'''
EXTRACT FROM pdf
'''

def extract_text_from_pdf(file):
    text_file = open(file, 'rb')
    pypdf_read = PyPDF2.PdfFileReader(text_file)
    n_of_pages = pypdf_read.numPages
    title = pypdf_read.getDocumentInfo().title
    current_page = 0
    content = ''
    while (current_page < n_of_pages):
        get_page = pypdf_read.getPage(current_page)
        current_page += 1
        content += get_page.extractText()
    if len(content) == 0:
        content = textract.process(file, method='pdftotext')
    pdf_ = preprocess(content)
    if title == None: #check
        title = get_title(pdf_)
    sentiment_ = sentiment(pdf_)
    ner_ = ner(pdf_)
    person = []
    location = []
    organization = []
    for x in ner_:
        if x.label_ == 'PERSON':
            person.append({x.label_:x.text})
        if x.label_ == 'ORG':
            organization.append({x.label_:x.text})
        if x.label_ == 'GPE':
            location.append({x.label_:x.text})
    sendToNeo4j(location=location, sentiment_=sentiment_, content=content, title=title, organization=organization, person=person)
