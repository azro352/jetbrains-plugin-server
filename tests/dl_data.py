import json
from pathlib import Path

from requests import get
import xml.etree.ElementTree as ET

from src.plugin_catalog import get_plugin_catalog
from src.schemas import CatalogSchema, PluginSchema, PluginVersionSchema, PluginVersionSpecSchema

LOCAL = Path(__file__).parent.parent.joinpath("local")

if __name__ == '__main__':
    result: CatalogSchema = get_plugin_catalog()

    for plugin in result.plugins:
        for version in plugin.versions:
            print("DO", version.plugin_id, version.version, version.plugin_version_id)
            dl = get(
                "https://plugins.jetbrains.com/plugin/download",
                params={"updateId": version.plugin_version_id}
            )

            print("Done in ", dl.elapsed)

            LOCAL.joinpath(f"plugin_{version.plugin_version_id}.zip").write_bytes(
                dl.content
            )

            input("again ?")
