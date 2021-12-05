# steps:
# 1. Remove punctuations
# 2. Break by space
# 3. Count occurrence
# 4. Remove stop words
# 5. Remove commonly used words in reviews
# 6. Statistically find words using TF-IDF

# load data
import json

data = []
with open("./yelp_academic_500-head-sample.json", "r") as f:
    for text in f:
        jsonText = json.loads(text)
        realText = jsonText['text']
        data.append(realText)

# remove break space
data = ' '.join(data)
data = [t.lower() for t in data.split()]

# remove punctuations
import re

data = [re.sub(r'[^\w\s]', '', s) for s in data]


# remove stop words
def removeStopWords(text):
    list_stop_word = ['in', 'of', 'the', 'at']
    if (len(text) < 2) or text in list_stop_word:
        return None
    return text


data = [removeStopWords(t) for t in data]
data = [t for t in data if t]

# remove commonly used words
list_common_words = ['like', 'get', 'to']
data = [t for t in data if t not in list_common_words]

# count word
data_counted = {}
for t in data:
    if t not in data_counted.keys():
        data_counted[t] = 1
    else:
        data_counted[t] += 1
print(data_counted)
