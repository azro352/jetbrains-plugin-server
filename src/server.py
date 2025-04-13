from pathlib import Path

import markdown
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response

from src.plugin_model import get_plugins
from src.to_xml import to_xml


def create_app():
    app = FastAPI()

    @app.get("/")
    def get_plugins_route(build: str = ""):
        if not build:
            md = Path(__file__).parent.parent.joinpath("README.md").read_text()
            return HTMLResponse(content=markdown.markdown(md))

        result = get_plugins(build)
        return Response(content=to_xml(result), media_type="application/xml")

    return app
