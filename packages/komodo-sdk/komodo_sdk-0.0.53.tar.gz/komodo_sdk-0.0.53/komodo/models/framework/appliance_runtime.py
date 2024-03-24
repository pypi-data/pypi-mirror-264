from komodo.core.agents.coordinator_agent import CoordinatorAgent
from komodo.core.agents.groot_agent import GrootAgent
from komodo.framework.komodo_app import KomodoApp
from komodo.loaders.database.user_loader import UserLoader
from komodo.models.framework.agent_runner import AgentRunner
from komodo.models.framework.workflow_runner import WorkflowRunner


class ApplianceRuntime:

    def __init__(self, appliance):
        self.appliance = appliance

    @staticmethod
    def run_agent_as_tool(agent, args) -> str:
        runner = AgentRunner(agent)
        history = [{'role': "system", 'content': args['system']}]
        response = runner.run(prompt=args['user'], history=history)
        return response.text

    @staticmethod
    def run_workflow_as_tool(workflow, args) -> str:
        runner = WorkflowRunner(workflow)
        response = runner.run(prompt=args['command'], history=None)
        return response.text

    def coordinator_agent(self):
        return CoordinatorAgent(self.appliance,
                                ApplianceRuntime.run_agent_as_tool,
                                ApplianceRuntime.run_workflow_as_tool)

    def get_user(self, email):
        return UserLoader.load(email) or next((x for x in self.appliance.users if x.email == email), None)

    def get_all_agents(self):
        return self.appliance.get_all_agents()

    def get_agent(self, shortcode):
        for a in self.get_all_agents():
            if a.shortcode == shortcode:
                return a
        return None

    def get_capabilities_of_agents(self):
        t = [
            "{}. {} ({}): {}".format(i, a.name, a.shortcode, a.purpose)
            for i, a in enumerate(self.get_all_agents(), start=1)
            if a.purpose is not None
        ]
        return '\n'.join(t)

    def get_capabilities_of_tools(self):
        t = ["{}. {}: {}".format(i + 1, tool.shortcode, tool.purpose)
             for i, tool in enumerate(filter(lambda x: x.purpose is not None, self.appliance.tools))]
        return '\n'.join(t)

    def list_capabilities(self):
        return "I am " + self.appliance.name + \
            " appliance and my purpose is " + self.appliance.purpose + "." + \
            "\n\nI have agents with these capabilities: \n" + self.get_capabilities_of_agents() + \
            "\n\nI have tools with these capabilities: \n" + self.get_capabilities_of_tools()


if __name__ == '__main__':
    appliance = KomodoApp.default()
    appliance.add_agent(GrootAgent())
    runtime = ApplianceRuntime(appliance)
    print(runtime.list_capabilities())
