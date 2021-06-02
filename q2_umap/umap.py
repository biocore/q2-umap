import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from skbio.stats.distance import DistanceMatrix
from skbio.stats.ordination import OrdinationResults
from umap import UMAP


def embed(
            distance_matrix: DistanceMatrix,
            n_neighbors: int,
            min_dist: float = 1,
            number_of_dimensions: int = 2,
            random_state: int = 724,
        ) -> OrdinationResults:

    n_samples = len(distance_matrix.ids)
    if number_of_dimensions > n_samples:
        raise ValueError(
            f'number_of_dimensions ({number_of_dimensions}) must be fewer than'
            f'number of samples ({n_samples}) - 2'
        )

    transformer = UMAP(
        n_neighbors=n_neighbors,
        n_components=number_of_dimensions,
        min_dist=min_dist,
        random_state=random_state,
        metric='precomputed',
    )

    embedding = transformer.fit_transform(distance_matrix[:, :])

    if embedding.shape[1] < 3:
        difference = 3 - embedding.shape[1]
        embedding = np.hstack((embedding, np.zeros((len(embedding),
                                                    difference))))

    number_of_dimensions = embedding.shape[1]

    embedding_df = pd.DataFrame(embedding, index=distance_matrix.ids,
                                columns=[f'UMAP-{i}' for i in
                                         range(embedding.shape[1])]
                                )

    null_eigvals = pd.Series(np.zeros(number_of_dimensions))
    ord_results = OrdinationResults(
        'umap',
        'Uniform Manifold Approximation and Projection',
        eigvals=null_eigvals,
        samples=embedding_df,
        proportion_explained=null_eigvals,
    )

    return center(ord_results)


def center(embedding: OrdinationResults) -> OrdinationResults:
    short_name = embedding.short_method_name
    long_name = embedding.long_method_name
    n_dimensions = embedding.samples.shape[1]
    transformer = PCA(n_components=n_dimensions)
    new_embedding = transformer.fit_transform(embedding.samples)

    embedding_df = pd.DataFrame(new_embedding,
                                index=embedding.samples.index,
                                columns=embedding.samples.columns
                                )

    null_eigvals = pd.Series(np.zeros(n_dimensions))
    ord_results = OrdinationResults(
        short_name,
        long_name,
        eigvals=null_eigvals,
        samples=embedding_df,
        proportion_explained=null_eigvals,
    )
    return ord_results
