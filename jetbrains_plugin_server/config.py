import os
from pathlib import Path

JETBRAINS_PLUGINS_HOST = "https://plugins.jetbrains.com"

LOCAL_DIR = Path(os.getenv(
    "LOCAL_DIR",
    Path(__file__).parent.parent.joinpath("local").as_posix()
))

PLUGIN_PROD_DATA = Path(__file__).parent.parent.joinpath("plugins_prod.json")

PLUGIN_TEST_DATA = Path(__file__).parent.parent.joinpath("tests", "data", "plugins_test.json")

PLUGIN_SPECS_DIR = "plugin_specs"
PLUGIN_VERSIONS_DIR = "plugin_versions"
PLUGINS_DIR = "plugins"


def is_test_mode() -> bool:
    return os.getenv("TEST_MODE") == "true"


FAST_API_OFFLINE = os.getenv("FAST_API_OFFLINE") == "true"
