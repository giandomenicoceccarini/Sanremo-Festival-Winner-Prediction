from unittest import TestCase, skip

from src.crawler.wikipedia import WikiCrawler


class TestWikiCrawler(TestCase):
    @skip
    def test_get_info(self):
        info = WikiCrawler.get_artist_info(person_name="Marco Mengoni")
        self.assertIsNotNone(info)
