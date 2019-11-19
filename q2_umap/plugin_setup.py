from qiime2.plugin import (Plugin, Str, Int, Citations)
from q2_types.feature_table import FeatureTable, Frequency
from q2_types.distance_matrix import DistanceMatrix
from q2_umap._method import distances
import skbio

citations = Citations.load('citations.bib', package='q2_umap')

plugin = Plugin(
    name='umap',
    version='0.0.1',
    website='https://github.com/gwarmstrong/q2-umap',
    package='q2_umap',
    description=('This QIIME 2 plugin supports exploring community '
                 'differences through embedding with the UMAP algorithm.'),
    short_description='Plugin for community difference analysis.',
)

plugin.methods.register_function(
    function=distances,
    inputs={'table': FeatureTable[Frequency]},
    parameters={'metric': Str,
                'n_components': Int,
                'pseudocount': Int,
                'umap_args': Str},
    outputs=[('distance_matrix', DistanceMatrix)],
    input_descriptions={
        'table': ('The feature table containing the samples over which UMAP '
                  'distances should be computed.')
    },
    parameter_descriptions={
        'metric': 'The metric to use within the UMAP algorithm.',
        'n_components': 'The number of components to use for UMAP embeddings',
        'pseudocount': 'The pseudocount to use if using \'aitchision\' as '
                       'metric',
        'umap_args': 'Additional arguments to passed into UMAP'
    },
    output_descriptions={'distance_matrix': 'The resulting distance matrix.'},
    name='UMAP Distances',
    description='Computes Euclidean distances between UMAP embeddings on a '
                'user-specified metric and number of components for all '
                'pairs of samples in a feauture table.',
    citations=[citations['lel2018umap']]
)

