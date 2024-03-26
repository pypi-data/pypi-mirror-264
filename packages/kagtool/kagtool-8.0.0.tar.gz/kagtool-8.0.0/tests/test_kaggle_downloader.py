import unittest
from kaggle_downloader import KaggleDownloader

class TestKaggleDOwnloader(unittest.TestCase):
    def test_instantiate(self):
        downloader = KaggleDownloader('', '')

unittest.main()
