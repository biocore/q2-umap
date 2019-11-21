import pandas as pd
from qiime2 import Metadata, Artifact
from qiime2.plugin.testing import TestPluginBase


class TestUMAPPipeline(TestPluginBase):

    package = 'q2_umap'

    def setUp(self):
        super().setUp()
        self.data = pd.DataFrame([[1, 2, 0, 4],
                                  [1, 4, 3, 5],
                                  [0, 0, 1, 2],
                                  [0, 1, 2, 1],
                                  [1, 2, 2, 0],
                                  [0, 1, 1, 0]],
                                 index=['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
                                 columns=['O1', 'O2', 'O3', 'O4'])
        self.metadata = Metadata(
            pd.DataFrame({'foo': ['1', '2', '3', '4', '5', '6']},
                         index=pd.Index(['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
                                        name='id')))
        self.pipeline = self.plugin.pipelines['pipeline']
        self.distance = self.plugin.methods['distances']

    def test_pipeline_all_results(self):
        table = Artifact.import_data('FeatureTable[Frequency]', self.data)
        results = self.pipeline(table, metadata=self.metadata,
                                umap_args="{'n_neighbors': 3}")
        self.assertEqual(len(results), 3)

    def test_pipeline_dm(self):
        table = Artifact.import_data('FeatureTable[Frequency]', self.data)
        results = self.pipeline(table, metadata=self.metadata,
                                umap_args="{'n_neighbors': 3}")
        self.assertEqual(repr(results.distance_matrix.type),
                         'DistanceMatrix')

    def test_pipeline_pcoa(self):
        table = Artifact.import_data('FeatureTable[Frequency]', self.data)
        results = self.pipeline(table, metadata=self.metadata,
                                umap_args="{'n_neighbors': 3}")
        self.assertEqual(repr(results.pcoa_results.type),
                         'PCoAResults')

    def test_pipeline_emperor(self):
        table = Artifact.import_data('FeatureTable[Frequency]', self.data)
        results = self.pipeline(table, metadata=self.metadata,
                                umap_args="{'n_neighbors': 3}")
        self.assertEqual(repr(results.emperor.type), 'Visualization')


class TestUMAPDistances(TestPluginBase):
    package = 'q2_umap'

    def setUp(self):
        super().setUp()
        self.data = pd.DataFrame([[1, 2, 0, 4],
                                  [1, 4, 3, 5],
                                  [0, 0, 1, 2],
                                  [0, 1, 2, 1],
                                  [1, 2, 2, 0],
                                  [0, 1, 1, 0]],
                                 index=['S1', 'S2', 'S3', 'S4', 'S5',
                                        'S6'],
                                 columns=['O1', 'O2', 'O3', 'O4'])
        self.metadata = Metadata(
            pd.DataFrame({'foo': ['1', '2', '3', '4', '5', '6']},
                         index=pd.Index(
                             ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
                             name='id')))
        self.distance = self.plugin.methods['distances']

    def test_distances(self):
        table = Artifact.import_data('FeatureTable[Frequency]', self.data)
        results = self.distance(table, umap_args="{'n_neighbors': 3}")
        self.assertEqual(repr(results.distance_matrix.type), 'DistanceMatrix')
