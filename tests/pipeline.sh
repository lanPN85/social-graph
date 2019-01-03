#!/usr/bin/env bash

set -e

EGO_ID=${1:-477094958}

./conv_cluster.py -i data/twitter/egos/${EGO_ID}.edges -p 3 -co rwsymm

./analyze_results.py -i out/${EGO_ID}-rwsymm-laplacian/component-0\
    -f data/twitter/egos/${EGO_ID}.feat\
    -fn data/twitter/egos/${EGO_ID}.featnames
