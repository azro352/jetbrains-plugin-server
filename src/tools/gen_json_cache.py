import json
import xml.etree.ElementTree as ET
from pathlib import Path

from src.config import PLUGIN_TEST_DATA, PLUGIN_SPECS_DIR, PLUGIN_VERSIONS_DIR, LOCAL
from src.model.data_listing import ArtifactoryDataListing, FSDataListing
from src.schemas import CatalogSchema, PluginSchema, PluginVersionSchema, PluginVersionSpecSchema

if __name__ == '__main__':

    dl = ArtifactoryDataListing("", "")
    dl = FSDataListing(LOCAL)

    result: CatalogSchema = CatalogSchema()

    for plugin in dl.list(PLUGIN_SPECS_DIR):
        plugin_id_int = plugin.split(".", maxsplit=1)[0]

        versions_to_plugin_version_id = {
            row["version"]: row["id"]
            for row in json.loads(dl.get(PLUGIN_VERSIONS_DIR, f"{plugin_id_int}.json"))
        }

        plugin_spec = dl.get(PLUGIN_SPECS_DIR, plugin)

        root = ET.fromstring(plugin_spec)

        versions = root.find("category").findall("idea-plugin")

        result.plugins.append(PluginSchema(
            name=versions[0].find("name").text,
            versions=[
                PluginVersionSchema(
                    plugin_id=version.find("id").text,
                    plugin_version_id=versions_to_plugin_version_id[version.find("version").text],
                    version=version.find("version").text,
                    specs=PluginVersionSpecSchema(
                        **{k: v for k, v in version.find("idea-version").items() if v != "n/a"}
                    )
                )
                for version in versions
            ]
        ))
        print(f"Plugin {plugin} found {len(result.plugins[-1].versions)} versions")

    PLUGIN_TEST_DATA.write_text(json.dumps(result.model_dump(by_alias=True), indent=4))
