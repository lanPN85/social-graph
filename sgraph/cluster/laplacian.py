import numpy as np
import networkx as nx
import networkx.linalg.laplacianmatrix as lpm

from logzero import logger


def laplacian_cluster(g, partitions=8):
    nodes = list(g.nodes())
    if partitions < 2 or len(nodes) == 1:
        return [nodes]

    L = lpm.laplacian_matrix(g).todense()
    eig_vals, eig_vecs = np.linalg.eig(L)
    eig_vals = np.abs(eig_vals)
    s_idx = np.argsort(eig_vals)[:2]

    index = s_idx[-1]
    vec = eig_vecs[:, index]
    n1, n2 = [], []
    for i, v in enumerate(vec):
        if v < 0:
            n1.append(nodes[i])
        else:
            n2.append(nodes[i])
    g1 = g.subgraph(n1)
    g2 = g.subgraph(n2)
    out = []
    out.extend(laplacian_cluster(g1, partitions=partitions//2))
    out.extend(laplacian_cluster(g2, partitions=partitions//2))
    return out
