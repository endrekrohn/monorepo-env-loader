import logging
import os
import sys
from typing import Any, TypeAlias
import tomli

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

GRN = "\x1b[1;32m"
YLW = "\x1b[33;20m"
BRD = "\x1b[31;1m"
CLR = "\x1b[0m"
BLU = "\x1b[1;34m"

_KeyValPair: TypeAlias = "dict[tuple[str, ...], str]"
_FileKeyValPair: TypeAlias = "dict[tuple[str], list[tuple[str, str]]]"


def flatten_dict(y: dict) -> _KeyValPair:
    out = {}

    def flatten(x: dict | tuple | Any, name: tuple[str, ...] = tuple()):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + (a,))
        elif type(x) is list:
            for a in x:
                if type(a) is str:
                    flatten(a, name + (a,))
        else:
            out[name] = x

    flatten(y)
    return out


def get_by_file(pairs: _KeyValPair) -> _FileKeyValPair:
    out: _FileKeyValPair = {}
    for k, v in pairs.items():
        file = k[:-1]
        key = k[-1]
        if out.get(file) is None:
            out[file] = []
        out[file].append((key, v))
    return out


def read_file(path: str) -> dict[str, Any]:
    error = None
    if not path.endswith(".toml"):
        error = f"Type of file must be a '.toml'. Were given '{path}'"
    elif not os.path.isfile(path):
        error = f"File not found at location '{path}'"
    if error is not None:
        logger.error(BRD + error + CLR)
        sys.exit(1)
    logger.info(
        f"Initializing environment variables with the file: '{BLU + path + CLR}'"
    )
    with open(path, mode="rb") as fp:
        return tomli.load(fp)


def main(path: str):
    config = read_file(path)

    flat = get_by_file(flatten_dict(config))
    for k, l in flat.items():
        dir = "./" + "/".join(k[:-1])
        path = "./" + "/".join(k)
        if not os.path.isdir(dir):
            logger.warning(
                YLW + f"- Folder not found. Could not write to '{path}'" + CLR
            )
            continue
        with open(path, "w") as f:
            lines = [f"{v[0]}={v[1]}" for v in l]
            f.writelines("\n".join(lines))
    logger.info(GRN + "Added credentials! 🔑" + CLR)


if __name__ == "__main__":
    path = "env.toml"
    if len(sys.argv) > 1:
        path = sys.argv[1]
    main(path)
