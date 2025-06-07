import logging
from pathlib import Path
from typing import Annotated

import markdown

from src.config import FAST_API_OFFLINE

if FAST_API_OFFLINE:
    from fastapi_offline import FastAPIOffline as FastAPI
else:
    from fastapi import FastAPI  # type: ignore

from fastapi.responses import HTMLResponse, Response

from src.plugin_catalog import get_plugin_catalog
from src.plugin_model import get_plugins
from src.to_xml import to_xml

LOG = logging.getLogger(__name__)


def create_app():
    app = FastAPI()

    @app.get("/")
    def get_plugins_route(build: Annotated[str, "IDE build number to filter the available plugins and return only the compatible ones"] = ""):
        if not build:
            md = Path(__file__).parent.parent.joinpath("README.md").read_text()
            return HTMLResponse(content=markdown.markdown(md))

        LOG.debug("Request with build=%s", build)
        result = get_plugins(build)
        return Response(content=to_xml(result), media_type="application/xml")

    @app.get("/cache")
    def get_cache_route():
        return get_plugin_catalog()

    return app
