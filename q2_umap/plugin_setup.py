from qiime2.plugin import (Plugin, Str, Int, Citations, Metadata,
                           Visualization, Range, Bool, Choices, Float)
from q2_types.feature_table import FeatureTable, Frequency
from q2_types.tree import Phylogeny, Rooted
from q2_types.distance_matrix import DistanceMatrix
from q2_types.ordination import PCoAResults
import q2_umap
from q2_diversity import _beta as beta

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
        'umap_args': Str,
        'sampling_depth': Int % Range(1, None),
        'with_replacement': Bool,
    },
    outputs=[
        ('rarefied_table', FeatureTable[Frequency]),
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
        'umap_args': 'Additional arguments to passed into UMAP',
        'sampling_depth': 'The total frequency that each sample should be '
                          'rarefied to prior to computing distance metric.',
        'with_replacement': 'Rarefy with replacement by sampling from the '
                            'multinomial distribution instead of rarefying '
                            'without replacement.',
    },
    output_descriptions={
        'rarefied_table':
            'The resulting rarefied feature table (if sampling depth is '
            'specified). Otherwise, it is the original table.',
        'distance_matrix':
            'Matrix of distances between UMAP embeddings.',
        'pcoa_results':
            'PCoA matrix computed from distances between UMAP embeddings '
            'for each sample.',
        'emperor':
            'Emperor plot of the PCoA matrix computed from UMAP embeddings.',
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

plugin.methods.register_function(
    function=q2_umap.distances_phylogenetic,
    inputs={
        'table': FeatureTable[Frequency],
        'phylogeny': Phylogeny[Rooted],
    },
    parameters={
        'umap_metric': Str % Choices(beta.phylogenetic_metrics()),
        'n_jobs': Int,
        'variance_adjusted': Bool,
        'alpha': Float % Range(0, 1, inclusive_end=True),
        'bypass_tips': Bool,
        'n_components': Int,
        'umap_args': Str,
    },
    outputs=[
        ('distance_matrix', DistanceMatrix),
    ],
    input_descriptions={
        'table': ('The feature table containing the samples over which UMAP '
                  'distances should be computed.'),
        'phylogeny': ('Phylogenetic tree containing tip identifiers that '
                      'correspond to the feature identifiers in the table. '
                      'This tree can contain tip ids that are not present in '
                      'the table, but all feature ids in the table must be '
                      'present in this tree.')
    },
    parameter_descriptions={
        'umap_metric': 'The metric to use within the UMAP algorithm.',
        'n_jobs': 'The number of workers to use.',
        'variance_adjusted': ('Perform variance adjustment based on Chang et '
                              'al. BMC Bioinformatics 2011. Weights distances '
                              'based on the proportion of the relative '
                              'abundance represented between the samples at a'
                              ' given node under evaluation.'),
        'alpha': ('This parameter is only used when the choice of metric is '
                  'generalized_unifrac. The value of alpha controls importance'
                  ' of sample proportions. 1.0 is weighted normalized UniFrac.'
                  ' 0.0 is close to unweighted UniFrac, but only if the sample'
                  ' proportions are dichotomized.'),
        'bypass_tips': ('In a bifurcating tree, the tips make up about 50% of '
                        'the nodes in a tree. By ignoring them, specificity '
                        'can be traded for reduced compute time. This has the'
                        ' effect of collapsing the phylogeny, and is analogous'
                        ' (in concept) to moving from 99% to 97% OTUs'),
        'n_components': 'The number of components to use for UMAP embeddings',
        'umap_args': 'Additional arguments to passed into UMAP',
    },
    output_descriptions={
        'distance_matrix': 'The resulting distance matrix.',
    },
    name='UMAP Distances',
    description='Computes Euclidean distances between UMAP embeddings on a '
                'user-specified phylogenetic distance metric and number of '
                'components for all pairs of samples in a feauture table.',
    citations=[
        citations['lel2018umap'],
        citations['lozupone2005unifrac'],
        citations['lozupone2007quantitative'],
        citations['chang2011variance'],
        citations['chen2012associating'],
        citations['mcdonald2018unifrac'],
    ]
)
