import sys
from pathlib import Path

from requests import Session, get
from requests.adapters import HTTPAdapter, Retry

from jetbrains_plugin_server.config import JETBRAINS_PLUGINS_HOST, LOCAL_DIR, PLUGIN_SPECS_DIR, PLUGIN_VERSIONS_DIR, PLUGINS_DIR


def dl_data(plugins: list[str]):
    """
    The argument values can be either:
     - plugins IDs: "631" (for python)
     - plugin id+name: "631-python"
     - plugin full url: "https://plugins.jetbrains.com/plugin/631-python",
    """
    if not LOCAL_DIR.exists():
        raise FileNotFoundError(f"The directory {LOCAL_DIR.as_posix()} is missing, "
                                f"please create it or specify another one using the env var 'LOCAL_DIR'")

    missing_dirs = []
    for d in [PLUGIN_VERSIONS_DIR, PLUGINS_DIR, PLUGIN_SPECS_DIR]:
        if not LOCAL_DIR.joinpath(d).exists():
            missing_dirs.append(d)

    if missing_dirs:
        raise FileNotFoundError(f"The directory(ies) {','.join([d.as_posix() for d in missing_dirs])} "
                                f"is(are) missing, please create it(the)")

    s = Session()
    retries = Retry(total=5, backoff_factor=0.1)
    s.mount('https://', HTTPAdapter(max_retries=retries))

    for plugin in plugins:
        print("PLUGIN", plugin)
        plugin = plugin.replace(f"{JETBRAINS_PLUGINS_HOST}/plugin/", "").strip("/").split("#", maxsplit=1)[0]
        plugin_id_int = plugin.split("-", maxsplit=1)[0]

        versions_rep = get(f"{JETBRAINS_PLUGINS_HOST}/plugins/list?pluginId={plugin}")
        LOCAL_DIR.joinpath(PLUGIN_SPECS_DIR, f"{plugin_id_int}.xml").write_bytes(
            versions_rep.content
        )

        versions_id_rep = get(f"{JETBRAINS_PLUGINS_HOST}/api/plugins/{plugin_id_int}/updateVersions")
        LOCAL_DIR.joinpath(PLUGIN_VERSIONS_DIR, f"{plugin_id_int}.json").write_bytes(
            versions_id_rep.content
        )

        for row in versions_id_rep.json()[:-50:-1]:
            print(f"   VERSION {row['version']:20s}", end="")
            sys.stdout.flush()
            plugin_version_id = row["id"]
            zip_file = LOCAL_DIR.joinpath(PLUGINS_DIR, f"{plugin_version_id}.zip")
            if zip_file.exists():
                print("   already done", plugin_version_id)
                continue

            dl = s.get(
                f"{JETBRAINS_PLUGINS_HOST}/plugin/download",
                params={"updateId": plugin_version_id},
                stream=True
            )
            zip_file.write_bytes(dl.content)
            print("   done in", dl.elapsed, plugin_version_id)


def main_cli():
    in_file = Path(sys.argv[1])
    if not in_file.exists():
        raise FileNotFoundError(
            "The given input should be a path to an existing file containing one plugin ID per line")
    dl_data(
        in_file.read_text().splitlines()
    )
