import json
from pathlib import Path

from requests import get
import xml.etree.ElementTree as ET

from src.config import PLUGIN_TEST_DATA
from src.schemas import CatalogSchema, PluginSchema, PluginVersionSchema, PluginVersionSpecSchema

PLUGINS: list[str] = [
    "https://plugins.jetbrains.com/plugin/631-python",
    "https://plugins.jetbrains.com/plugin/10080-rainbow-brackets",
    "https://plugins.jetbrains.com/plugin/11938-one-dark-theme",
    "https://plugins.jetbrains.com/plugin/9525--env-files",
    "https://plugins.jetbrains.com/plugin/11938-one-dark-theme",
    "https://plugins.jetbrains.com/plugin/15075-jpa-buddy",
    "https://plugins.jetbrains.com/plugin/9525--env-files-support/",
    "https://plugins.jetbrains.com/plugin/10044-atom-material-icons/",
    "https://plugins.jetbrains.com/plugin/164-ideavim",
    "https://plugins.jetbrains.com/plugin/9792-key-promoter-x",
    "https://plugins.jetbrains.com/plugin/14708-mario-progress-bar",
    "https://plugins.jetbrains.com/plugin/7086-acejump"
]

if __name__ == '__main__':

    result: CatalogSchema = CatalogSchema()

    for plugin in PLUGINS:
        plugin = plugin.replace("https://plugins.jetbrains.com/plugin/", "").strip("/")
        plugin_id_int = plugin.split("-", maxsplit=1)[0]
        versions_id_rep = get(f"https://plugins.jetbrains.com/api/plugins/{plugin_id_int}/updateVersions")
        versions_to_plugin_version_id = {
            row["version"]: row["id"]
            for row in versions_id_rep.json()
        }

        versions_rep = get(f"https://plugins.jetbrains.com/plugins/list?pluginId={plugin}")
        root = ET.fromstring(versions_rep.content)

        result.plugins.append(PluginSchema(
            name=plugin,
            versions=[
                PluginVersionSchema(
                    plugin_id=version.find("id").text,
                    plugin_version_id=versions_to_plugin_version_id[version.find("version").text],
                    version=version.find("version").text,
                    specs=PluginVersionSpecSchema(
                        **{k: v for k, v in version.find("idea-version").items() if v != "n/a"}
                    )
                )
                for version in root.find("category").findall("idea-plugin")

            ]
        ))
        print(f"Plugin {plugin} found {len(result.plugins[-1].versions)} versions")

    PLUGIN_TEST_DATA.write_text(json.dumps(result.model_dump(by_alias=True), indent=4))
