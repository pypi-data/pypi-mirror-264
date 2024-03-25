from komodo.framework.komodo_agent import KomodoAgent
from komodo.framework.komodo_config import KomodoConfig
from komodo.framework.komodo_context import KomodoContext
from komodo.framework.komodo_features import KomodoFeatures, KomodoApplianceType, Komodo
from komodo.framework.komodo_tool import KomodoTool
from komodo.framework.komodo_tool_registry import KomodoToolRegistry
from komodo.framework.komodo_user import KomodoUser
from komodo.framework.komodo_workflow import KomodoWorkflow


class KomodoApp:

    def __init__(self, shortcode, name, purpose, **kwargs):
        self.shortcode = shortcode
        self.name = name
        self.purpose = purpose
        self.agents: [KomodoAgent] = []
        self.tools: [KomodoTool] = []
        self.workflows: [KomodoWorkflow] = []
        self.config = kwargs.get("config", KomodoConfig())
        self.context = kwargs.get("context", KomodoContext())
        self.company = kwargs.get("company", Komodo.company)
        self.type = kwargs.get("type", KomodoApplianceType.enterprise)
        self.features = kwargs.get("features", [e for e in KomodoFeatures])
        self.users: [KomodoUser] = kwargs.get("users", [])

    def add_agent(self, agent):
        self.agents += [agent]
        return self

    def add_tool(self, tool):
        self.tools.extend(KomodoToolRegistry.get_tools([tool]))
        return self

    def add_workflow(self, workflow):
        self.workflows += [workflow]
        return self

    def get_all_agents(self):
        return self.agents + self.workflows

    def generate_context(self, prompt=None):
        return self.context

    def index(self, reindex=False):
        for agent in self.agents:
            agent.index(reindex=reindex)

    @staticmethod
    def default(config=KomodoConfig()):
        return KomodoApp(name="Placeholder", shortcode="placeholder", purpose="Placeholder", config=config)
