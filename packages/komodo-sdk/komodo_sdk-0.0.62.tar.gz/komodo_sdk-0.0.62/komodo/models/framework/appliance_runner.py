from komodo.models.framework.agent_runner import AgentRunner
from komodo.models.framework.appliance_runtime import ApplianceRuntime
from komodo.models.framework.runner import Runner


class ApplianceRunner(Runner):
    def __init__(self, appliance, user=None):
        agent = ApplianceRuntime(appliance).coordinator_agent()
        self.runner = AgentRunner(agent, user=user)

    def run(self, prompt, **kwargs):
        return self.runner.run(prompt, **kwargs)

    def run_streamed(self, prompt, **kwargs):
        for response in self.runner.run_streamed(prompt, **kwargs):
            yield response
