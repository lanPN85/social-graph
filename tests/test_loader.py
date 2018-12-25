import unittest
import sys
sys.path.append('.')

from sgraph import loader


class LoaderTestCase(unittest.TestCase):
    def test_graph_load(self):
        g = loader.load_raw_graph('tests/data/12831.edges')
        self.assertEqual(2478, len(g.edges))
        self.assertTrue(g.has_edge(398874773, 652193))

    def test_graph_feats(self):
        g = loader.load_raw_graph('tests/data/12831.edges')
        feats = loader.add_node_feats(g, 'tests/data/12831.feat', 'tests/data/12831.featnames')
        self.assertEqual(len(feats), 1364)

if __name__ == "__main__":
    unittest.main()
