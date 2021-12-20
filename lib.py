import json
import typing


def load_docs_from_file(filename, key, count=None):
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


# Graph class
class Point:
    def __init__(self, values):
        self.v = values

    def dist(self, point) -> int:
        '''
        compute Euclidean distance to another Point
        '''
        return abs(point.v - self.v)

    def __add__(self, other):
        '''
        add my value with other Point value
        '''
        return Point(self.v + other.v)

    def __str__(self):
        return f"Point(v={self.v})"

    def __repr__(self):
        return self.__str__()


class BaseCluster:
    def __init__(self, data: list = []):
        self.els = []
        self.els += data

    def add(self, el):
        '''
        add new point into cluster
        '''
        self.els.append(el)

    def clear(self):
        '''
        clear all element in cluster
        '''
        self.els.clear()

    def display(self, cluster_name: str, extra_display: typing.Callable):
        print("---------")
        print(f"{cluster_name} info:")
        extra_display()
        print("elements list:")
        print(self.els)
        print("---------")
