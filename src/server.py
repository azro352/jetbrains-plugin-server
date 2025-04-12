from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from src.plugin_model import get_plugins


def create_app():
    app = FastAPI()

    @app.get("/")
    def get_plugins_route(build: str = ""):
        result = get_plugins(build)
        if isinstance(result, str):
            return HTMLResponse(content=result)
        return result

    return app
