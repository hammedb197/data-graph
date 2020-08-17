from allennlp.predictors.predictor import Predictor
from nltk.tokenize import word_tokenize
from nltk import pos_tag, ne_chunk
import re
import nltk

import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
from pprint import pprint

nlp = en_core_web_sm.load()

#sentiment analysis model; extracting just Positive and negative sentiment(allen nlp model)
def sentiment(wiki_data):
  predictor = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/sst-2-basic-classifier-glove-2019.06.27.tar.gz")
  predict  = predictor.predict(wiki_data)
  # print(predict)
  if predict['label'] == '1':
    label = 'Positive'
  elif predict['label'] == '0':
    label = 'Negative'
  return label

# named entity recognition model   (Spacy)
def ner(text):
    doc = nlp(text)
    return doc.ents
 
            
