from typing import Tuple
from io import BufferedReader, BufferedWriter
import os
from pathlib import Path

import PyPDF2

from MergeTool import MergeTool


class PDFMergeTool(MergeTool):
    EXTENSTION: str = '.pdf'

    @classmethod
    def merge_files(cls, output_path: Path,
                    *args: Tuple[Path]):

        with cls.get_output_file(output_path) as output_file:
            pdf_writer: PyPDF2.PdfWriter = PyPDF2.PdfWriter()

            for path in args:
                with cls.get_input_file(path) as input_file:
                    pdf_reader: PyPDF2.PdfReader = PyPDF2.PdfReader(input_file)
                    cls.__add_pages_from_file(pdf_reader.pages, pdf_writer)

            pdf_writer.write(output_file)

    @classmethod
    def get_output_file(cls, file_path: Path) -> BufferedWriter:
        unique_file_name: str = cls.__get_unique_file_name(
                file_path,
                cls.MERGED_FILE_NAME,
                cls.EXTENSTION
            )
        output_file_path: Path = file_path / unique_file_name
        return open(output_file_path, 'wb')

    @staticmethod
    def get_input_file(file_path: Path) -> BufferedReader:
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
