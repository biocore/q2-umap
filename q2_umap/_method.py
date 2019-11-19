import pandas as pd
import skbio
import umap
from skbio.stats.composition import clr
from scipy.spatial.distance import euclidean
from sklearn.metrics.pairwise import _VALID_METRICS as _SK_VALID_METRICS
from scipy.spatial.distance import pdist

_ADDITIONAL_METRICS = ['aitchison']
_VALID_METRICS = _ADDITIONAL_METRICS + _SK_VALID_METRICS


def distances(table: pd.DataFrame, metric: str = 'euclidean',
              n_components: int = 3, pseudocount: int = 1,
              umap_args: dict = None) -> skbio.DistanceMatrix:

    # perform argument checks
    if umap_args is None:
        umap_args = dict()
    if (metric not in _VALID_METRICS and not callable(metric) and metric is
            not None):
        raise ValueError("Unknown metric %s. "
                         "Valid metrics are %s, or 'precomputed', or a "
                         "callable" % (metric, _VALID_METRICS))
    counts = table.values
    if counts.sum() == 0:
        raise ValueError("The provided table object is empty")

    # define aitchison distance calculation
    def aitchison(x, y, **kwds):
        return euclidean(clr(x), clr(y))
    if metric == 'aitchison':
        counts += pseudocount
        metric = aitchison

    # run UMAP
    reducer = umap.UMAP(n_components=n_components, metric=metric,
                        random_state=42, **umap_args)
    embedding = reducer.fit_transform(counts)

    # get euclidean distances between UMAP embeddings
    sample_distances = pdist(embedding)

    return skbio.DistanceMatrix(sample_distances, ids=table.index)
