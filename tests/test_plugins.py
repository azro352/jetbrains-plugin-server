import os
from unittest import TestCase

os.environ["TEST_MODE"] = "true"

from src.plugin_model import get_plugins

"""
for c in content:
    print(f'self.assertPluginExists(content, "{c[0]}", "{c[1].version}")')
"""


class TestPlugin(TestCase):

    def test_one(self):
        content = get_plugins("243.26053")
        self.assertEquals(len(content), 4)

        self.assertPluginExists(content, "631-python", "243.26053.27")
        self.assertPluginExists(content, "10080-rainbow-brackets", "2024.2.10-241")
        self.assertPluginExists(content, "11938-one-dark-theme", "5.13.0")
        self.assertPluginExists(content, "9525--env-files", "2024.3")

    def test_two(self):
        content = get_plugins("222.4554.15")
        self.assertEquals(len(content), 4)

        self.assertPluginExists(content, "631-python", "222.4554.10")
        self.assertPluginExists(content, "10080-rainbow-brackets", "2023.3.7-ij")
        self.assertPluginExists(content, "11938-one-dark-theme", "5.13.0")
        self.assertPluginExists(content, "9525--env-files", "2022.2")

    def assertPluginExists(self, plugins, name, version):
        for pname, pvs in plugins:
            if pname == name:
                self.assertEquals(pvs.version, version, f"Invalid version for plugin {name}")
                break
        else:
            self.fail(f"Plugin {name} not found")
