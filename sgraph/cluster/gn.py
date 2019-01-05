from networkx.algorithms.community.centrality import girvan_newman as gn
import itertools

def girvan_newman(g, partitions=2):
    comp = gn(g)
    clusters = list(itertools.takewhile(lambda c: len(c) <= partitions, comp))[-1]
    return list(list(sorted(c)) for c in clusters)