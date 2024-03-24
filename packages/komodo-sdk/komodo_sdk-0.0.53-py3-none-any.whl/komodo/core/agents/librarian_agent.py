import json

from komodo.core.tools.files.directory_reader import DirectoryReader
from komodo.core.tools.files.file_reader import FileReader
from komodo.core.tools.search.vector_search import VectorSearch
from komodo.core.utils.indexer import Indexer
from komodo.core.utils.rag_context import RagContext
from komodo.framework.komodo_agent import KomodoAgent
from komodo.framework.komodo_context import KomodoContext
from komodo.models.framework.agent_runner import AgentRunner


class LibrarianAgent(KomodoAgent):
    shortcode = "librarian"
    name = "Librarian Agent"
    purpose = "Answer questions based on documents provided."
    instructions = "You are a Document QnA Agent. " \
                   "You will be given vector search tool and a question. " \
                   "You must answer the question based on the provided data. " \
                   "Do not use any external sources."

    def __init__(self, rc: RagContext):
        super().__init__(
            shortcode=self.shortcode + "_" + rc.shortcode,
            name=self.name + f" ({rc.shortcode})",
            purpose=self.purpose,
            instructions=self.instructions)

        self.rag_context = rc
        self.files = DirectoryReader(rc.path).action({})
        self.add_tool(FileReader(rc.path, rc.cache_path))
        self.add_tool(VectorSearch(rc.get_vector_store()))

    def generate_context(self, prompt=None):
        context = KomodoContext()
        context.extend(super().generate_context(prompt))
        context.add("List of Files for Reference", json.dumps(self.files))
        return context

    def index(self, reindex=False):
        indexer = Indexer(self.rag_context)
        indexer.run(reindex=reindex)
        if reindex:
            self.files = DirectoryReader(self.rag_context.path).action({})


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
