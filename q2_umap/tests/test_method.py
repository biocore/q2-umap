import io

import skbio
import pandas as pd
from biom.table import Table
from biom.util import biom_open
from q2_umap._method import distances, distances_phylogenetic
import q2_umap.tests.base as test_base


class TestUMAPDistances(test_base.TestCase):

    package = 'q2_umap.tests'

    def setUp(self):
        super(TestUMAPDistances, self).setUp()
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

    def test_umap_runner_no_args(self):
        dm = distances(self.data)
        self.assertEqual(dm.shape, (6, 6))

    def test_umap_callable_metric(self):
        def my_metric(x, y, **kwargs):
            return sum(x - y)
        umap_kwargs = {'n_neighbors': 3}
        dm = distances(self.data, umap_metric=my_metric,
                       umap_args=umap_kwargs)
        self.assertEqual(dm.shape, (6, 6))

    def test_umap_no_table_empty_error(self):
        data = pd.DataFrame([[0, 0], [0, 0]])
        with self.assertRaisesRegex(ValueError, r'is empty'):
            distances(data)

    def test_umap_unknown_metric_error(self):
        with self.assertRaisesRegex(ValueError, r'Unknown metric'):
            distances(self.data, umap_metric='unknown_metric')


class TestUMAPDistancesPhylogenetic(test_base.TestCase):

    package = 'q2_umap.tests'

    def setUp(self):
        super(TestUMAPDistancesPhylogenetic, self).setUp()
        data_table = pd.DataFrame([[1, 2, 0, 4],
                                   [1, 4, 3, 5],
                                   [0, 0, 1, 2],
                                   [0, 1, 2, 1],
                                   [1, 2, 2, 0],
                                   [0, 1, 1, 0]],
                                  index=['S1', 'S2', 'S3', 'S4', 'S5', 'S6'],
                                  columns=['O1', 'O2', 'O3', 'O4'])

        data = Table(data_table.values.T,
                     data_table.columns,
                     data_table.index)
        tree = skbio.TreeNode.read(io.StringIO(
            '((O1:0.25, (O4:0.25, O2:0.50):0.1):0.25, O3:0.75)root;'))

        self.table_path = self.create_data_path('table.biom')
        self.tree_path = self.create_data_path('tree.newick')

        with biom_open(self.table_path, 'w') as f:
            data.to_hdf5(f, "test_example")
        tree.write(self.tree_path)

    def test_umap_phylogenetic(self):
        umap_kwargs = {'n_neighbors': 3}
        dm = distances_phylogenetic(self.table_path, self.tree_path,
                                    umap_metric='unweighted_unifrac',
                                    umap_args=umap_kwargs)
        self.assertEqual(dm.shape, (6, 6))

    def test_umap_phylogenetic_no_args(self):
        dm = distances_phylogenetic(self.table_path, self.tree_path,
                                    'unweighted_unifrac')
        self.assertEqual(dm.shape, (6, 6))

