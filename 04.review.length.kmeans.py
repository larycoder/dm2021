from random import random
from typing import List

import lib
from lib import BaseCluster, Point


# inspect tool
def print_cluster(clusters: list):
    # display result
    print("Kmean result:\n")
    for cluster in clusters:
        cluster.display()
        print("\n")


# load data
docs = lib.load_docs_from_file(
    "./yelp_academic_500-head-sample.json",
    "text",
    count=50,  # number of sample with maximum is 500
)
data = [len(doc) for doc in docs]


# implement kmeans
class KmeanCluster(BaseCluster):
    def __init__(self, value_len: int, centroid: Point = None):
        '''
        initialize a cluster object supporting kmean algorithm

        Parameters
        ----------
        value_len: int
            maximum length of point value in Point list
            which is used to decide random initial centroid
            if centroid is not assigned
        centroid: Point
            centroid point of cluster. If centroid is not
            passed, a random one will be assigned
        '''
        super().__init__()
        self.centroid = Point(0)
        self.old_centroid = Point(0)
        if centroid:
            self.centroid = centroid
        else:
            self.centroid = Point(int(random() * value_len))

    def dist(self, point: Point):
        '''
        compute Euclidean distance from point to cluster centroid
        '''
        return self.centroid.dist(point)

    def update_centroid(self):
        '''
        update to new centroid which is mean of all elements
        '''
        total = Point(0)
        for i in self.els:
            total += i
        self.old_centroid.v = self.centroid.v
        if len(self.els) > 0:
            self.centroid.v = int(total.v / len(self.els))

    def is_moved(self):
        '''
        comparing current centroid position to its old position
        '''
        return not (self.centroid.v == self.old_centroid.v)

    def display(self):
        print("---------")
        print("Kmean cluster info:")
        print("Centroid: ", self.centroid)
        print("Elements list:")
        print(self.els)
        print("---------")


class Kmean:
    def __init__(self, clusters: List[KmeanCluster], data: List[Point]):
        self.clusters = clusters
        self.data = data

    def update_cluster(self):
        '''
        add points to cluster
        '''
        for point in self.data:
            dist = []
            for cluster in self.clusters:
                dist.append({
                    "cluster": cluster,
                    "distance": cluster.dist(point)
                })
            cluster = min(dist, key=lambda ip: ip["distance"])["cluster"]
            cluster.add(point)

    def update_cluster_centroid(self):
        '''
        re-update clusters following point data
        '''
        # update point in each cluster
        self.update_cluster()

        # update cluster centroid by its point
        for cluster in self.clusters:
            cluster.update_centroid()

        # clear point in cluster
        for cluster in self.clusters:
            cluster.clear()

    def run(self):
        '''
        loop update centroid until nothing move
        '''
        while True:
            self.update_cluster_centroid()
            if all(not cluster.is_moved() for cluster in self.clusters):
                break


if __name__ == "__main__":
    p_data = [Point(d) for d in data]
    p_max_len = max(data)
    clusters = [KmeanCluster(p_max_len) for i in range(3)]
    kmean = Kmean(clusters, p_data)
    kmean.run()
    kmean.update_cluster()
    print_cluster(clusters)
