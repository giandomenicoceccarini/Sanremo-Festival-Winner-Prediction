from unittest import TestCase

from src.crawler.wikipedia import WikiCrawler


class TestWikiCrawler(TestCase):
    def test_get_info(self):
        info = WikiCrawler.get_artist_info(person_name="Marco Mengoni")
        self.assertIsNotNone(info)
