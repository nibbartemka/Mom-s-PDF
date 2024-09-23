from typing import Tuple, Protocol
from pathlib import Path


class MergeTool(Protocol):
    MERGED_FILE_NAME: str = 'merged_file'
    EXTENSTION: str = '.txt'

    @classmethod
    def merge_files(cls, output_path: Path,
                    *args: Tuple[Path]):
        pass
