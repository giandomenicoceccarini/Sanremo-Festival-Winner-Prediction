from unittest import TestCase

from src.data_loader.load_dataset import DataLoader


class TestDataLoad(TestCase):
    def test_dataset_loader(self):
        df = DataLoader('../data').load()
        self.assertIsNotNone(df)
        self.assertGreater(df.shape[0], 1)
