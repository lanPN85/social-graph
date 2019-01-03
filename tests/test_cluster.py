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
        self.assertLessEqual(len(clusters), 8)

if __name__ == "__main__":
    unittest.main()
