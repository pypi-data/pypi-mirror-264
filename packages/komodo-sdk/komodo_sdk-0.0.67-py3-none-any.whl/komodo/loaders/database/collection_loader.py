from komodo.framework.komodo_collection import KomodoCollection
from komodo.store.collection_store import CollectionStore


class CollectionLoader:

    @classmethod
    def load(cls, guid) -> KomodoCollection:
        collection = CollectionStore().retrieve_collection(guid)
        print(collection)
        return KomodoCollection(guid=collection.guid, name=collection.name, description=collection.description,
                                files=collection.files)
