import io

import skbio
import pandas as pd
import q2_umap.tests.base as test_base
import pandas.testing as pdt
from qiime2 import Metadata, Artifact
from qiime2.plugin.testing import TestPluginBase


class TestUMAPPipeline(TestPluginBase):

    package = 'q2_umap.tests'

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
        self.assertEqual(len(results), 4)

    def test_pipeline_rarefied_table_no_rarefy(self):
        table = Artifact.import_data('FeatureTable[Frequency]', self.data)
        results = self.pipeline(table, metadata=self.metadata,
                                umap_args="{'n_neighbors': 3}")
        self.assertEqual(repr(results.rarefied_table.type),
                         'FeatureTable[Frequency]')
        raw_table = table.view(pd.DataFrame)
        no_rarefy_table = results.rarefied_table.view(pd.DataFrame)
        pdt.assert_frame_equal(raw_table, no_rarefy_table)

    def test_pipeline_rarefied_table_with_rarefy(self):
        table = Artifact.import_data('FeatureTable[Frequency]', self.data)
        sampling_depth = 2
        results = self.pipeline(table, metadata=self.metadata,
                                umap_args="{'n_neighbors': 3}",
                                sampling_depth=sampling_depth)
        self.assertEqual(repr(results.rarefied_table.type),
                         'FeatureTable[Frequency]')
        rarefied_table = results.rarefied_table.view(pd.DataFrame)
        sample_sums = rarefied_table.sum(axis='columns')
        self.assertTrue((sample_sums == sampling_depth).all())

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


class TestUMAPDistancesPlugin(TestPluginBase):
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


class TestUMAPDistancesPhylogeneticPlugin(TestPluginBase, test_base.TestCase):
    package = 'q2_umap'

    def setUp(self):
        TestPluginBase.setUp(self)
        test_base.TestCase.setUp(self)
        self.data = pd.DataFrame([[1, 2, 0, 4],
                                  [1, 4, 3, 5],
                                  [0, 0, 1, 2],
                                  [0, 1, 2, 1],
                                  [1, 2, 2, 0],
                                  [0, 1, 1, 0]],
                                 index=['S1', 'S2', 'S3', 'S4', 'S5',
                                        'S6'],
                                 columns=['O1', 'O2', 'O3', 'O4'])
        self.tree = skbio.TreeNode.read(io.StringIO(
            '((O1:0.25, (O4:0.25, O2:0.50):0.1):0.25, O3:0.75)root;'))
        self.metadata = Metadata(
            pd.DataFrame({'foo': ['1', '2', '3', '4', '5', '6']},
                         index=pd.Index(
                             ['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
                             name='id')))
        self.distance = self.plugin.methods['distances_phylogenetic']

    def test_distances(self):
        table = Artifact.import_data('FeatureTable[Frequency]', self.data)
        tree = Artifact.import_data('Taxonomy[Rooted]', self.tree)
        results = self.distance(table, tree, 'unweighted_unifrac',
                                umap_args="{'n_neighbors': 3}")
        self.assertEqual(repr(results.distance_matrix.type), 'DistanceMatrix')
