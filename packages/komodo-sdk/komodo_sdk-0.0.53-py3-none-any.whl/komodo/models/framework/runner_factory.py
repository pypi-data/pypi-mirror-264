from komodo.framework.komodo_agent import KomodoAgent
from komodo.framework.komodo_app import KomodoApp
from komodo.framework.komodo_workflow import KomodoWorkflow
from komodo.models.framework.agent_runner import AgentRunner
from komodo.models.framework.appliance_runner import ApplianceRunner
from komodo.models.framework.workflow_runner import WorkflowRunner


class RunnerFactory:
    @staticmethod
    def create_runner(item):
        if isinstance(item, KomodoApp):
            return ApplianceRunner(item)

        if isinstance(item, KomodoAgent):
            return AgentRunner(item)

        if isinstance(item, KomodoWorkflow):
            return WorkflowRunner(item)

        raise ValueError(f"Unsupported item type: {type(item)}")
