from typing import (
        Protocol,
        TypeAlias,
        NamedTuple,
        List
    )
from pathlib import Path
import re


PageNumber: TypeAlias = int


class PageInterval(NamedTuple):
    begin_interval: PageNumber
    end_interval: PageNumber


class PageIntervalConverter(object):
    INTERVAL_SEPARATOR: str = '-'
    INTERVAL_PATTERN: re.Pattern = re.compile(f'^\\d+[{INTERVAL_SEPARATOR}]\\d+$')

    @classmethod
    def convert_line_to_page_interval(cls, line: str) -> PageInterval:
        if not cls.INTERVAL_PATTERN.fullmatch(line):
            raise ValueError('Некорректные значения для интервала!\n')

        page_interval: List[str] = line.split(cls.INTERVAL_SEPARATOR)
        begin_interval, end_interval = page_interval

        return PageInterval(int(begin_interval),
                            int(end_interval))


class SplitTool(Protocol):
    EXTENSTION: str = '.txt'

    @classmethod
    def split_file(cls, file: Path, output_path: Path,
                   *args: List[PageInterval]):
        pass
