import json
from pathlib import Path

from requests import get
import xml.etree.ElementTree as ET

from src.schemas import CatalogSchema, PluginSchema, PluginVersionSchema, PluginVersionSpecSchema

PLUGINS: list[str] = [
    "631-python",
    "10080-rainbow-brackets",
    "11938-one-dark-theme",
    "9525--env-files"
]

if __name__ == '__main__':
    output = Path(__file__).parent.joinpath("data", "plugins_test_2.json")

    result: CatalogSchema = CatalogSchema()

    for plugin in PLUGINS:
        versions_rep = get(f"https://plugins.jetbrains.com/plugins/list?pluginId={plugin}")
        root = ET.fromstring(versions_rep.content)

        result.plugins.append(PluginSchema(
            name=plugin,
            versions=[
                PluginVersionSchema(
                    id=version.find("id").text,
                    version=version.find("version").text,
                    specs=PluginVersionSpecSchema(
                        **{k: v for k, v in version.find("idea-version").items() if v != "n/a"}
                    )
                )
                for version in root.find("category").findall("idea-plugin")

            ]
        ))
        print(f"Plugin {plugin} found {len(result.plugins[-1].versions)} versions")

    output.write_text(json.dumps(result.model_dump(by_alias=True), indent=4))
