from komodo.core.agents.summarizer_agent import SummarizerAgent
from komodo.core.tools.files.directory_reader import DirectoryReader
from komodo.framework.komodo_agent import KomodoAgent
from komodo.models.framework.agent_runner import AgentRunner
from komodo.testdata.config import TestConfig


def sample_agent_runner():
    from komodo.core.tools.web.serpapi_search import SerpapiSearch

    agent = SummarizerAgent.create(100)
    print(agent.instructions)

    agent = SummarizerAgent(n=200)
    print(agent.instructions)

    runner = AgentRunner(agent)
    result = runner.run("Summarize the iliad in 5 words")
    print(result.text)

    agent = KomodoAgent.default()
    dir = TestConfig().data_dir()
    agent.tools = [DirectoryReader(dir)]
    runner = AgentRunner(agent)

    prompt = "list files available to you"
    response = runner.run(prompt)
    print(response.text)

    for response in runner.run_streamed(prompt):
        print(response, end="")
    print()

    prompt = "whats up in nyc today? search for event and then search for additional details on the first event found"
    serpapi_key = TestConfig().get_serpapi_key()
    agent.tools = [SerpapiSearch(serpapi_key)]
    for response in runner.run_streamed(prompt):
        print(response, end="")
    print()

    response = runner.run(prompt)
    print(response.text)
