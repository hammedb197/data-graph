
import textract


from .get_title import get_title
from .preprocess import preprocess
from .nlp import sentiment, ner
from .save_to_db import sendToNeo4j




'''
EXTRACT FROM doc
'''    
def extract_text_from_doc(file):
    content = textract.process(file)
    doc_ = preprocess(content) #content
    title = get_title(doc_) #title
    sentiment_ = sentiment(doc_) #sentiment model
    ner_ = ner(doc_) #named entity recognition
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
    #save to db after extraction
    sendToNeo4j(location=location, sentiment_=sentiment_, content=content, title=title, organization=organization, person=person)


