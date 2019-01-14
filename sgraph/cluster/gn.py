from networkx.algorithms.community.centrality import girvan_newman as gn
import itertools
from networkx.algorithms.components import *

def girvan_newman(g, partitions=2):
    if number_weakly_connected_components(g) >= partitions:
        print("Number of partitions has to be greater than the number of components")
        exit(0)
    comp = gn(g)
    clusters = list(itertools.takewhile(lambda c: len(c) <= partitions, comp))[-1]
    return list(list(sorted(c)) for c in clusters)