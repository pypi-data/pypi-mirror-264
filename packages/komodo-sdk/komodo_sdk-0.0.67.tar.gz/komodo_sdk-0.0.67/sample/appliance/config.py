from pathlib import Path

from komodo.framework.komodo_config import KomodoConfig


class ApplianceConfig(KomodoConfig):
    def get_serpapi_key(self):
        return self.get_secret("SERP_API_KEY")


class LocalConfig(ApplianceConfig):
    def __init__(self):
        folder = Path(__file__).parent.parent.resolve()
        super().__init__(data_directory=folder / "data" / "komodo")
