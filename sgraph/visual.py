import os
import networkx as nx
import graphviz as gv

from logzero import logger
from networkx.drawing.nx_agraph import write_dot


def render_graph(g, outdir='.', name='graph', format='pdf',
                 no_label=False, node_attrs=None,
                 graph_attrs=None):
    directional = isinstance(g, nx.DiGraph)
    gcls = gv.Digraph if directional else gv.Graph

    if node_attrs is None:
        node_attrs = {}
    if no_label:
        node_attrs['label'] = ''

    g_ = gcls(name=name, directory=outdir, format=format,
              node_attr=node_attrs, graph_attr=graph_attrs)

    for edge in g.edges():
        g_.edge(str(edge[0]), str(edge[1]),
                **g.edges[edge[0], edge[1]])
    g_.render()


def render_clusters(g, clusters, outdir='.', name='graph', format='pdf',
                    no_label=False, node_attrs=None, graph_attrs=None):
    directional = isinstance(g, nx.DiGraph)
    gcls = gv.Digraph if directional else gv.Graph

    if node_attrs is None:
        node_attrs = {}
    if no_label:
        node_attrs['label'] = ''
    
    g_ = gcls(name=name, directory=outdir, format=format,
              node_attr=node_attrs, graph_attr=graph_attrs)
    clus_ = [gcls(name='cluster_%d' % i, directory=outdir, format=format,
                node_attr=node_attrs, graph_attr=graph_attrs) for i in range(len(clusters))]
    
    for e1, e2 in g.edges():
        skip = False
        for j, cl in enumerate(clusters):
            if e1 in cl and e2 in cl:
                clus_[j].edge(str(e1), str(e2), **g.edges[e1, e2])
                skip = True
                break
        if not skip:
            g_.edge(str(e1), str(e2), **g.edges[e1, e2])
    
    for cl_ in clus_:
        g_.subgraph(cl_)
    
    g_.render()
