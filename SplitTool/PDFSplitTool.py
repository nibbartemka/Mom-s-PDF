from typing import Tuple, TypeAlias, Optional
from io import BufferedReader, BufferedWriter
from pathlib import Path
import os

import PyPDF2

from SplitTool import SplitTool, PageInterval

PageNumber: TypeAlias = Optional[int]


class PDFSplitTool(SplitTool):
    EXTENSTION = '.pdf'

    @classmethod
    def split_file(cls, file: Path, output_path: Path, *args: Tuple[PageInterval]):
        with cls.get_input_file(file) as input_file:
            pdf_reader: PyPDF2.PdfReader = PyPDF2.PdfReader(input_file)
            pages: list[PyPDF2.PageObject] = pdf_reader.pages

            for begin_interval, end_interval in args:
                if not cls.__check_page_number(begin_interval, len(pages)):
                    raise ValueError(
                        'Incorrect page number!'
                        'Please check entered value, 1 <= value <= page count'
                    )

                if not end_interval:
                    end_interval: PageNumber = begin_interval

                if not cls.__check_page_number(end_interval, len(pages)):
                    raise ValueError(
                        'Incorrect page number!'
                        'Please check entered value, 1 <= value <= page count'
                    )

                pdf_writer: PyPDF2.PdfWriter = PyPDF2.PdfWriter()

                cls.__add_pages_from_file(
                    [pages[page_number - 1]
                     for page_number in range(begin_interval,
                                              end_interval + 1)],
                    pdf_writer
                )

                final_name: str = (Path(file).stem
                                   + f'_{str(begin_interval)}-{str(end_interval)}')

                with cls.get_output_file(output_path,
                                         final_name) as output_file:
                    pdf_writer.write(output_file)

    @classmethod
    def get_output_file(cls, file_path: Path,
                        output_file_name: str) -> BufferedWriter:
        unique_file_name: str = cls.__get_unique_file_name(
                file_path,
                output_file_name,
                cls.EXTENSTION
            )
        output_file_path: Path = file_path / unique_file_name
        return open(output_file_path, 'wb')

    @staticmethod
    def get_input_file(file_path: str) -> BufferedReader:
        return open(file_path, 'rb')

    @staticmethod
    def __add_pages_from_file(pages: list[PyPDF2.PageObject],
                              pdf_writer: PyPDF2.PdfWriter) -> None:
        for page_index in range(len(pages)):
            pdf_writer.add_page(pages[page_index])

    @staticmethod
    def __get_unique_file_name(file_path: Path,
                               file_name: str,
                               extension: str) -> str:
        full_file_name: str = file_name + extension
        suggested_file_path: Path = file_path / full_file_name

        is_existed: bool = os.path.isfile(suggested_file_path)
        copy_count: int = 1

        while is_existed:
            full_file_name = file_name + f'({str(copy_count)})' + extension
            suggested_file_path: Path = file_path / full_file_name
            copy_count += 1
            is_existed: bool = os.path.isfile(suggested_file_path)

        return full_file_name

    @staticmethod
    def __check_page_number(page_number: PageNumber, max_value: PageNumber):
        return 1 <= page_number <= max_value
