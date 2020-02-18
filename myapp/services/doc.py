
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


