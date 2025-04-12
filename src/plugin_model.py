from pathlib import Path

import markdown


def get_plugins(build: str):
    if not build:
        md = Path(__file__).parent.parent.joinpath("README.md").read_text()
        return markdown.markdown(md)
    return [
        {"foo": "var"}
    ]
