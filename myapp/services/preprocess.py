import re
from nltk.corpus import stopwords


stopwords = set(stopwords.words('english'))

"""
Preprocess text using regex
"""
def preprocess(data):
    if type(data) == bytes:
        data = data.decode('utf-8')
    clean_text = re.sub("(@)|(http[:/.A-Za-z0-9]+)|(RT)|(#)|(\W)|([0-9])", " ", data)

    clean_text = [i for i in clean_text.split() if i not in stopwords and len(i) > 2]
    clean_text_ = ' '.join(clean_text)
    return clean_text_