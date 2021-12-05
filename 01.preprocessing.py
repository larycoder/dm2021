# steps:
# 1. Remove punctuations
# 2. Break by space
# 3. Count occurrence
# 4. Remove stop words
# 5. Remove commonly used words in reviews
# 6. Statistically find words using TF-IDF

import json
import re

# load data
documents = []
with open("./yelp_academic_500-head-sample.json", "r") as f:
    for text in f:
        jsonText = json.loads(text)
        realText = jsonText['text']
        documents.append(realText)


def cleanText(document: str, word_count: list) -> list:
    '''
    this function allows to leverage memory to overcome calculation time
    side effect on word_count
    '''

    # define list
    list_stop_word = ['in', 'of', 'the', 'at']
    list_common_words = ['like', 'get', 'to']

    # remove punctuations
    document = re.sub(r'[^\w\s]', '', document)

    # lower document
    document = document.lower()

    # document as list
    document_as_list = document.split()

    # remove stop and common words
    document_as_list = [
        w for w in document_as_list
        if w not in (list_stop_word + list_common_words)
    ]

    # count words
    words = {}
    for w in document_as_list:
        words[w] = 1 if w not in words.keys() else (words[w] + 1)
    word_count.append(words)

    return document_as_list


words = []
documents = [cleanText(d, words) for d in documents]

# statistic calculation
print(words[0])
