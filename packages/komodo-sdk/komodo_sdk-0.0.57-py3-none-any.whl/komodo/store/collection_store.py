import uuid

from komodo.proto.generated.collection_pb2 import Collection, Intelligence
from komodo.store.redis_database import RedisDatabase, get_redis_server


class CollectionStore:
    def __init__(self, database=RedisDatabase.COLLECTIONS):
        self.redis = get_redis_server(database)

    def create_collection(self, shortcode, path, name, description):
        shortcode = shortcode or str(uuid.uuid4())
        collection = Collection(shortcode=shortcode, name=name, description=description, path=str(path))
        self.store_collection(collection)
        return collection

    def get_or_create_collection(self, shortcode, path, name=None, description=None):
        collection = self.retrieve_collection(shortcode)
        if collection:
            return collection
        else:
            return self.create_collection(shortcode, path, name, description)

    def store_collection(self, collection: Collection):
        collection_data = collection.SerializeToString()
        key = f"collection:{collection.shortcode}"
        self.redis.set(key, collection_data)

    def retrieve_collection(self, shortcode):
        key = f"collection:{shortcode}"
        collection_data = self.redis.get(key)
        if collection_data:
            collection = Collection()
            collection.ParseFromString(collection_data)
            return collection
        else:
            print("Collection not found for shortcode: ", shortcode)
            return None

    @staticmethod
    def find_file_in_collection(collection, filepath):
        for file in collection.files or []:
            if file.path == str(filepath):
                return file
        return None

    @staticmethod
    def remove_file_in_collection(collection: Collection, filepath):
        for file in collection.files or []:
            if file.path == str(filepath):
                collection.files.remove(file)

    @staticmethod
    def upsert_file_in_collection(collection, file):
        existing = CollectionStore.find_file_in_collection(collection, file.path)
        if existing:
            collection.files.remove(existing)
        collection.files.append(file)

    def remove_collection(self, shortcode):
        key = f"collection:{shortcode}"
        if self.redis.exists(key):
            self.redis.delete(key)

        keys = self.redis.keys(f"user:*:collection:{shortcode}")
        for key in keys:
            self.redis.delete(key)
        keys = self.redis.keys(f"appliance:*:collection:{shortcode}")
        for key in keys:
            self.redis.delete(key)

    def remove_everything(self):
        keys = self.redis.keys("*")
        for key in keys:
            self.redis.delete(key)

    def retrieve_all_collections(self):
        keys = self.redis.keys("collection:*")
        collections = []
        for key in keys or []:
            collection_data = self.redis.get(key)
            collection = Collection()
            collection.ParseFromString(collection_data)
            collections.append(collection)
        return collections

    def add_user_collection(self, user_email, shortcode):
        key = f"user:{user_email}:collection:{shortcode}"
        self.redis.sadd(key, shortcode)

    def remove_user_collection(self, user_email, shortcode):
        key = f"user:{user_email}:collection:{shortcode}"
        self.redis.delete(key)

    def exists_user_collection(self, user_email, shortcode):
        key = f"user:{user_email}:collection:{shortcode}"
        return self.redis.exists(key)

    def retrieve_collections_by_user(self, user_email):
        keys = self.redis.keys(f"user:{user_email}:collection:*")
        collections = []
        for key in keys or []:
            shortcode = key.decode('utf-8').split(":")[-1]
            collection = self.retrieve_collection(shortcode)
            collections.append(collection)
        return collections

    def add_appliance_collection(self, appliance_shortcode, shortcode):
        key = f"appliance:{appliance_shortcode}:collection:{shortcode}"
        self.redis.sadd(key, shortcode)

    def remove_appliance_collection(self, appliance_shortcode, shortcode):
        key = f"appliance:{appliance_shortcode}:collection:{shortcode}"
        self.redis.delete(key)

    def exists_appliance_collection(self, appliance_shortcode, shortcode):
        key = f"appliance:{appliance_shortcode}:collection:{shortcode}"
        return self.redis.exists(key)

    def retrieve_collections_by_appliance(self, appliance_shortcode):
        keys = self.redis.keys(f"appliance:{appliance_shortcode}:collection:*")
        collections = []
        for key in keys or []:
            shortcode = key.decode('utf-8').split(":")[-1]
            collection = self.retrieve_collection(shortcode)
            collections.append(collection)
        return collections

    def add_intelligence(self, shortcode, source, intelligence: Intelligence):
        intelligence_data = intelligence.SerializeToString()
        key = f"collection:{shortcode}:intelligence:{source}"
        self.redis.set(key, intelligence_data)

    def retrieve_intelligence(self, shortcode, source):
        key = f"collection:{shortcode}:intelligence:{source}"
        intelligence_data = self.redis.get(key)
        if intelligence_data:
            intelligence = Intelligence()
            intelligence.ParseFromString(intelligence_data)
            return intelligence
        else:
            return None

    def remove_intelligence(self, shortcode, source):
        key = f"collection:{shortcode}:intelligence:{source}"
        self.redis.delete(key)


if __name__ == "__main__":
    store = CollectionStore(database=RedisDatabase.TEST)
    collection = Collection(name="Test Collection", description="Test Description")
    collection.shortcode = "123"
    collection.path = "test"
    store.store_collection(collection)
    print(store.retrieve_collection("123"))

    user_email = "a@b.com"
    store.add_user_collection(user_email, "123")
    print(store.retrieve_collections_by_user(user_email))

    shortcode = "test"
    store.add_appliance_collection("123", shortcode)
    print(store.retrieve_collections_by_appliance(shortcode))

    collections = store.retrieve_all_collections()
    for collection in collections:
        print(collection)
        print(collection.shortcode)
        store.remove_collection(collection.shortcode)
    print(store.retrieve_all_collections())
    print(store.retrieve_collections_by_user(user_email))
    print(store.retrieve_collections_by_appliance(shortcode))

    intelligence = Intelligence()
    intelligence.source = "test"
    intelligence.summary = "test"
    intelligence.faq.add(question="test", answer="test")
    intelligence.faq.add(question="test2", answer="test2")

    store.add_intelligence(collection.shortcode, "test", intelligence)
    print(store.retrieve_intelligence(collection.shortcode, "test"))

    store.remove_intelligence(collection.shortcode, "test")
    print(store.retrieve_intelligence(collection.shortcode, "test"))
    store.redis.flushdb()
