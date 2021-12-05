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
    text = f.readline();
    jsonText = json.loads(text)
    realText = jsonText['text']
    data.append(realText)

# remove break space
data = ' '.join(data)
data = [t.lower() for t in data.split()]

# remove punctuations
import re
data = [re.sub(r'[^\w\s]','',s) for s in data]

# remove stop words

print(data)
