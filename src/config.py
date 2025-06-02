import os
from pathlib import Path

DL_URL_BASE = os.getenv("DL_URL_BASE", "https://fake.url/{plugin_version_id}")

JETBRAINS_PLUGINS_HOST = "https://plugins.jetbrains.com"

LOCAL = Path(__file__).parent.parent.joinpath("local")

PLUGIN_TEST_DATA = Path(__file__).parent.parent.joinpath("tests", "data", "plugins_test.json")

PLUGIN_SPECS_DIR = "plugin_specs"
PLUGIN_VERSIONS_DIR = "plugin_versions"
PLUGINS_DIR = "plugins"
