
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
    text_file = open(file, 'rb') #open file
    pypdf_read = PyPDF2.PdfFileReader(text_file) #pdf reader
    n_of_pages = pypdf_read.numPages #get page number
    title = pypdf_read.getDocumentInfo().title #get title
    current_page = 0
    content = ''
    #loop through pages
    while (current_page < n_of_pages):
        get_page = pypdf_read.getPage(current_page) 
        current_page += 1
        content += get_page.extractText() #extract content
        #considtion if no text was extracted use 'textract'
    if len(content) == 0:
        content = textract.process(file, method='pdftotext')# process pdf to text
    pdf_ = preprocess(content)
    if title == None: #check
        title = get_title(pdf_) #title
    sentiment_ = sentiment(pdf_) #sentiment model
    ner_ = ner(pdf_) #named entity recognition model
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
    #save to db
    sendToNeo4j(location=location, sentiment_=sentiment_, content=content, title=title, organization=organization, person=person)
