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
        dm = distances(self.data, metric='aitchison',
                       umap_args=umap_kwargs)
        self.assertEqual(dm.shape, (6, 6))


if __name__ == '__main__':
    unittest.main()
