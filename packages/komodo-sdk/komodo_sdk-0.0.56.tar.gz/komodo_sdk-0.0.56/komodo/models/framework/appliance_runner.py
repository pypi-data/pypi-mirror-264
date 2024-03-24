from komodo.core.agents.groot_agent import GrootAgent
from komodo.framework.komodo_app import KomodoApp
from komodo.models.framework.agent_runner import AgentRunner
from komodo.models.framework.appliance_runtime import ApplianceRuntime
from komodo.models.framework.runner import Runner


class ApplianceRunner(Runner):
    def __init__(self, appliance):
        agent = ApplianceRuntime(appliance).coordinator_agent()
        self.runner = AgentRunner(agent)

    def run(self, prompt, **kwargs):
        return self.runner.run(prompt, **kwargs)

    def run_streamed(self, prompt, **kwargs):
        for response in self.runner.run_streamed(prompt, **kwargs):
            yield response


if __name__ == '__main__':
    appliance = KomodoApp.default()
    appliance.add_agent(GrootAgent())
    runner = ApplianceRunner(appliance)
    result = runner.run("Tell me a joke using groot_agent.")
    print(result.text)
