# steps:
# 1. Remove punctuations
# 2. Break by space
# 3. Count occurrence
# 4. Remove stop words
# 5. Remove commonly used words in reviews
# 6. Statistically find words using TF-IDF

import json
import re
import math

# load data
documents = []
with open("./yelp_academic_500-head-sample.json", "r") as f:
    for text in f:
        jsonText = json.loads(text)
        realText = jsonText['text']
        documents.append(realText)


def cleanText(document: str, word_count: list, word_list: dict) -> list:
    '''
    this function allows to leverage memory to overcome calculation time
    side effect on word_count and word_list
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

    # get and count words
    words = {}
    silent = []
    for w in document_as_list:
        # get word from document
        if w not in silent:
            if w not in word_list.keys():
                word_list[w] = 1
            else:
                word_list[w] += 1
            silent.append(w)
        # count word in document
        words[w] = 1 if w not in words.keys() else (words[w] + 1)
    word_count.append(words)

    return document_as_list


words = {}
word_counts = []
documents = [cleanText(d, word_counts, words) for d in documents]

# statistic calculation
D = len(documents)

# the (m * n) matrix with m is number of word and n is number of doc
TF_IDF = []

for widx, word in enumerate(words.keys()):
    W_TF_IDF = []
    IDF = math.log(D / words[word])
    for didx, doc in enumerate(documents):
        TF = word_counts[didx]
        # case empty word in document
        TF = 0 if word not in TF.keys() else TF[word]
        W_TF_IDF.append(IDF * TF)
    TF_IDF.append(W_TF_IDF)

# NOTE: this is a sparse matrix
print(TF_IDF)
