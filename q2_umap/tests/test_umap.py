import unittest
from unittest import TestCase
import numpy as np
import pandas as pd
import pandas.testing as pdt
from skbio.stats.distance import DistanceMatrix
from skbio.stats.ordination import OrdinationResults
from q2_umap.umap import embed, center


class UMAPTests(TestCase):
    def setUp(self):
        self.test_dm = DistanceMatrix(
            np.array([
                [0, 1, 2, 3, 4],
                [1, 0, 4, 5, 6],
                [2, 4, 0, 6, 7],
                [3, 5, 6, 0, 8],
                [4, 6, 7, 8, 0],
            ]),
            ids=[f'S{i}' for i in range(5)],
        )

        n_samples = 100
        np.random.seed(825)
        sample_embedding = np.random.normal(size=(n_samples, 3)) + 2
        sample_embedding[:, 1] *= 3
        sample_embedding[:, 2] *= 6
        sample_df = pd.DataFrame(sample_embedding,
                                 index=[f'S{i}' for i in range(n_samples)],
                                 columns=[f'C{i}' for i in range(3)],
                                 )

        self.test_ord_results = OrdinationResults(
            'foo',
            'bar',
            eigvals=pd.Series(np.arange(n_samples)),
            samples=sample_df,
        )

    def test_embed(self):
        ord = embed(self.test_dm, n_neighbors=3)
        self.assertTupleEqual(
            (5, 3),
            ord.samples.shape,
        )
        self.assertTrue(ord.proportion_explained)

    def test_embed_more_n_neighbors(self):
        ord = embed(self.test_dm, n_neighbors=5)
        self.assertTupleEqual(
            (5, 3),
            ord.samples.shape,
        )

    def test_embed_2d(self):
        ord = embed(
            self.test_dm,
            number_of_dimensions=2,
            n_neighbors=3,
        )
        self.assertTupleEqual(
            (5, 3),
            ord.samples.shape,
        )
        self.assertAlmostEqual(
            0,
            ord.samples.iloc[:, 2].sum()
        )

    def test_center(self):
        ord = center(self.test_ord_results)
        ord_df = ord.samples
        pdt.assert_index_equal(ord_df.index,
                               self.test_ord_results.samples.index)
        pdt.assert_index_equal(ord_df.columns,
                               self.test_ord_results.samples.columns)
        self.assertAlmostEqual(0, ord_df.values.mean())
        stdevs = ord_df.std()
        self.assertGreater(stdevs[0], stdevs[1])
        self.assertGreater(stdevs[1], stdevs[2])


if __name__ == "__main__":
    unittest.main()
