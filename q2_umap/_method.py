import pandas as pd
import skbio
import umap
from skbio.stats.composition import clr
from scipy.spatial.distance import euclidean
from sklearn.metrics.pairwise import _VALID_METRICS as _SK_VALID_METRICS
from scipy.spatial.distance import pdist
from ast import literal_eval
from typing import Union, Callable
from q2_types.feature_table import BIOMV210Format
from q2_types.tree import NewickFormat
from q2_diversity import beta_phylogenetic

_ADDITIONAL_METRICS = ['aitchison']
_PHYLOGENETIC_METRICS = ['unweighted_unifrac', 'weighted_unifrac',
                         'weighted_normalized_unifrac', 'generalized_unifrac']
_VALID_METRICS = _ADDITIONAL_METRICS + _SK_VALID_METRICS


def pipeline(ctx, table, metadata, umap_metric='euclidean', n_components=3,
             pseudocount=1, umap_args=None, sampling_depth=None,
             with_replacement=False):
    rarefy = ctx.get_action('feature_table', 'rarefy')
    dm = ctx.get_action('umap', 'distances')
    pcoa = ctx.get_action('diversity', 'pcoa')
    emperor_plot = ctx.get_action('emperor', 'plot')

    results = []

    if sampling_depth:
        rarefied_table = rarefy(table=table, sampling_depth=sampling_depth,
                                with_replacement=with_replacement)
        to_dm = rarefied_table.rarefied_table
    else:
        rarefied_table = [table]
        to_dm = table

    results += rarefied_table

    dm_results = dm(table=to_dm, umap_metric=umap_metric,
                    n_components=n_components, pseudocount=pseudocount,
                    umap_args=umap_args)

    results += dm_results

    pcoa_results = pcoa(distance_matrix=dm_results.distance_matrix)

    results += pcoa_results

    results += emperor_plot(pcoa=pcoa_results.pcoa, metadata=metadata)

    return tuple(results)


def pipeline_phylogenetic(ctx, table, phylogeny, metadata,
                          umap_metric,
                          n_components=3,
                          n_jobs=1,
                          variance_adjusted=False,
                          alpha=None,
                          bypass_tips=True,
                          umap_args=None, sampling_depth=None,
                          with_replacement=False):
    rarefy = ctx.get_action('feature_table', 'rarefy')
    dm = ctx.get_action('umap', 'distances_phylogenetic')
    pcoa = ctx.get_action('diversity', 'pcoa')
    emperor_plot = ctx.get_action('emperor', 'plot')

    results = []

    if sampling_depth:
        rarefied_table = rarefy(table=table, sampling_depth=sampling_depth,
                                with_replacement=with_replacement)
        to_dm = rarefied_table.rarefied_table
    else:
        rarefied_table = [table]
        to_dm = table

    results += rarefied_table

    dm_results = dm(table=to_dm, phylogeny=phylogeny,
                    n_jobs=n_jobs, variance_adjusted=variance_adjusted,
                    alpha=alpha, bypass_tips=bypass_tips,
                    umap_metric=umap_metric, n_components=n_components,
                    umap_args=umap_args)

    results += dm_results

    pcoa_results = pcoa(distance_matrix=dm_results.distance_matrix)

    results += pcoa_results

    results += emperor_plot(pcoa=pcoa_results.pcoa, metadata=metadata)

    return tuple(results)


def distances_phylogenetic(table: BIOMV210Format,
                           phylogeny: NewickFormat,
                           umap_metric: str,
                           n_jobs: int = 1,
                           variance_adjusted: bool = False,
                           alpha: float = None,
                           n_components: int = 3,
                           umap_args: Union[str, dict] = None,
                           bypass_tips: bool = False) -> skbio.DistanceMatrix:
    if umap_args is None:
        umap_args = dict()
    elif isinstance(umap_args, str):
        umap_args = literal_eval(umap_args)
    dm = beta_phylogenetic(table, phylogeny, umap_metric, n_jobs=n_jobs,
                           variance_adjusted=variance_adjusted, alpha=alpha,
                           bypass_tips=bypass_tips)

    reducer = umap.UMAP(n_components=n_components, metric='precomputed',
                        random_state=42, **umap_args)
    embedding = reducer.fit_transform(dm.data)

    # get euclidean distances between UMAP embeddings
    sample_distances = pdist(embedding)

    return skbio.DistanceMatrix(sample_distances, ids=dm.ids)


def distances(table: pd.DataFrame,
              umap_metric: Union[str, Callable] = 'euclidean',
              n_components: int = 3, pseudocount: int = 1,
              umap_args: Union[str, dict] = None) -> skbio.DistanceMatrix:

    # perform argument checks
    if umap_args is None:
        umap_args = dict()
    elif isinstance(umap_args, str):
        umap_args = literal_eval(umap_args)

    if umap_metric not in _VALID_METRICS and not callable(umap_metric):
        raise ValueError("Unknown metric %s. "
                         "Valid metrics are %s, or a "
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
