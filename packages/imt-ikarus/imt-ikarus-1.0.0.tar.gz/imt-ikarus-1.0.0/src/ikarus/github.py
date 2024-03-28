from pathlib import Path
from typing import Optional

import requests
import wget


def listdir(
    user: str,
    repo: str,
    branch: str,
    filter_prefix: Optional[str] = None,
    filter_suffix: Optional[str] = None,
    recursive: bool = True,
) -> list[str]:

    url = (
        f"https://api.github.com/repos/{user}/{repo}/"
        f"git/trees/{branch}?recursive={int(recursive)}"
    )
    resp = requests.get(url).json()
    files = [ele["path"] for ele in resp["tree"]]

    if filter_prefix is not None:
        files = [file for file in files if file[: len(filter_prefix)] == filter_prefix]

    if filter_suffix is not None:
        files = [
            file
            for file in files
            if file[-len(filter_suffix) :] == filter_suffix  # noqa: E203
        ]

    return files


def download(
    path_in_repo: str,
    user: str,
    repo: str,
    branch: str,
    path_to_cache: str = "~/.ikarus_cache",
) -> Path:
    "Download file from Github repo. Returns path on disk."
    path_on_disk = Path(path_to_cache).expanduser().joinpath(path_in_repo)
    if not path_on_disk.exists():
        path_on_disk.parent.mkdir(parents=True, exist_ok=True)
        url = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path_in_repo}"
        print(f"Downloading file from url {url}.. (this might take a moment)")
        wget.download(url, out=str(path_on_disk.parent))
        print(
            f"Downloading finished. Saved to location {path_on_disk}. "
            f"All downloaded files can be deleted by removing folder {path_to_cache}."
        )
    return path_on_disk
