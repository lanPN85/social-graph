#!/usr/bin/env python3

import os
import logzero
import networkx as nx

from argparse import ArgumentParser
from logzero import logger

from sgraph import loader, conversions, visual, cluster
from sgraph.output import save_clusters, save_edges

CONVERTERS = {
    'naive': conversions.naive_conversion
}

CLUSTERERS = {
    'laplacian': cluster.laplacian_cluster
}


def parse_arguments():
    parser = ArgumentParser()

    parser.add_argument('-i', '--input', default='data/twitter/twitter-combined.txt')
    parser.add_argument('-o', '--outdir', default='out/twitter')
    parser.add_argument('-p', '--partitions', type=int, default=8)
    parser.add_argument('-co', '--converter', default='naive', help=str(list(CONVERTERS.keys())))
    parser.add_argument('-cl', '--clusterer', default='laplacian', help=str(list(CLUSTERERS.keys())))
    parser.add_argument('-e', '--engine', default='neato')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    os.makedirs(args.outdir, exist_ok=True)
    logzero.logfile('logs/conv_cluster.log', mode='w')

    logger.info('Loading graph')
    g = loader.load_raw_graph(args.input)

    logger.info('Converting to undirected graph')
    conv = CONVERTERS[args.converter]
    ug = conv(g)

    logger.info('Finding connected components')
    comp_g = [ug.subgraph(c) for c in nx.connected_components(ug)]
    logger.info('Found %d components' % len(comp_g))
    del ug

    for i, gx in enumerate(comp_g):
        logger.info('Component %d/%d' % (i+1, len(comp_g)))
        logger.info('Clustering')
        clu = CLUSTERERS[args.clusterer]
        clusters = clu(gx, partitions=args.partitions)
        node_attrs = {
            'shape': 'point'
        }
        graph_attrs = {
            'clusterMode': 'global',
        }
        edge_attrs = {
            'arrowsize': '0.2',
            'arrowhead': 'open'
        }
        
        out_name = 'clusters-%d.txt' % i
        out_path = os.path.join(args.outdir, out_name)
        logger.info('Saving clusters to %s' % out_path)
        save_clusters(clusters, out_path)

        out_name = 'graph-%d.txt'
        out_path = os.path.join(args.outdir, out_name)
        logger.info('Saving graph edges to %s' % out_path)
        save_edges(g, out_path)

        logger.info('Rendering %d clusters' % len(clusters))
        visual.render_clusters(g, clusters, outdir=args.outdir,
            name='clusters-%d' % i, no_label=True, node_attrs=node_attrs,
            edge_attrs=edge_attrs, engine=args.engine)
        logger.info('Rendering original graph')
        visual.render_graph(g, outdir=args.outdir, edge_attrs=edge_attrs,
            name='graph-%d' % i, no_label=True, node_attrs=node_attrs,
            engine=args.engine)
