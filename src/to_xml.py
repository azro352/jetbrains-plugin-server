import xml.etree.ElementTree as ET
from io import BytesIO

from src.config import DL_URL_BASE
from src.schemas import PluginVersionSchema


def to_xml(plugins: list[tuple[str, PluginVersionSchema]]):
    a = ET.Element('plugins')
    for name, plugin in plugins:
        p = ET.SubElement(a, 'plugin', {
            "id": plugin.plugin_id,
            # url of download
            "url": DL_URL_BASE.format(plugin_version_id=plugin.plugin_version_id),
            "version": plugin.version
        })
        attrs = {"since-build": plugin.specs.since_build, }
        if ub := plugin.specs.until_build:
            attrs["until-build"] = ub
        iv = ET.SubElement(p, 'idea-version', attrs)

    bio = BytesIO()
    ET.ElementTree(a).write(bio)
    bio.seek(0)
    return b"<?xml version='1.0' encoding='UTF-8'?>" + bio.read()
