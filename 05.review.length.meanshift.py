import typing

from lib import load_docs_from_file, Point, BaseCluster

## CONFIGURE MAGIC NUMBER ##
# BANDWIDTH
BAND = 300  # magic number

# CONVERGE CRITICAL
CON = 50  # magic number
#########################


class MsPoint(Point):
    '''
    Extension of Point class supports Mean Shift algorithm
    '''
    def __init__(self, values):
        super().__init__(values)
        self.mode = []
        # mode hold 2 steps mode of point
        # 0 position is newest and 1 is old mode
        self.mode.append(values)
        self.mode.append(values)

    def shiftMode(self, point_list: list, kernel: typing.Callable) -> None:
        '''
        update point mode by point list and kernel passed in function
        '''
        self.mode[1] = self.mode[0]
        point_sum = 0
        kernel_sum = 0
        for point in point_list:
            kernel_rst = kernel(abs(self.mode[0] - point.v))
            point_sum += point.v * kernel_rst
            kernel_sum += kernel_rst
        if kernel_sum > 0:
            self.mode[0] = point_sum / kernel_sum

    def moved_length(self):
        '''
        return moved mode comparing to old mode position
        '''
        return abs(self.mode[0] - self.mode[1])

    def __str__(self):
        return f"Point(v={self.v}, mode={self.mode})"


class MsCluster(BaseCluster):
    '''
    Extension of base cluster supports Mean Shift algorithm
    '''
    def __init__(self, centroid: float):
        super().__init__()
        self.centroid = centroid

    def collect_point(self, point_list: list):
        '''
        get all point have same mode in point list and add to cluster
        '''
        for point in point_list:
            if point.mode[0] == self.centroid:
                self.add(point)

    def __eq__(self, other):
        '''
        comparing myself to other MsCluster
        '''
        return (self.centroid == other.centroid)

    def display(self):
        '''
        display cluster info
        '''
        def extra():
            print("centroid: ", self.centroid)

        super().display("Mean Shift", extra)

    def __repr__(self):
        print()
        self.display()
        return super().__repr__()


class MeanShift():
    '''
    class implementing mean shift algorithm
    '''
    def __init__(self, point_list: typing.List[MsPoint],
                 kernel: typing.Callable, con: float):
        '''
        initialize mean shift with configuration parameters

        Parameters
        ----------
        point_list: list
            List of MsPoint in map
        kernel: typing.Callable
            function used to calculate density of area
        con: float
            convergent critical for mode moving length
        '''
        self.point_list = point_list
        self.kernel = kernel
        self.con = con
        self.clusters = []

    def run(self):
        for point in self.point_list:
            while True:
                point.shiftMode(self.point_list, self.kernel)
                if point.moved_length() <= self.con:
                    break
        for point in self.point_list:
            cluster = MsCluster(point.mode[0])
            if not (cluster in self.clusters):
                self.clusters.append(cluster)
                cluster.collect_point(self.point_list)


# kernel function
def kernel_func(length):
    return 1 if length <= BAND else 0


if __name__ == "__main__":
    docs = load_docs_from_file(
        "./yelp_academic_500-head-sample.json",
        "text",
        count=10,
    )
    points = [MsPoint(len(doc)) for doc in docs]
    mean_shift = MeanShift(points, kernel_func, CON)
    mean_shift.run()

    print("## RESULT ##")
    print(mean_shift.clusters)
