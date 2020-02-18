import requests
import json
import sys


from .nlp import sentiment, ner
from .preprocess import preprocess
from .save_to_db import sendToNeo4j


headers = {
    # http://www.mediawiki.org/wiki/API:Main_page#Identifying_your_client
    "User-Agent": "Definitions/1.0 (Contact rob@example.com for info.)"
}

def get_wiki_data(q):
    
    params = {
    'action':'query',
    'prop':'extracts',
    'format':'json',
    'exintro':1,
    'explaintext':1,
    'generator':'search',
    'gsrsearch': str(q),
    'gsrlimit':1,
    'continue':''
}
    try:
        r = requests.get('http://en.wikipedia.org/w/api.php', params=params, headers=headers,)
        json = r.json()	
        if "query" in json:
            try:
                for i in json["query"]["pages"]:
                    content = json["query"]["pages"][i]['extract']
                    title = json["query"]["pages"][i]['title']
                    wiki_data = preprocess(content)
                    sentiment_ =  sentiment(wiki_data)
                    ner_ = ner(wiki_data)
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
            except requests.exceptions.NoneType as err:
                print(err)
    except Exception as err:
      print(err)
              


        
    
 
