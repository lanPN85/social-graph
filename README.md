# Social Graph Clustering
This repo contains examples of directed social graph clustering on the Twitter network dataset (Big Data - IT4779 - HUST).

Authors: Phan Ngoc Lan, Nguyen Duy Manh, Vi Thanh Dat

## Quickstart
```bash
pip3 install -r requirements.txt

# Run tests
pytest tests/
```

## Dataset
To download and extract the Twitter dataset, run the following:
```bash
cd data/twitter
./download.sh
```

## Convert-Cluster Pipeline
The pipeline consists of the following scripts:
- `conv_cluster.py`: Outputs clusters and GraphViz visualizations for an input network (edge list representation)
- `analyze_results.py`: Uses the output directory to produce graph metrics (`metrics.json`) and cluster properties (`props.json`)
- `dashboard.py`: Displays results in a web interface

For convenience, you can run the pipeline on a Twitter ego net using:
```bash
./tests/pipeline.sh [EGO_NET_ID] [NUM_PARTITIONS]
```
