from komodo import KomodoApp
from komodo.core.agents.default import translator_agent, summarizer_agent

from komodo.core.agents.librarian_agent import LibrarianAgent
from komodo.core.tools.web.serpapi_search import SerpapiSearch
from komodo.core.utils.rag_context import RagContext
from komodo.framework.komodo_context import KomodoContext
from komodo.framework.komodo_user import KomodoUser
from komodo.loaders.database.appliance_loader import ApplianceLoader
from komodo.models.framework.agent_runner import AgentRunner
from komodo.models.framework.appliance_runner import ApplianceRunner
from komodo.models.framework.appliance_runtime import ApplianceRuntime
from sample.config import ApplianceConfig
from sample.workflow import SampleWorkflow


class SampleAppliance(KomodoApp):
    def __init__(self, config=ApplianceConfig()):
        super().__init__(shortcode='sample', name='Sample', purpose='To test the Komodo Appliances SDK', config=config)
        self.users.append(KomodoUser(name="Test User", email="test@example.com"))

        locations = config.locations()
        locations.setup_appliance(self.shortcode)
        appliance_data = locations.appliance_data(self.shortcode)
        cache_path = locations.cache_path()
        print(f"Appliance data: {appliance_data}, cache path: {cache_path}")

        rc = RagContext(path=appliance_data, cache_path=cache_path, shortcode='default')
        self.add_agent(LibrarianAgent(rc))

        self.add_agent(summarizer_agent())
        self.add_agent(translator_agent())

        self.add_tool(SerpapiSearch(config.get_serpapi_key()))
        self.add_workflow(SampleWorkflow())

    def generate_context(self, prompt=None):
        context = KomodoContext()
        context.add("Sample", f"Develop context for the {self.name} appliance")
        return context


def build_and_run():
    appliance = SampleAppliance()
    prompt = '''
        Summarize the following text in 5 words and then translate into Spanish, Hindi and German:
        This is a sample application using the new Komodo SDK.
    '''
    runner = ApplianceRunner(appliance)
    response = runner.run(prompt)
    print(response.text)


def build_and_search():
    appliance = SampleAppliance()
    appliance.index()
    prompt = '''
        what is revenue breakdown of nvidia?
    '''
    runner = ApplianceRunner(appliance)
    response = runner.run(prompt)
    print(response.text)


def load_and_run():
    appliance = ApplianceLoader.load('sample')
    prompt = '''
        Summarize the following text in 5 words and translate into Spanish, Hindi and German:
        This is a sample application using the new Komodo 9 SDK.
    '''
    runner = ApplianceRunner(appliance)
    response = runner.run(prompt)
    print(response.text)


def build_and_search_with_agent():
    appliance = SampleAppliance()
    appliance.index()
    prompt = '''
        Any policy changes for nvidia?
    '''
    runtime = ApplianceRuntime(appliance)
    for a in runtime.get_all_agents():
        if 'docsearch' in a.shortcode:
            runner = AgentRunner(a)
            response = runner.run(prompt)
            print(response.text)

    agent = runtime.get_agent('librarian')
    runner = AgentRunner(agent)
    response = runner.run(prompt)
    print(response.text)


if __name__ == '__main__':
    appliance = SampleAppliance()
    email = "test@example.com"
    profile = next((x for x in appliance.users if x.email == email), None)
    print(profile.to_dict())
