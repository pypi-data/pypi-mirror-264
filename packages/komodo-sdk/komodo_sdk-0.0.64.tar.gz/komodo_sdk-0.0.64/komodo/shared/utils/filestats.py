import os
import uuid
from datetime import datetime
from pathlib import Path

import magic

from komodo.proto.generated.collection_pb2 import File
from komodo.shared.utils.digest import get_digest


def file_details(filepath):
    file = File(guid=str(uuid.uuid4()), path=filepath)
    stat = Path(filepath).stat()
    file.name = os.path.basename(filepath)
    file.size = stat.st_size
    file.magic = magic.from_file(filepath, mime=True)
    file.checksum = get_digest(filepath)
    file.created_at = datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    file.modified_at = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    return file
