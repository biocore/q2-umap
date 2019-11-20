from qiime2.plugin import (Plugin, Str, Int, Citations, Metadata,
                           Visualization)
from q2_types.feature_table import FeatureTable, Frequency
from q2_types.distance_matrix import DistanceMatrix
from q2_types.ordination import PCoAResults
import q2_umap

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

plugin.pipelines.register_function(
    function=q2_umap.pipeline,
    inputs={
        'table': FeatureTable[Frequency],
    },
    parameters={
        'metadata': Metadata,
        'umap_metric': Str,
        'n_components': Int,
        'pseudocount': Int,
        'umap_args': Str
    },
    outputs=[
        ('distance_matrix', DistanceMatrix),
        ('pcoa_results', PCoAResults),
        ('emperor', Visualization),
    ],
    input_descriptions={
        'table': ('The feature table containing the samples over which UMAP '
                  'distances should be computed.'),
    },
    parameter_descriptions={
        'metadata': 'The sample metadata to use in the emperor plots.',
        'umap_metric': 'The metric to use within the UMAP algorithm.',
        'n_components': 'The number of components to use for UMAP embeddings',
        'pseudocount': 'The pseudocount to use if using \'aitchision\' as '
                       'metric',
        'umap_args': 'Additional arguments to passed into UMAP'
    },
    output_descriptions={
        'distance_matrix':
            'Matrix of distances between UMAP embeddings.',
        'pcoa_results':
            'PCoA matrix computed from distances between UMAP embeddings '
            'for each sample.',
        'emperor':
            'Emperor plot of the PCoA matrix computed from UMAP embeddings.'
    },
    name='UMAP Pipeline',
    description='Applies a steps to ordinate and visualize samples in a '
                'feature table using UMAP embeddings.'
)

plugin.methods.register_function(
    function=q2_umap.distances,
    inputs={
        'table': FeatureTable[Frequency],
    },
    parameters={
        'umap_metric': Str,
        'n_components': Int,
        'pseudocount': Int,
        'umap_args': Str
    },
    outputs=[
        ('distance_matrix', DistanceMatrix),
    ],
    input_descriptions={
        'table': ('The feature table containing the samples over which UMAP '
                  'distances should be computed.'),
    },
    parameter_descriptions={
        'umap_metric': 'The metric to use within the UMAP algorithm.',
        'n_components': 'The number of components to use for UMAP embeddings',
        'pseudocount': 'The pseudocount to use if using \'aitchision\' as '
                       'metric',
        'umap_args': 'Additional arguments to passed into UMAP',
    },
    output_descriptions={
        'distance_matrix': 'The resulting distance matrix.',
    },
    name='UMAP Distances',
    description='Computes Euclidean distances between UMAP embeddings on a '
                'user-specified metric and number of components for all '
                'pairs of samples in a feauture table.',
    citations=[
        citations['lel2018umap'],
    ]
)
