import cv2
import pytesseract
import imutils
import numpy as np
import textract


from .preprocess import preprocess
from .nlp import sentiment, ner
from .save_to_db import sendToNeo4j
from .get_title import get_title

'''
EXTRACT FROM IMAGE
'''

# custom_config = r'--oem 3 --psm 6'

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
        [x, y, w, h] = cv2.boundingRect(c)
        if h > average_ * 2:
            cv2.drawContours(mask, [c], -1, 0, -1)
            
    title = pytesseract.image_to_string(mask)#title
    content = pytesseract.image_to_string(img)#extracted content
    # conditions
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
      # save to db
    sendToNeo4j(location=location, sentiment_=sentiment_, content=content, title=title, organization=organization, person=person)
    
    
        
   