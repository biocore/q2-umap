![Build Status](https://github.com/biocore/q2-umap/actions/workflows/python-package.yml/badge.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/biocore/q2-umap/badge.svg?branch=master)](https://coveralls.io/github/gwarmstrong/q2-umap?branch=master)
# q2-umap
Applying umap to microbiome data via QIIME2.

This plugin is intended to be able to used very similarly to PCoA.


## Installation
Make sure you have working installation of [Qiime2](https://qiime2.org).

```bash
conda install umap-learn -c conda-forge
# in the q2-umap directory
pip install . 
```

## CAUTION
Note for all users. If you intend to view the results in 2 dimensions, you 
should use `--p-number-of-dimensions 2`. Taking the first 2 components of a 3 
dimensional embedding DOES NOT give you an optimal result.

## Example
We will use the [Moving Pictures Tutorial]() from [Qiime2](https://qiime2.org)
to demonstrate use of the plugin.

You should obtain the Jaccard distance matrix [here](https://docs.qiime2.org/2021.4/data/tutorials/moving-pictures/core-metrics-results/jaccard_distance_matrix.qza)
and the sample metadata [here](https://data.qiime2.org/2021.4/tutorials/moving-pictures/sample_metadata.tsv)

```bash
# get the data
wget \
 -O "jaccard_distance_matrix.qza" \
 "https://docs.qiime2.org/2021.4/data/tutorials/moving-pictures/core-metrics-results/jaccard_distance_matrix.qza"

wget \
  -O "sample-metadata.tsv" \
  "https://data.qiime2.org/2021.4/tutorials/moving-pictures/sample_metadata.tsv"
```

Then, we can use q2-umap:
```bash
# embed with umap
qiime umap embed \
  --i-distance-matrix jaccard_distance_matrix.qza \
  --p-n-neighbors 500 \
  --o-umap jaccard_umap.qza
  
# visualize with emperor
qiime emperor plot \
    --i-pcoa jaccard_umap.qza \
    --m-metadata-file sample-metadata.tsv \
    --o-visualization umap-emperor.qzv
    
```
