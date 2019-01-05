import unittest
import sys
sys.path.append('.')

from sgraph import conversions, loader


class ConversionTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = loader.load_raw_graph('tests/data/12831.edges')

    def test_naive(self):
        gx = conversions.naive_conversion(self.graph)

    def test_transpose(self):
        gx = conversions.transpose_symmetric_conversion(self.graph)

    def test_rw(self):
        gx = conversions.random_walk_symmetric_conversion(self.graph)

    def test_biblio(self):
        gx = conversions.biblio_symmetric_conversion(self.graph)

if __name__ == "__main__":
    unittest.main()
