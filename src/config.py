import os
from pathlib import Path

DL_URL_BASE = os.getenv("DL_URL_BASE", "https://fake.url/{plugin_version_id}")

PLUGIN_TEST_DATA = Path(__file__).parent.parent.joinpath("tests", "data", "plugins_test.json")
