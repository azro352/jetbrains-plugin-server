import xml.etree.ElementTree as EltT
from io import BytesIO

from jetbrains_plugin_server.schemas import PluginVersionSchema

DL_PLACEHOLDER = "{plugin_version_id}"


def to_xml(plugins: list[tuple[str, PluginVersionSchema]], download_url_root: str) -> bytes:
    if DL_PLACEHOLDER not in download_url_root:
        raise ValueError(f"Invalid download_url_root, it should contain the placeholder {DL_PLACEHOLDER}")

    a = EltT.Element('plugins')
    for name, plugin in plugins:
        p = EltT.SubElement(a, 'plugin', {
            "id": plugin.plugin_id,
            # url of download
            "url": download_url_root.format(plugin_version_id=plugin.plugin_version_id),
            "version": plugin.version
        })
        attrs = {"since-build": plugin.specs.since_build}
        if ub := plugin.specs.until_build:
            attrs["until-build"] = ub

        EltT.SubElement(p, 'name').text = name
        EltT.SubElement(p, 'description').text = plugin.description
        EltT.SubElement(p, 'change-notes').text = plugin.change_notes

    bio = BytesIO()
    EltT.ElementTree(a).write(bio)
    bio.seek(0)
    return b"<?xml version='1.0' encoding='UTF-8'?>" + bio.read()
