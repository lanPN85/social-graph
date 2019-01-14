from networkx.algorithms.community.quality import performance as pf, coverage as cv
from networkx import DiGraph

# The performance of a partition is the ratio of the number of intra-community edges plus inter-community non-edges with the total number of potential edges.
def performance(g: DiGraph, partition):
    return pf(g,partition)


def coverage(g: DiGraph, partition):
    return cv(g, partition)
