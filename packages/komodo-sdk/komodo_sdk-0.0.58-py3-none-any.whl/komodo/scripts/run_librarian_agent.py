
from komodo.core.agents.librarian_agent import LibrarianAgent
from komodo.core.utils.rag_context import RagContext
from komodo.models.framework.agent_runner import AgentRunner


def run_search():
    from komodo.testdata.config import TestConfig
    path = TestConfig().locations().appliance_data('komodo')
    cache_path = TestConfig().locations().cache_path()
    agent = LibrarianAgent(RagContext(path=path, cache_path=cache_path))
    agent.index()
    runner = AgentRunner(agent)
    response = runner.run("What did the G20 leaders agreed in 2009?")
    print(response.text)

    response = runner.run("tell me more about unique swap identifiers (USI) of each clearing swap?")
    print(response.text)


if __name__ == "__main__":
    run_search()
