from typing import Tuple, Protocol
from pathlib import Path


class MergeTool(Protocol):
    MERGED_FILE_NAME: str = 'merged_file'
    EXTENSTION: str = '.txt'

    @classmethod
    def merge_files(cls, path_to_file: Path,
                    *args: Tuple[Path]):
        pass
