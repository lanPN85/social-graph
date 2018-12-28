import networkx as nx


def save_clusters(clusters, path):
    with open(path, 'wt') as f:
        for i, cl in enumerate(clusters):
            f.write('Cluster %d\n' % i)
            for node in cl:
                f.write('%s\n' % str(node))
            f.write('\n')


def save_edges(graph: nx.Graph, path):
    with open(path, 'wt') as f:
        for u, v in graph.edges():
            f.write('%s %s\n' % (str(u), str(v)))
