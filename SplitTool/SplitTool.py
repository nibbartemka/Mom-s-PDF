from typing import (
        Protocol,
        TypeAlias,
        NamedTuple,
        Optional,
        Tuple
    )
from pathlib import Path


PageNumber: TypeAlias = Optional[int]


class PageInterval(NamedTuple):
    begin_interval: PageNumber = 1
    end_interval: PageNumber = None


class SplitTool(Protocol):
    EXTENSTION = '.txt'

    @classmethod
    def split_file(cls, file_path: Path,
                   *args: Tuple[PageInterval]):
        pass
