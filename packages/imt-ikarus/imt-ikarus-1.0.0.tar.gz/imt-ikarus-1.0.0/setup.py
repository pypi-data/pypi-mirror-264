import fnmatch
import os

import setuptools


def find_data_files(package_dir, patterns, excludes=()):
    """Recursively finds files whose names match the given shell patterns."""
    paths = set()

    def is_excluded(s):
        for exclude in excludes:
            if fnmatch.fnmatch(s, exclude):
                return True
        return False

    for directory, _, filenames in os.walk(package_dir):
        if is_excluded(directory):
            continue
        for pattern in patterns:
            for filename in fnmatch.filter(filenames, pattern):
                # NB: paths must be relative to the package directory.
                relative_dirpath = os.path.relpath(directory, package_dir)
                full_path = os.path.join(relative_dirpath, filename)
                if not is_excluded(full_path):
                    paths.add(full_path)
    return list(paths)


baselines_requires = ["onnxruntime", "ring @ git+https://github.com/SimiPixel/ring.git"]
benchmark_requires = ["ring @ git+https://github.com/SimiPixel/ring.git"]

setuptools.setup(
    name="ikarus",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    version="1.0.0",
    package_data={
        "ikarus": find_data_files(
            package_dir="src/ikarus",
            patterns=["*.xml", "*.onnx"],
            excludes=[],
        ),
    },
    include_package_data=True,
    install_requires=[
        "numpy",
        "qmt",
        "scipy",
        "dm-tree",
        "wget",
        "requests",
        "pandas",
        "tree_utils @ git+https://github.com/SimiPixel/tree_utils.git",
    ],
    extras_require={
        "benchmark": benchmark_requires,
        "baselines": baselines_requires,
    },
)
