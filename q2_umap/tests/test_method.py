import unittest
import pandas as pd
from qiime2.plugin.testing import TestPluginBase
from qiime2 import Artifact, Metadata
from q2_umap._method import distances


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

    def test_pipeline(self):
        table = Artifact.import_data('FeatureTable[Frequency]', self.data)
        results = self.pipeline(table, metadata=self.metadata,
                                umap_args="{'n_neighbors': 3}")
        self.assertEqual(len(results), 3)
        self.assertEqual(repr(results.distance_matrix.type),
                         'DistanceMatrix')
        self.assertEqual(repr(results.pcoa.type),
                         'PCOA')
        self.assertEqual(repr(results.emperor.type), 'Visualization')


class TestUMAPMethod(TestPluginBase):

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

    def test_umap_runner(self):
        umap_kwargs = {'n_neighbors': 3}
        dm = distances(self.data, umap_args=umap_kwargs)
        self.assertEqual(dm.shape, (6, 6))

    def test_umap_aitchison(self):
        umap_kwargs = {'n_neighbors': 3}
        dm = distances(self.data, umap_metric='aitchison',
                       umap_args=umap_kwargs)
        self.assertEqual(dm.shape, (6, 6))


if __name__ == '__main__':
    unittest.main()
