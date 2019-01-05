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
            
            if graph.has_node(uid):
                for i, c in enumerate(comps[1:]):
                    graph.nodes[uid][feat_names[i]] = int(c)
            else:
                logger.warning('Node %d not found' % uid)
                
    return feat_names


def load_clusters(path):
    clusters = []
    with open(path, 'rt') as f:
        cl = []
        for line in f:
            line = line.strip()
            if line == '':
                clusters.append(cl)
                cl = []
            elif not line.startswith('Cluster'):
                cl.append(int(line))
        if len(cl) > 0:
            clusters.append(cl)
    return clusters
