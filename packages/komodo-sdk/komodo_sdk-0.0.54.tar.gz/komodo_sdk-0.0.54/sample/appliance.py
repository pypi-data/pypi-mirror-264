from komodo import KomodoApp
from komodo.core.agents.default import translator_agent, summarizer_agent

from komodo.core.agents.librarian_agent import LibrarianAgent
from komodo.core.tools.web.serpapi_search import SerpapiSearch
from komodo.framework.komodo_context import KomodoContext
from komodo.framework.komodo_user import KomodoUser
from komodo.models.framework.appliance_runtime import ApplianceRuntime
from sample.config import ApplianceConfig
from sample.workflow import SampleWorkflow


class SampleAppliance(KomodoApp):
    def __init__(self, config=ApplianceConfig()):
        super().__init__(shortcode='sample', name='Sample', purpose='To test the Komodo Appliances SDK', config=config)
        self.users.append(KomodoUser(name="Test User", email="test@example.com"))

        runtime = ApplianceRuntime(self)
        self.add_agent(LibrarianAgent(runtime.get_appliance_rag_context()))

        self.add_agent(summarizer_agent())
        self.add_agent(translator_agent())

        self.add_tool(SerpapiSearch(config.get_serpapi_key()))
        self.add_workflow(SampleWorkflow())

    def generate_context(self, prompt=None):
        context = KomodoContext()
        context.add("Sample", f"Develop context for the {self.name} appliance")
        return context
