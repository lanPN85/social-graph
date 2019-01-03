#!/usr/bin/env python3

import os
import logzero
import json
import socket
import flask
import shutil
import dash
import dash_core_components as dcc
import dash_table as dt
import dash_html_components as html

from argparse import ArgumentParser
from logzero import logger


def parse_arguments():
    parser = ArgumentParser(description='''
        Serves a dashboard visualizing results using Dash. The input
        directory must contain clusters.gv.png and graph.gv.png
    ''')

    parser.add_argument('-i', '--logdir', required=True)
    parser.add_argument('-p', '--port', type=int, default=None)

    return parser.parse_args()


def find_free_port(start=8050, end=65535):
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            res = sock.connect_ex(('localhost', port))
            if res != 0:
                return port
    raise ValueError('No free port in specified range')


if __name__ == "__main__":
    args = parse_arguments()
    logzero.logfile('logs/dashboard.log', mode='w')
    shutil.copy2('static/favicon.ico', os.path.join(args.logdir, 'favicon.ico'))

    metrics = {}
    mpath = os.path.join(args.logdir, 'metrics.json')
    if os.path.exists(mpath):
        logger.info('Loading metrics')
        with open(mpath, 'rt') as f:
            metrics = json.load(f)
    else:
        logger.warning('No metrics file found. Metrics won\'t be shown.')
    
    props = []
    ppath = os.path.join(args.logdir, 'props.json')
    if os.path.exists(ppath):
        logger.info('Loading cluster properties')
        with open(ppath, 'rt') as f:
            props = json.load(f)
    else:
        logger.warning('No props file found. Props won\'t be shown.')

    app = dash.Dash(__name__, assets_folder=args.logdir,
        external_stylesheets=[
            '/static/plotly.css',
            '/static/bootstrap/css/bootstrap.css',
            '/static/bootstrap/css/bootstrap-theme.css'
        ])

    img_src = ['/assets/graph.gv.png', '/assets/clusters.gv.png']

    # Render metrics
    tab_metric = []
    for name, val in metrics.items():
        tab_metric.append({
            'Metric': name.capitalize(),
            'Value': val
        })

    # Render props
    tab_props = []
    prop_keys = []
    for i, cl in enumerate(props):
        pr = {'Cluster': i + 1}
        pr.update(cl)
        prop_keys = list(cl.keys())
        tab_props.append(pr)
    prop_keys.insert(0, 'Cluster')

    # Styles
    bg_color = '#424242'
    txt_color = 'white'

    # Declare layout
    app.title = 'Community Detection'
    app.layout = html.Div([
        html.Div([
            html.H2(html.B('Community Visualization')),
            html.P('Log directory: %s' % args.logdir, style={'font-size': 'small'}),
        ], className='row', style={
            'backgroundColor': bg_color,
            'color': txt_color,
            'padding-left': '10px',
            'padding-right': '10px',
            'margin-bottom': '10px'
        }),
        html.Div([
            html.Div([
                html.H2('Metrics'),
                dt.DataTable(data=tab_metric,
                    id='met_table',
                    columns=[
                        {'id': 'Metric', 'name': 'Metric Name'},
                        {'id': 'Value', 'name': 'Value'}
                    ], style_table={
                        'height': '300',
                        'overflowY': 'auto'
                    }, style_as_list_view=True,
                    style_header={
                        'fontWeight': 'bold'
                    }, style_cell={
                        'textAlign': 'left'
                    })
            ], className='col-xs-4'),
            html.Div([
                html.H2('Cluster Properties'),
                dt.DataTable(data=tab_props,
                    id='prop_table',
                    columns=[{'id': c, 'name': c} for c in prop_keys],
                    style_table={
                        'height': '300',
                        'overflowY': 'auto',
                        'overflowX': 'auto'
                    }, style_as_list_view=True,
                    style_header={
                        'fontWeight': 'bold'
                    }, style_cell={
                        'textAlign': 'left'
                    })
            ], className='col-xs-8', style={'border-left': '1px solid black'})
        ], className='row', style={
            'margin': '0 5px 0 5px',
            'border-bottom': '1px solid black'
        }),
        html.Div([
            html.H2('Graphs'),
            html.Div([
                html.Div([
                    html.Img(src=src_, className='img-responsive', 
                            width="100%"),
                    html.Div([
                        html.H4(html.A(src_, href=src_), className='text-center')
                    ], className='row')
                ], className='col-xs-6', style={}) for src_ in img_src
            ], className='row')
        ], style={
            'margin': '0 5px 5px 5px', 
            # 'border': '1px solid black',
            'padding': '5px'
        }),
        html.P(html.A('Powered by Dash', href='https://plot.ly/products/dash/', target='_blank'), className='text-right')
    ], className='container-fluid')

    if args.port is None:
        args.port = find_free_port()
    app.run_server(port=args.port)
