from komodo.core.agents.groot_agent import GrootAgent
from komodo.framework.komodo_app import KomodoApp
from komodo.models.framework.appliance_runner import ApplianceRunner

if __name__ == '__main__':
    appliance = KomodoApp.default()
    appliance.add_agent(GrootAgent())
    runner = ApplianceRunner(appliance)
    result = runner.run("Tell me a joke using groot_agent.")
    print(result.text)
