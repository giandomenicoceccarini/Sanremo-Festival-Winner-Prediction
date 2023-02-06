from unittest import TestCase

from src.google_trends.g_trends import GTrends


class TestGTrends(TestCase):
    def test_get_trends(self):
        trends = GTrends(["Anna Oxa", "Marco Mengoni"], smooth=True)
        self.assertIsNotNone(trends.trends)
        print(trends.trends)
