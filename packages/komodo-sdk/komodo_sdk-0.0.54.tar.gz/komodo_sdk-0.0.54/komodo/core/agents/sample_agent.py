from komodo.core.tools.utils.sample_tool import SampleTool
from komodo.framework.komodo_agent import KomodoAgent
from komodo.models.framework.agent_runner import AgentRunner
from komodo.testdata.config import TestConfig


class SampleAgent(KomodoAgent):
    shortcode = "sample_agent"
    name = "Sample Agent"
    purpose = "Sample agent to invoke sample tool."
    instructions = "Call the sample tool"

    def __init__(self, path):
        super().__init__(shortcode=self.shortcode, name=self.name, purpose=self.purpose,
                         instructions=self.instructions,
                         tools=[SampleTool(path)])


if __name__ == "__main__":
    path = TestConfig().data_dir() / "dir1"
    agent = SampleAgent(path)
    runner = AgentRunner(agent)
    response = runner.run("Call the sample tool with hello.txt file and call hello_world function.")
    print(response.text)
