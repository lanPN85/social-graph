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
    parser.add_argument('-o', '--outdir', default=None)
    parser.add_argument('-p', '--partitions', type=int, default=8)
    parser.add_argument('-co', '--converter', default='naive', help=str(list(CONVERTERS.keys())))
    parser.add_argument('-cl', '--clusterer', default='laplacian', help=str(list(CLUSTERERS.keys())))
    parser.add_argument('-e', '--engine', default='neato')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    if args.outdir is None:
        inp_name = os.path.split(args.input)[-1].split('.')[:-1]
        inp_name = '.'.join(inp_name)
        args.outdir = os.path.join('out/', inp_name)

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
        outdir = os.path.join(args.outdir, 'component-%d' % i)
        os.makedirs(outdir, exist_ok=True)

        logger.info('Component %d/%d' % (i+1, len(comp_g)))
        logger.info('Clustering')
        clu = CLUSTERERS[args.clusterer]
        clusters = clu(gx, partitions=args.partitions)
        
        out_name = 'clusters.txt'
        out_path = os.path.join(outdir, out_name)
        logger.info('Saving clusters to %s' % out_path)
        save_clusters(clusters, out_path)

        out_name = 'graph.txt'
        out_path = os.path.join(outdir, out_name)
        logger.info('Saving graph edges to %s' % out_path)
        save_edges(g, out_path)
        
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
        logger.info('Rendering %d clusters' % len(clusters))
        visual.render_clusters(g, clusters, outdir=outdir,
            name='clusters', no_label=True, node_attrs=node_attrs,
            edge_attrs=edge_attrs, engine=args.engine)
        logger.info('Rendering original graph')
        visual.render_graph(g, outdir=outdir, edge_attrs=edge_attrs,
            name='graph', no_label=True, node_attrs=node_attrs,
            engine=args.engine)
