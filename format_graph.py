#!/usr/bin/env python3

import networkx as nx
import logzero
import os

from argparse import ArgumentParser
from logzero import logger

from sgraph.loader import load_raw_graph
from sgraph import conversions

FORMATS = {
    'gml': nx.readwrite.write_gml,
    'graphml': nx.readwrite.write_graphml,
    'yaml': nx.readwrite.write_yaml
}


CONVERTERS = {
    'naive': conversions.naive_conversion,
    'tsymm': conversions.transpose_symmetric_conversion,
    'rwsymm': conversions.random_walk_symmetric_conversion,
    'bisymm': conversions.biblio_symmetric_conversion
}


def parse_arguments():
    parser = ArgumentParser(description='''
        Converts the default edge list graph file to another format
    ''')

    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', default=None)
    parser.add_argument('-f', '--format', default='gml', help='|'.join(list(FORMATS.keys())))
    parser.add_argument('-co', '--converter', default=None, help='|'.join(list(CONVERTERS.keys())))

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    logzero.logfile('logs/format_graph.log', mode='w')
    if args.format not in FORMATS.keys():
        raise ValueError('Invalid format `%s`' % args.format)

    logger.info('Loading graph')
    g = load_raw_graph(args.input)
    if args.converter is not None:
        logger.info('Converting to undirected')
        g = CONVERTERS[args.converter](g)

    if args.output is None:
        args.output = '.'.join(args.input.split('.')[:-1]) + '.%s' % args.format
    
    logger.info('Saving conversion to %s' % args.output)
    FORMATS[args.format](g, args.output, stringizer=str)
