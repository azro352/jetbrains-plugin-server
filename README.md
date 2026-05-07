<!--

THIS README FILE IS RENDERED ON '/' ENDPOINT WHEN NO "build" ARG IS GIVEN

-->

Creates a jetbrains-compatible plugin server with a given list of plugins

## How-to use

### Download the data

Use the script `dl_data.py` to fetch plugins metadata and data from jetbrains server, and save them where you want

### Create the server

```python
from fastapi import FastAPI

from jetbrains_plugin_server import create_plugin_server
from jetbrains_plugin_server.model.data_listing import FSDataListing

app: FastAPI = create_plugin_server(
    FSDataListing("/data/myfolder"),
    "https://myendpoint/plugins/{plugin_version_id}"
)
```

Then deploy it like you want

### Use the server

Register the server [in your IDE][jb-custom-repo]

## Tools

- `jetbrains_plugin_server/tools/dl_data.py` to fetch plugins specifications, versions and content from jetbrains to a
  local filesystem
- `jetbrains_plugin_server/tools/gen_json_cache.py` to build a JSON cache to answer faster, using either a filesystem
  storage, an artifactory or an apache server

## Paths

- `/` to get the readme OR the compliant xml content if url param `build` is provided
- `/cache` to get the full JSON cache of the server
- `/packages` to get a nicer view of the available packages
- `/docs` the openapi spec of the app, provided by FastAPI

[jb-custom-repo]: https://www.jetbrains.com/help/idea/managing-plugins.html#add_plugin_repos
