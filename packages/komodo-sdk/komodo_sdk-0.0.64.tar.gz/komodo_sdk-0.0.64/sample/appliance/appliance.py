from komodo import KomodoApp
from komodo.core.agents.default import translator_agent, summarizer_agent

from komodo.core.agents.librarian_agent import LibrarianAgent
from komodo.core.tools.web.serpapi_search import SerpapiSearch
from komodo.framework.komodo_context import KomodoContext
from komodo.framework.komodo_user import KomodoUser
from komodo.models.framework.appliance_runtime import ApplianceRuntime
from sample.appliance.workflow import SampleWorkflow


class SampleAppliance(KomodoApp):
    shortcode = 'sample'
    name = 'Sample Appliance'
    purpose = 'To test the Komodo Appliances SDK'

    def __init__(self, config):
        super().__init__(shortcode=self.shortcode, name=self.name, purpose=self.purpose, config=config)
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
