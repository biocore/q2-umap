from qiime2.plugin import (Plugin, Int, Citations,
                           Range, Float)
from q2_types.distance_matrix import DistanceMatrix
from q2_types.ordination import PCoAResults
from q2_umap.umap import embed, center

citations = Citations.load('citations.bib', package='q2_umap')

plugin = Plugin(
    name='umap',
    version='0.1.1',
    website='https://github.com/gwarmstrong/q2-umap',
    package='q2_umap',
    description=('This QIIME 2 plugin supports exploring community '
                 'differences through embedding with the UMAP algorithm.'),
    short_description='Plugin for UMAP visualization.',
)

plugin.methods.register_function(
    function=embed,
    inputs={
        'distance_matrix': DistanceMatrix,
    },
    parameters={
        'number_of_dimensions': Int % Range(1, 3, inclusive_end=True),
        'n_neighbors': Int % Range(1, None),
        'min_dist': Float % Range(0, 1, inclusive_end=True),
        'random_state': Int,
    },
    outputs=[
        ('umap', PCoAResults),
    ],
    input_descriptions={
        'distance_matrix': (
            'The distance matrix over which UMAP should be computed.'
        ),
    },
    parameter_descriptions={
        'number_of_dimensions': (
            'The number of components to use for UMAP embeddings.'
        ),
        'n_neighbors': (
            'The local neighborhood size used for UMAP.'
        ),
        'min_dist': (
            'Controls how tightly UMAP is allowed to pack points together.'
        ),
        'random_state': (
            'Seed used by the random number generator.'
        ),
    },
    output_descriptions={
        'umap':
            'Ordination matrix computed by UMAP.'
    },
    name='UMAP Embedding',
    description='Applies UMAP to generate embeddings of the distance matrix.',
    citations=[
        citations['lel2018umap'],
    ]
)

plugin.methods.register_function(
    function=center,
    inputs={
        'embedding': PCoAResults,
    },
    parameters={
    },
    outputs=[
        ('centered_embedding', PCoAResults),
    ],
    input_descriptions={
        'embedding': (
            'Embedding to center.'
        )
    },
    parameter_descriptions={
    },
    output_descriptions={
        'centered_embedding': (
            'Embedding translated such that it is centered around 0'
            'and rotated so that the principal axes of the original '
            'embedding are used as the axes.'
        )
    },
    name='center embedding',
    description='Applies a centering to an embedding',
)
