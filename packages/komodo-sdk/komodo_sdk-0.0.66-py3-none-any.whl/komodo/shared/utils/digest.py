import base64
import hashlib
import json


def get_guid(n=None):
    import uuid
    guid = str(uuid.uuid4())
    return guid[:n] if n else guid


def get_digest(filename):
    try:
        with open(filename, "rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return file_hash.hexdigest()
    except FileNotFoundError:
        return None


def get_text_digest(text):
    return hashlib.md5(text.encode()).hexdigest()


def convert_to_base64(contents) -> str:
    if type(contents) is bytes:
        return base64.b64encode(contents).decode('utf-8')

    if type(contents) is dict or type(contents) is list:
        v = json.dumps(contents, default=str)
        return base64.b64encode(v.encode('utf-8')).decode('utf-8')

    return base64.b64encode(str(contents).encode('utf-8')).decode('utf-8')


if __name__ == "__main__":
    print(get_digest(__file__))
    print(get_text_digest("hello"))
