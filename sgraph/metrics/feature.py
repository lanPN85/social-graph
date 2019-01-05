import networkx as nx


def feat_histogram(graph: nx.Graph, featnames):
    hist = {}
    for fn in featnames:
        d = nx.get_node_attributes(graph, fn)
        freq = sum(d.values())
        hist[fn] = freq
    
    return hist


def top_k_feats(graph, featnames, k=5):
    hist = feat_histogram(graph, featnames)
    lh = list(hist.items())
    lh = sorted(lh, key=lambda x: x[1], reverse=True)
    return lh[:k]
