from unittest import TestCase

from src.plugin_model import get_plugins


class TestPlugin(TestCase):

    def test_no_build_arg(self):
        content = get_plugins("")
        self.assertIsInstance(content, str)

    def test_a(self):
        self.assertTrue(True)
