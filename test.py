from sgraph.cluster.gn import *
from sgraph.loader import *
from networkx.algorithms.community.quality import performance
g = load_raw_graph('./data/twitter/egos/12831.edges')
partitions = girvan_newman(g,4)
print(performance(g,partitions))