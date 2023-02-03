from unittest import TestCase, skip

from src.crawler.instagram import InstaCrawler


class TestInstaCrawler(TestCase):
    @skip
    def test_get_follower(self):
        follower = InstaCrawler.get_follower(person_name="Anna Oxa")
        self.assertIsNotNone(follower)
        self.assertGreater(follower, 1000)
