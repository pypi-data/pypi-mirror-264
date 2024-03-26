import os
from pathlib import Path


class KomodoLocations:

    def __init__(self, data_directory, **kwargs):
        self.data_directory = data_directory
        self.kwargs = kwargs

    def shared(self) -> Path:
        return self.data_directory / "shared"

    def cache(self) -> Path:
        return self.data_directory / "cache"

    def cache_path(self) -> Path:
        return self.data_directory / "cache"

    def appliances(self) -> Path:
        return self.data_directory / "appliances"

    def appliance(self, shortcode) -> Path:
        return self.appliances() / shortcode

    def available_appliances(self) -> list[str]:
        folder = self.appliances()
        return [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

    def appliance_data(self, shortcode) -> Path:
        return self.appliance(shortcode) / "data"

    def appliance_files(self, shortcode) -> [Path]:
        folder = self.appliance_data(shortcode)
        return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    def appliance_instructions(self, shortcode) -> Path:
        return self.appliance(shortcode) / "instructions.txt"

    def appliance_context(self, shortcode) -> Path:
        return self.appliance(shortcode) / "context.yml"

    def appliance_dictionary(self, shortcode) -> Path:
        return self.appliance(shortcode) / "dictionary.yml"

    def agents(self) -> Path:
        return self.data_directory / "agents"

    def agent(self, shortcode) -> Path:
        return self.agents() / shortcode

    def available_agents(self) -> list[str]:
        folder = self.agents()
        return [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

    def agent_instructions(self, shortcode) -> Path:
        return self.agent(shortcode) / "instructions.txt"

    def agent_context(self, shortcode) -> Path:
        return self.agent(shortcode) / "context.yml"

    def agent_dictionary(self, shortcode) -> Path:
        return self.agent(shortcode) / "dictionary.yml"

    def agent_data(self, shortcode) -> Path:
        return self.agent(shortcode) / "data"

    def agent_files(self, shortcode) -> [Path]:
        folder = self.agent_data(shortcode)
        return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    def workflows(self) -> Path:
        return self.data_directory / "workflows"

    def workflow(self, shortcode) -> Path:
        return self.workflows() / shortcode

    def available_workflows(self) -> list[str]:
        folder = self.workflows()
        return [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

    def workflow_data(self, shortcode) -> Path:
        return self.workflow(shortcode) / "data"

    def workflow_files(self, shortcode) -> [Path]:
        folder = self.workflow_data(shortcode)
        return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    def workflow_instructions(self, shortcode) -> Path:
        return self.workflow(shortcode) / "instructions.txt"

    def workflow_context(self, shortcode) -> Path:
        return self.workflow(shortcode) / "context.yml"

    def workflow_dictionary(self, shortcode) -> Path:
        return self.workflow(shortcode) / "dictionary.yml"

    def users(self) -> Path:
        return self.data_directory / "users"

    def user(self, email) -> Path:
        return self.users() / email

    def user_uploads(self, email) -> Path:
        return self.user(email) / "uploads"

    def user_collections(self, email) -> Path:
        return self.user(email) / "collections"

    def setup_appliance(self, shortcode, skeleton=False):
        for d in [self.appliances(), self.agents(), self.users(), self.workflows()]:
            os.makedirs(d, exist_ok=True)

        os.makedirs(self.appliance(shortcode), exist_ok=True)
        os.makedirs(self.appliance_data(shortcode), exist_ok=True)
        if skeleton:
            self.setup_appliance_skeleton(shortcode)

    def setup_appliance_skeleton(self, shortcode):
        for file in [self.appliance_instructions(shortcode), self.appliance_context(shortcode),
                     self.appliance_dictionary(shortcode)]:
            if not file.exists():
                file.touch()

    def setup_agent(self, shortcode, skeleton=False):
        os.makedirs(self.agent(shortcode), exist_ok=True)
        os.makedirs(self.agent_data(shortcode), exist_ok=True)
        if skeleton:
            for file in [self.agent_instructions(shortcode), self.agent_context(shortcode),
                         self.agent_dictionary(shortcode)]:
                if not file.exists():
                    file.touch()

    def setup_workflow(self, shortcode, skeleton=False):
        os.makedirs(self.workflow(shortcode), exist_ok=True)
        os.makedirs(self.workflow_data(shortcode), exist_ok=True)
        if skeleton:
            for file in [self.workflow_instructions(shortcode), self.workflow_context(shortcode),
                         self.workflow_dictionary(shortcode)]:
                if not file.exists():
                    file.touch()

    def setup_user(self, email):
        os.makedirs(self.user(email), exist_ok=True)
        for d in [self.user_uploads(email), self.user_collections(email)]:
            os.makedirs(d, exist_ok=True)


if __name__ == "__main__":
    from komodo.testdata.config import TestConfig

    email = "ryan@kmdo.app"
    locations = KomodoLocations(TestConfig().data_dir())
    locations.setup("sample", ["planner", "checker"], ["analyzer"], ["ryan@kmdo.app", "test@example.com"])

    test_appliance = "sample"
    print(locations.appliances())
    print(locations.appliance(test_appliance))
    print(locations.appliance_data(test_appliance))
    print(locations.appliance_files(test_appliance))
    print(locations.appliance_instructions(test_appliance))
    print(locations.appliance_context(test_appliance))
    print(locations.appliance_dictionary(test_appliance))

    test_agent = "planner"
    print(locations.agents())
    print(locations.agent(test_agent))
    print(locations.agent_instructions(test_agent))
    print(locations.agent_context(test_agent))
    print(locations.agent_dictionary(test_agent))
    print(locations.agent_data(test_agent))
    print(locations.agent_files(test_agent))

    test_workflow = "analyzer"
    print(locations.workflows())
    print(locations.workflow(test_workflow))
    print(locations.workflow_data(test_workflow))
    print(locations.workflow_files(test_workflow))
    print(locations.workflow_instructions(test_workflow))
    print(locations.workflow_context(test_workflow))
    print(locations.workflow_dictionary(test_workflow))

    print(locations.users())
    print(locations.user(email))
    print(locations.user_uploads(email))
    print(locations.user_collections(email))

    print(locations.available_appliances())
    print(locations.available_agents())
    print(locations.available_workflows())
