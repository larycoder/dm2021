import json


def load_docs_from_file(filename, key, count = None):
    documents = []
    with open(filename, "r") as f:
        idx = 0
        for text in f:
            jsonText = json.loads(text)
            realText = jsonText[key]
            documents.append(realText)
            if count and idx >= count:
                break
            idx += 1
    return documents
