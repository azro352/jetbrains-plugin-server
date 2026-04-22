import os

os.environ["TEST_MODE"] = "true"

from jetbrains_plugin_server.config import LOCAL_DIR
from jetbrains_plugin_server.model.data_listing import FSDataListing
from jetbrains_plugin_server.tools.gen_json_cache import gen_json_cache

if __name__ == '__main__':
    dl = FSDataListing(LOCAL_DIR)

    gen_json_cache(dl, only_available_plugins=False)
