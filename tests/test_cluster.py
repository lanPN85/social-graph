import unittest
import sys
sys.path.append('.')

from sgraph import conversions, loader, cluster


class ClusterTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = loader.load_raw_graph('tests/data/477094958.edges')
        cls.graph = conversions.naive_conversion(cls.graph)

    def test_laplacian(self):
        clusters = cluster.laplacian_cluster(self.graph, partitions=8)
        self.assertIsNotNone(clusters)
        self.assertIsInstance(clusters[0], list)
        self.assertIsInstance(clusters[0][0], int)
        self.assertLessEqual(len(clusters), 8)

    def test_gn(self):
        clusters = cluster.girvan_newman(self.graph, partitions=4)
        self.assertIsNotNone(clusters)
        self.assertIsInstance(clusters[0], list)
        self.assertIsInstance(clusters[0][0], int)


if __name__ == "__main__":
    unittest.main()
