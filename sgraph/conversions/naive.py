import networkx as nx


def naive_conversion(digraph, **kwargs):
    return nx.Graph(digraph)
