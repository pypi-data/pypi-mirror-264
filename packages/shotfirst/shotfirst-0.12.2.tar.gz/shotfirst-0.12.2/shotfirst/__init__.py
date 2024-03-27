from importlib import metadata

__version__ = metadata.version("shotfirst")
__desc__ = metadata.metadata("shotfirst")["Summary"]
