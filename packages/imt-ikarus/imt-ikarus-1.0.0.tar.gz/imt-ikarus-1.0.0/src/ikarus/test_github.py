from ikarus import github


def test_download_from_repo():
    icon_svg = "docs/img/icon.svg"
    path_on_disk = github.download(icon_svg, "SimiPixel", "ring", "main")

    assert path_on_disk.exists() and path_on_disk.is_file()
