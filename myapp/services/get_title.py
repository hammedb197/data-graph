from .preprocess import preprocess
from collections import Counter 


def get_title(data):
    hold_data = preprocess(data)
    split_data = hold_data.split()
    if len(split_data) == 0:
        title = hold_data[0:250]
    else:
        counter = Counter(split_data)
        title = counter.most_common(1)[0][0]
    
    return title