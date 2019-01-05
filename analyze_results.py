#!/usr/bin/env python3

import os
import logzero
import json
import networkx as nx

from collections import OrderedDict
from argparse import ArgumentParser
from logzero import logger

from sgraph import loader, metrics as ms


def parse_arguments():
    parser = ArgumentParser(description='''
        Analyzes the clustering results in an output folder. The folder must contain clusters.txt and graph.txt
    ''')

    parser.add_argument('-i', '--logdir', required=True)
    parser.add_argument('-o', '--outdir', default=None)
    parser.add_argument('-f', '--feats', default=None)
    parser.add_argument('-fn', '--featnames', default=None)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    logzero.logfile('logs/analyze_results.log', mode='w')
    if args.outdir is None:
        args.outdir = args.logdir
    os.makedirs(args.outdir, exist_ok=True)

    g = loader.load_raw_graph(os.path.join(args.logdir, 'graph.txt'))
    has_feats = args.feats is not None and args.featnames is not None
    feat_names = []

    if has_feats:
        logger.info('Loading features')
        feat_names = loader.add_node_feats(g, args.feats, args.featnames)
    
    clpath = os.path.join(args.logdir, 'clusters.txt')
    clusters = loader.load_clusters(clpath)

    metrics, props = OrderedDict(), []
    FEAT_K = 5
    
    # Node count
    logger.info('Logging node count')
    metrics['# nodes'] = g.number_of_nodes()
    # Edge count
    logger.info('Logging edge count')
    metrics['# edges'] = g.number_of_edges()
    # Cluster count
    logger.info('Logging cluster count')
    metrics['# clusters'] = len(clusters)

    if has_feats:
        # Top features
        logger.info('Getting top %d features' % FEAT_K)
        top_k = ms.top_k_feats(g, feat_names, k=FEAT_K)
        top_ks = []
        for i, (feat, count) in enumerate(top_k):
            top_ks.append('%s(%d)' % (feat, count))
        metrics['Top %d Features' % FEAT_K] = top_ks

    for i, cl in enumerate(clusters):
        logger.info('Getting props for cluster %d/%d' % (i+1, len(clusters)))
        gx = g.subgraph(cl)
        pr = OrderedDict()

        # Cluster node count
        pr['# nodes'] = gx.number_of_nodes()
        # Cluster edge count
        pr['# edges'] = gx.number_of_edges()
        if has_feats:
            # Top features
            top_k = ms.top_k_feats(gx, feat_names, k=FEAT_K)
            top_ks = []
            for i, (feat, count) in enumerate(top_k):
                top_ks.append('%s(%d)' % (feat, count))
            pr['Top %d Features' % FEAT_K] = top_ks
        props.append(pr)

    mpath = os.path.join(args.outdir, 'metrics.json')
    logger.info('Saving metrics to %s' % mpath)
    with open(mpath, 'wt') as f:
        f.write(json.dumps(metrics, indent=2))

    ppath = os.path.join(args.outdir, 'props.json')
    logger.info('Saving props to %s' % ppath)
    with open(ppath, 'wt') as f:
        f.write(json.dumps(props, indent=2))
