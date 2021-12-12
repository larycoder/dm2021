from lib import *

# load data
docs = load_docs_from_file("./yelp_academic_5-head-sample.json", "text")
values = [len(doc) for doc in docs]
length = len(values)
len_matrix = [[] for i in range(length)]

# compute length matrix
for row in range(length):
    for col in range(length):
        d = abs(values[row] - values[col])
        len_matrix[row].append(d)


class HierarchicalCluster():
    # let each data be a cluster
    # loop
    #   calculate cluster distance
    #   merge 2 closest cluster
    #   if only single cluster then stop
    def __init__(self, values: list, len_matrix: list):
        self.values = values
        self.length = len(values)
        self.len_matrix = len_matrix

    def _init_cluster(self) -> list:
        return [[i] for i in range(self.length)]

    def _dist(self, c1, c2) -> int:
        d = -1
        if type(c1) == int and type(c2) == int:
            return self.len_matrix[c1][c2]
        elif type(c1) == int:
            c1 = [c1]
        elif type(c2) == int:
            c2 = [c2]

        for v1 in c1:
            for v2 in c2:
                d_temp = self._dist(v1, v2)
                d = d_temp if (d_temp < d or d < 0) else d
        return d

    def _get_closest_cluster(self, cluster: list):
        # c2 always higher than c1
        c1, c2, d = 0, 1, -1
        c_len = len(cluster)
        for i in range(c_len):
            for j in range(c_len):
                d_temp = self._dist(cluster[i], cluster[j])
                if i != j and (d < 0 or d_temp < d):
                    c1, c2, d_temp = i, j, d_temp
        # return right order
        if c2 < c1:
            return c2, c1
        return c1, c2

    def generate_cluster(self):
        cluster = self._init_cluster()
        while len(cluster) > 3:
            idx1, idx2 = self._get_closest_cluster(cluster)
            c2 = cluster.pop(idx2)
            c1 = cluster.pop(idx1)
            cluster.append([c1, c2])
        return cluster

cluster_builder = HierarchicalCluster(values, len_matrix)
result_cluster = cluster_builder.generate_cluster()
print(result_cluster)
