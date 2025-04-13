import json
from pathlib import Path

from src.schemas import CatalogSchema

import os

if os.getenv("TEST_MODE") == "true":
    def get_plugin_catalog():
        test_catalog_path = Path(__file__).parent.parent.joinpath("tests", "data", "plugins_test.json")
        return CatalogSchema.model_validate(json.loads(test_catalog_path.read_text()))
else:

    def get_plugin_catalog() -> CatalogSchema:
        test_catalog_path = Path(__file__).parent.parent.joinpath("tests", "data", "plugins_test.json")
        return CatalogSchema.model_validate(json.loads(test_catalog_path.read_text()))
