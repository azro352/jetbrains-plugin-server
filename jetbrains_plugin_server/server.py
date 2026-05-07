import logging
import re
from importlib.metadata import PackageNotFoundError, metadata
from typing import Annotated

import markdown

from jetbrains_plugin_server.config import FAST_API_OFFLINE
from jetbrains_plugin_server.homepage import get_favicon, get_homepage

if FAST_API_OFFLINE:
    from fastapi_offline import FastAPIOffline as FastAPI
else:
    from fastapi import FastAPI  # type: ignore

from fastapi.responses import HTMLResponse, Response

from jetbrains_plugin_server.model import packages
from jetbrains_plugin_server.model.data_listing import DataListing
from jetbrains_plugin_server.model.errors import add_error_handler
from jetbrains_plugin_server.plugin_catalog import get_plugin_catalog
from jetbrains_plugin_server.plugin_model import get_plugins
from jetbrains_plugin_server.to_xml import to_xml
from jetbrains_plugin_server.tools.gen_json_cache import gen_json_cache

LOG = logging.getLogger(__name__)


def create_plugin_server(dl: DataListing, download_url_root: str):
    gen_json_cache(dl)

    app = FastAPI()
    add_error_handler(app)
    app.include_router(packages.router)

    @app.get("/")
    def get_plugins_route(build: Annotated[
        str, "IDE build number to filter the available plugins and return only the compatible ones"] = ""):
        if not build:
            return HTMLResponse(content=get_homepage())

        LOG.debug("Request with build=%s", build)
        result = get_plugins(build)
        return Response(content=to_xml(result, download_url_root), media_type="application/xml")

    @app.get("/cache")
    def get_cache_route():
        return get_plugin_catalog()

    @app.get("/favicon.ico")
    def get_favicon_route():
        return Response(
            content=get_favicon(),
            media_type="image/x-icon"
        )

    return app
