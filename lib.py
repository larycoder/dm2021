import json


def load_docs_from_file(filename, key):
    documents = []
    with open(filename, "r") as f:
        for text in f:
            jsonText = json.loads(text)
            realText = jsonText[key]
            documents.append(realText)
    return documents
