import networkx as nx

from tqdm import tqdm
from logzero import logger


def load_raw_graph(path, verbose=True):
    g = nx.DiGraph()

    with open(path, 'rt') as f:
        if verbose:
            f = tqdm(f, desc='Loading graph from %s' % path)
        for line in f:
            line = line.strip()
            id1, id2 = line.split(' ')
            g.add_edge(int(id1), int(id2))
    
    return g


def add_node_feats(graph, feat_path, feat_name_path, verbose=True):
    feat_names = []
    with open(feat_name_path, 'rt') as f:
        if verbose:
            logger.info('Reading feature names from %s' % feat_name_path)
        for line in f:
            line = line.strip()
            feat = line.split(' ')[-1]
            feat_names.append(feat)
        
    with open(feat_path, 'rt') as f:
        if verbose:
            f = tqdm(f, 'Loading features from %s' % feat_path)
        for line in f:
            line = line.strip()
            comps = line.split(' ')
            uid = int(comps[0])

            for i, c in enumerate(comps[1:]):
                if graph.has_node(uid):
                    graph.nodes[uid][feat_names[i]] = int(c)
                else:
                    logger.warning('Node %d not found')
                
    return feat_names
