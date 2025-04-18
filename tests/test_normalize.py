from unittest import TestCase

from parameterized import parameterized

from src.schemas import normalize_version


class TestNormalize(TestCase):

    @parameterized.expand([
        ["1", "1.0.0"],
        ["1.0", "1.0.0"],
        ["1.0.0", "1.0.0"],
    ])
    def test_normalize_start(self, version, expected):
        self.assertEquals(normalize_version(version, "start"), expected)

    @parameterized.expand([
        ["1", "1.9999.9999"],
        ["1.123", "1.123.9999"],
        ["1.123.456", "1.123.456"],
    ])
    def test_normalize_end(self, version, expected):
        self.assertEquals(normalize_version(version, "end"), expected)
