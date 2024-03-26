import os
from pathlib import Path

from komodo.framework.komodo_config import KomodoConfig


class TestConfig(KomodoConfig):
    PATH = os.path.dirname(__file__)

    def data_dir(self) -> Path:
        return Path(self.PATH)

    def get_mongo_url(self):
        return self.get_secret('MONGO_URL', "mongodb://root:example@localhost:27017/")

    def get_elastic_url(self):
        return self.get_secret("ELASTIC_URL", "http://localhost:9200")

    def get_authorized_indexes(self):
        return ["test-*"]

    def get_serpapi_key(self):
        self.get_secret('SERP_API_KEY')


if __name__ == "__main__":
    print(TestConfig.PATH)
    print(TestConfig().locations().available_appliances())
    print(TestConfig().locations().available_agents())
    print(TestConfig().locations().available_workflows())
