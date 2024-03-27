from importlib import metadata

try:
    __version__ = metadata.version("pgtui")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"
