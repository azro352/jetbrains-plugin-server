import json
from pathlib import Path

from src.config import PLUGIN_TEST_DATA
from src.schemas import CatalogSchema

import os

if os.getenv("TEST_MODE") == "true":
    def get_plugin_catalog():
        return CatalogSchema.model_validate(json.loads(PLUGIN_TEST_DATA.read_text()))
else:

    def get_plugin_catalog() -> CatalogSchema:
        return CatalogSchema.model_validate(json.loads(PLUGIN_TEST_DATA.read_text()))
