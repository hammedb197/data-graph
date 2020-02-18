import cv2
import pytesseract
import imutils

import PyPDF2

import re

import numpy as np

import textract

from collections import Counter 

from .preprocess import preprocess
from .nlp import sentiment, ner
from .save_to_db import sendToNeo4j


def get_title(data):
    hold_data = preprocess(data)
    split_data = hold_data.split()
    if len(split_data) == 0:
        title = hold_data[0:250]
    else:
        counter = Counter(split_data)
        title = counter.most_common(1)[0][0]
    
    return title
    



custom_config = r'--oem 3 --psm 6'

'''
EXTRACT FROM IMAGE
'''
def extract_from_images(file):
    img = cv2.imread(file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (_, binary) = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
     # convert2binary
    contours = cv2.findContours(~binary,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if imutils.is_cv4() else contours[1]
    heights = [cv2.boundingRect(contour)[3] for contour in contours]
    average_ = sum(heights)/len(heights)
  
    mask = np.ones(img.shape[:2], dtype="uint8") * 255 
    #create empty image of the size of the image
    for c in contours:
        [x,y,w,h] = cv2.boundingRect(c)
        if h > average_ * 2:
            cv2.drawContours(mask, [c], -1, 0, -1)
            
    title = pytesseract.image_to_string(mask)
    content = pytesseract.image_to_string(img)
    if len(content) == 0:
        content = textract.process(file)
    image = preprocess(content)
    if title == None:
      title = get_title(image)
    sentiment_ = sentiment(image)
    ner_ = ner(image)
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

'''
EXTRACT FROM doc
'''    
def extract_text_from_doc(file):
    content = textract.process(file)
    doc_ = preprocess(content)
    title = get_title(doc_)
    sentiment_ = sentiment(doc_)
    ner_ = ner(doc_)
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

