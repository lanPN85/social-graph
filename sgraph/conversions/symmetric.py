from logzero import logger

import networkx as nx
import numpy as np


def _graph_from_adjacency(adj, nodes):
    eps = 0

    g = nx.Graph()
    for i in range(adj.shape[0]):
        for j in range(i+1, adj.shape[0]):
            if adj[i, j] > eps:
                g.add_edge(nodes[i], nodes[j], weight=adj[i, j])
    
    return g


def transpose_symmetric_conversion(digraph, **kwargs):
    nodes = list(digraph.nodes())
    A = nx.linalg.graphmatrix.adjacency_matrix(digraph, nodelist=nodes).todense()
    nA = A + np.transpose(A)

    return _graph_from_adjacency(nA, nodes)


def random_walk_symmetric_conversion(digraph, **kwargs):
    nodes = list(digraph.nodes())
    A = nx.linalg.adjacency_matrix(digraph, nodelist=nodes).todense()
    D = np.multiply(np.dot(A, np.ones_like(A)), np.eye(A.shape[0]))
    P = np.dot(np.linalg.pinv(D), A)

    num_edges = digraph.number_of_edges()
    Pi = D / (2 * num_edges)
    nA = (np.dot(Pi, P) + np.dot(P.T, Pi)) / 2

    return _graph_from_adjacency(nA, nodes)


def biblio_symmetric_conversion(digraph, **kwargs):
    nodes = list(digraph.nodes())
    A = nx.linalg.adjacency_matrix(digraph, nodelist=nodes).todense()

    nA = np.dot(A, A.T) + np.dot(A.T, A)

    return _graph_from_adjacency(nA, nodes)
