import json

from komodo.shared.utils.digest import convert_to_base64


class KomodoTool:
    def __init__(self, shortcode, definition, action):
        self.shortcode = shortcode
        self.definition = definition
        self.action = action
        self.name = definition['function']['name']

    def __str__(self):
        return f"KomodoTool: {self.shortcode} {self.name} ({self.definition['function']['description']})"

    def to_dict(self):
        return {
            'shortcode': self.shortcode,
            'name': self.name,
            'definition': self.definition
        }

    def run(self, args: dict):
        return self.action(args)

    @staticmethod
    def to_base64(contents):
        result = {"Base64 Encoded": convert_to_base64(contents)}
        return json.dumps(result)

    @classmethod
    def default(cls):
        return KomodoTool(shortcode="test", definition={"function": {"name": "test", "description": "test"}},
                          action=lambda x: x)


if __name__ == "__main__":
    print(KomodoTool(shortcode="test", definition={"function": {"name": "test", "description": "test"}},
                     action=lambda x: x).to_dict())

    print(KomodoTool.to_base64("test"))
    print(KomodoTool.to_base64(b"test"))
    print(KomodoTool.to_base64({"test": "test"}))
    print(KomodoTool.to_base64([1, 2, 3]))
    print(KomodoTool.to_base64(1))
    print(KomodoTool.to_base64(1.0))
