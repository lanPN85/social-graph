#!/usr/bin/env bash

set -e

EGO_ID=${1:-477094958}
PARTITIONS=${2:-4}

echo "Clustering..."
./conv_cluster.py -i data/twitter/egos/${EGO_ID}.edges\
    -p ${PARTITIONS} -co rwsymm -cl laplacian

echo "Analyzing results..."
./analyze_results.py -i out/${EGO_ID}-rwsymm-laplacian/component-0\
    -f data/twitter/egos/${EGO_ID}.feat\
    -fn data/twitter/egos/${EGO_ID}.featnames

echo "Starting dashboard..."
./dashboard.py -i out/${EGO_ID}-rwsymm-laplacian/component-0
