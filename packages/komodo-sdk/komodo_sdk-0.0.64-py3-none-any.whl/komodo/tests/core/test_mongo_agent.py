
from komodo.core.agents.mongo_agent import MongoAgent
from komodo.shared.utils.term_colors import print_success
from komodo.testdata.config import TestConfig


def test_mongo_agent_context():
    agent = MongoAgent(TestConfig().get_mongo_url())
    print_success(agent.generate_context())
