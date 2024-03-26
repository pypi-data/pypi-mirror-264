import os
from pathlib import Path

from komodo.framework.komodo_locations import KomodoLocations


class KomodoConfig:

    def __init__(self, data_directory=None, **kwargs):
        self.data_directory = data_directory
        self.kwargs = kwargs

    def data_dir(self) -> Path:
        if self.data_directory:
            return Path(self.data_directory)

        path = os.getenv("KOMODO_DATA_DIR", "/data/komodo")
        if not os.path.exists(path):
            if os.path.exists("./data/komodo"):
                path = "./data/komodo"

        if not os.path.exists(path):
            raise Exception("Default data directory not found. Please set KOMODO_DATA_DIR environment variable.")

        return Path(path)

    def locations(self) -> KomodoLocations:
        return KomodoLocations(self.data_dir())

    def get_secret(self, name, default=None) -> str:
        if name in self.kwargs:
            return self.kwargs[name]

        if name not in os.environ and default is None:
            raise Exception(f"{name} not found in environment.")

        return os.getenv(name, default)
