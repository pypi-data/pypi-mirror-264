import uuid

from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import Parse as JsonToMessage

from komodo.proto.generated.collection_pb2 import Collection, File, Intelligence, QnA
from komodo.proto.generated.model_pb2 import User, Appliance

user = User(email="john.doe@acme.com", name="John Doe")
print(user)

## Test Json conversion
user_json = MessageToJson(user, indent=0).replace("\n", "")
print(user_json)
message = JsonToMessage(user_json, User())
print(message)
assert message == user  # True

## Test Serialization
ser = user.SerializeToString()
print(ser)
deser = User.FromString(ser)
print(deser)

appliance = Appliance(name="ACME 123", purpose="Building Automation")
print(appliance)

collection = Collection(shortcode=str(uuid.uuid4()), name="My Collection", description="My Collection Description")
print(collection)

file = File(path="/data/komodo/foo.txt", name="My File", description="My File Description")
print(file)

intelligence = Intelligence(source="/data/komodo/foo.txt", summary="My Summary")
intelligence.faq.append(QnA(question="What is the meaning of life?", answer="42"))
intelligence.faq.append(QnA(question="How do I get to the moon?", answer="You can't, it's made of cheese."))
print(intelligence)
