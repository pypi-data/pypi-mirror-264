from komodo.core.agents.elastic_agent import ElasticAgent
from komodo.models.framework.agent_runner import AgentRunner
from komodo.testdata.config import TestConfig


def elastic_url():
    return TestConfig().get_elastic_url()


def authorized_indexes():
    return TestConfig().get_authorized_indexes()


def test_elastic_agent():
    agent = ElasticAgent(elastic_url(), authorized_indexes())
    runner = AgentRunner(agent)
    prompt = "Match all the records in the index."
    response = runner.run(prompt)
    print(response.text)


def test_elastic_agent_list_indexes():
    agent = ElasticAgent(elastic_url(), authorized_indexes())
    runner = AgentRunner(agent)
    prompt = "List all the indexes."
    response = runner.run(prompt)
    print(response.text)


def test_elastic_agent_count_records():
    agent = ElasticAgent(elastic_url(), authorized_indexes())
    runner = AgentRunner(agent)
    prompt = "Count records."
    response = runner.run(prompt)
    print(response.text)
