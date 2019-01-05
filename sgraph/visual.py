import os
import random
import networkx as nx
import graphviz as gv

from logzero import logger
from networkx.drawing.nx_agraph import write_dot


def render_graph(g, outdir='.', name='graph', format='png',
                 engine='neato', no_label=False, node_attrs=None,
                 graph_attrs=None, edge_attrs=None):
    directional = isinstance(g, nx.DiGraph)
    gcls = gv.Digraph if directional else gv.Graph

    if node_attrs is None:
        node_attrs = {}
    if no_label:
        node_attrs['label'] = ''

    g_ = gcls(name=name, directory=outdir, format=format,
              node_attr=node_attrs, graph_attr=graph_attrs,
              edge_attr=edge_attrs, engine=engine)

    for edge in g.edges():
        g_.edge(str(edge[0]), str(edge[1]),
                **g.edges[edge[0], edge[1]])
    g_.render()


def render_clusters(g, clusters, outdir='.', name='graph', format='png',
                    engine='neato', no_label=False, node_attrs=None, 
                    graph_attrs=None, edge_attrs=None):
    directional = isinstance(g, nx.DiGraph)
    gcls = gv.Digraph if directional else gv.Graph

    if node_attrs is None:
        node_attrs = {}
    if no_label:
        node_attrs['label'] = ''
    
    g_ = gcls(name=name, directory=outdir, format=format, edge_attr=edge_attrs,
              node_attr=node_attrs, graph_attr=graph_attrs, engine=engine)
    clus_ = [gcls(name='cluster_%d' % i, directory=outdir, format=format, engine=engine,
                node_attr=node_attrs, graph_attr=graph_attrs, edge_attr=edge_attrs) for i in range(len(clusters))]
    colors = [random_color() for _ in range(len(clusters))]
    
    for e1, e2 in g.edges():
        skip = False
        for j, cl in enumerate(clusters):
            if e1 in cl and e2 in cl:
                clus_[j].node(str(e1), fillcolor=colors[j])
                clus_[j].node(str(e2), fillcolor=colors[j])
                clus_[j].edge(str(e1), str(e2), color=colors[j], **g.edges[e1, e2])
                skip = True
                break
        if not skip:
            g_.edge(str(e1), str(e2), **g.edges[e1, e2])
    
    for cl_ in clus_:
        g_.subgraph(cl_)
    
    g_.render()


def random_color():
    def rand_int():
        return random.randint(0, 255)
    return '#%02X%02X%02X' % (rand_int(), rand_int(), rand_int())
