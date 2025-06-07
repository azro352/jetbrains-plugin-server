import os

os.environ["TEST_MODE"] = "true"

from src.config import LOCAL
from src.model.data_listing import FSDataListing
from src.tools.gen_json_cache import gen_json_cache

if __name__ == '__main__':
    dl = FSDataListing(LOCAL)

    gen_json_cache(dl, only_available_plugins=False)
