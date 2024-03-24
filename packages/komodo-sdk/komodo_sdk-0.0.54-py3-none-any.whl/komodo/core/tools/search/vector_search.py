from komodo.core.vector_stores.qdrant_store import QdrantStore
from komodo.framework.komodo_tool import KomodoTool
from komodo.framework.komodo_vectorstore import KomodoVectorStore


class VectorSearch(KomodoTool):
    name = "Vector Search"
    shortcode = "vector_search_tool"
    purpose = "Search available data sources"

    definition = {
        "type": "function",
        "function": {
            "name": shortcode,
            "description": purpose,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search across all available data using vector search"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of results to return, default is 3",
                    }
                },
                "required": ["query"]
            }
        }
    }

    def __init__(self, store: KomodoVectorStore):
        super().__init__(shortcode=self.shortcode,
                         definition=self.definition,
                         action=self.action)
        self.store = store

    def action(self, args):
        text = args['query']
        top_k = int(args.get('top_k', 3))
        result = self.store.search(text, top_k=top_k)
        if len(result) > 0:
            return result
        return f"No results found for: {text}, total records: {self.store.get_count()}"


if __name__ == "__main__":
    store = QdrantStore.create(shortcode="test")
    store.get_collection()
    store.upsert_single(3, "test out this world", source="tool test")
    store.wait_for_upsert(3)

    tool = VectorSearch(store)
    print(tool.definition)
    print(tool.action({"query": "test", "top_k": "5"}))
