from .preprocess import preprocess
from collections import Counter 

# extract title from document
def get_title(data):
    hold_data = preprocess(data)
    split_data = hold_data.split()
    if len(split_data) == 0:
        title = hold_data[0:250] #get first 250 letters
    else:
        counter = Counter(split_data)
        title = counter.most_common(1)[0][0] #find the most common word in article
    
    return title