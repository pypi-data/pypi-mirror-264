import os

from komodo.framework.komodo_tool import KomodoTool
from komodo.shared.documents.text_extract_helper import TextExtractHelper
from komodo.shared.utils.digest import convert_to_base64


class FileReader(KomodoTool):
    shortcode = "komodo_file_reader"
    name = "File Reader"
    purpose = "Reads data files and returns the extracted text contents."

    definition = {
        "type": "function",
        "function": {
            "name": shortcode,
            "description": purpose,
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Name of the file to read"},
                    "start": {"type": "integer", "description": "Start position in file"},
                    "bytes": {"type": "integer", "description": "Number of bytes to read. Defaults t 2048."},
                    "raw": {"type": "boolean",
                            "description": "Return raw bytes instead of text, as base64 encoded string. Defaults to false."}
                },
                "required": ["filename"]
            }
        }
    }

    def __init__(self, path, cache_path=None):
        super().__init__(shortcode=self.shortcode,
                         definition=self.definition,
                         action=self.action)
        self.path = path
        self.cache_path = cache_path

    def action(self, args):
        try:
            path = os.path.join(self.path, args["filename"])
            start = args.get("start", 0)
            bytes = args.get("bytes", 2048)
            raw = args.get("raw", False)
            if not raw:
                helper = TextExtractHelper(path, cache_path=self.cache_path)
                contents = helper.extract_text()
                return contents[start:start + bytes]
            else:
                with open(path, "rb") as f:
                    f.seek(start)
                    contents = f.read(bytes)
                    return convert_to_base64(contents)

        except Exception:
            return f"Failed to read file: {args['filename']} from {self.path}"


if __name__ == "__main__":
    from komodo.testdata.config import TestConfig

    path = TestConfig().locations().appliance_data('komodo') / "dir1"
    cache_path = TestConfig().locations().cache_path()
    tool = FileReader(path, cache_path)
    print(tool.definition)
    print(tool.action({"filename": "hello.txt"}))

    path = TestConfig().locations().appliance_data('komodo') / "dir2"
    tool = FileReader(path, cache_path)
    print(tool.definition)
    print(tool.action({"filename": "InflationChapter1.pdf"}))
