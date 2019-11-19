import pandas as pd
import skbio
import umap
from skbio.stats.composition import clr
from scipy.spatial.distance import euclidean
from sklearn.metrics.pairwise import _VALID_METRICS as _SK_VALID_METRICS
from scipy.spatial.distance import pdist
from ast import literal_eval
from typing import Union

_ADDITIONAL_METRICS = ['aitchison']
_VALID_METRICS = _ADDITIONAL_METRICS + _SK_VALID_METRICS


def distances(table: pd.DataFrame, umap_metric: str = 'euclidean',
              n_components: int = 3, pseudocount: int = 1,
              umap_args: Union[str, dict] = None) -> skbio.DistanceMatrix:

    # perform argument checks
    if umap_args is None:
        umap_args = dict()
    elif isinstance(umap_args, str):
        umap_args = literal_eval(umap_args)

    if (umap_metric not in _VALID_METRICS and not callable(umap_metric) and
            umap_metric is not None):
        raise ValueError("Unknown metric %s. "
                         "Valid metrics are %s, or 'precomputed', or a "
                         "callable" % (umap_metric, _VALID_METRICS))
    counts = table.values
    if counts.sum() == 0:
        raise ValueError("The provided table object is empty")

    # define aitchison distance calculation
    def aitchison(x, y, **kwds):
        return euclidean(clr(x), clr(y))
    if umap_metric == 'aitchison':
        counts += pseudocount
        umap_metric = aitchison

    # run UMAP
    reducer = umap.UMAP(n_components=n_components, metric=umap_metric,
                        random_state=42, **umap_args)
    embedding = reducer.fit_transform(counts)

    # get euclidean distances between UMAP embeddings
    sample_distances = pdist(embedding)

    return skbio.DistanceMatrix(sample_distances, ids=table.index)
