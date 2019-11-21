import unittest
import pandas as pd
from q2_umap._method import distances


class TestUMAPMethod(unittest.TestCase):

    def setUp(self):
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
