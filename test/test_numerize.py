from unittest import TestCase
from src.numerizor.numerize import numerize


class TestNumerize(TestCase):
    def test_numerize(self):
        self.assertEqual(numerize('10'), 10)
        self.assertEqual(numerize('1K'), 1000)
        self.assertEqual(numerize('3M'), 3000000)
