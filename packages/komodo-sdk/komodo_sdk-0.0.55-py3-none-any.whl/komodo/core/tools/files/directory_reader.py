import json
import os
from pathlib import Path

import inflection

from komodo.framework.komodo_tool import KomodoTool
from komodo.shared.utils.filestats import file_details


class DirectoryReader(KomodoTool):
    name = "Directory Reader"
    purpose = "Lists directory contents recursively"
    shortcode = "komodo_directory_reader"

    definition = {
        "type": "function",
        "function": {
            "name": shortcode,
            "description": purpose,
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Pattern of files to match. Defaults to all files if not provided."
                    },
                }
            }
        }
    }

    def __init__(self, path):
        super().__init__(shortcode=self.shortcode + "_" + inflection.underscore(str(path)),
                         definition=self.definition,
                         action=self.action)
        self.path = path

    def action(self, args):
        try:
            pattern = args.get("pattern", "*")
            files = self.get_files_recursively_pathlib(self.path, pattern)
            result = []

            for file in files:
                if os.path.isfile(file):
                    details = file_details(str(file))
                    file_info = {
                        "path": str(file.relative_to(self.path)),
                        "basename": details.name,
                        "type": details.magic,
                        "checksum": details.checksum,
                        "created_at": details.created_at,
                        "updated_at": details.modified_at
                    }
                    result.append(file_info)

            # print(result)
            return json.dumps(result, default=str)

        except Exception as e:
            print("Failed to list files: ", e)
            return "Failed to list files: " + str(args.get("pattern", ""))

    def get_files_recursively_pathlib(self, datadir, pattern='*'):
        return Path(datadir).rglob(pattern)


if __name__ == "__main__":
    from komodo.testdata.config import TestConfig
    from komodo.framework.komodo_tool_registry import KomodoToolRegistry

    d = TestConfig.path("dir1")
    t = DirectoryReader(d)
    print(t.definition)
    print(t.action({"pattern": "*.txt"}))

    KomodoToolRegistry.add_tool(t.shortcode, t.definition, t.action)
    print(KomodoToolRegistry.get_definitions([t.shortcode]))
    y = KomodoToolRegistry.get_tool_by_shortcode(t.shortcode)
    print(y.definition)
    print(y.action({"pattern": "*.txt"}))
