from komodo.proto.generated.collection_pb2 import File


class KomodoCollection:
    def __init__(self, *, guid, name, description, files=None):
        self.guid = guid
        self.name = name
        self.description = description
        self.files: [File] = files or []

    def __str__(self):
        return f"KomodoCollection(name={self.name}, guid={self.guid}, description={self.description})"

    def __eq__(self, other):
        if not isinstance(other, KomodoCollection):
            return False
        return self.guid == other.guid

    def __hash__(self):
        return self.guid
