from pathlib import Path
import os
from typing import Optional, List

from PyQt6.QtWidgets import (
    QLabel,
    QFileDialog,
    QTabWidget,
    QPushButton,
    QMessageBox
)
from PyQt6.QtGui import QPixmap, QIcon

from MergeTool import MergeTool
from .LayoutBuilder import GridLayoutBuilder
from config import DEFAULT_OUTPUT_PATH, STATIC_DIRECTORY_PATH


class MergeTab(QTabWidget):
    def __init__(self, merge_tool: MergeTool, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.merge_tool: MergeTool = merge_tool

        self.output_directory: Path = DEFAULT_OUTPUT_PATH
        self.input_files: List[Optional[Path]] = []

        self.output_directory_label: QLabel = QLabel(str(self.output_directory))
        self.output_directory_label.setStyleSheet(
            '''
                color: white;
                border-radius: 15%;
                font-family: Roboto;
                font-size: 12px;
                background-color: grey;
                padding: 10%;
            '''
        )

        self.output_directory_change_button: QPushButton = QPushButton('ИЗМЕНИТЬ ПУТЬ')
        self.output_directory_change_button.clicked.connect(self.change_directory_dialog)
        self.output_directory_change_button.setStyleSheet(
            '''
                QPushButton {
                    font-weight: bold;
                    color: white;
                    border: none;
                    font-family: Roboto;
                    font-size: 12px;
                    padding: 10%;
                }

                QPushButton:hover {
                    border-radius: 15%;
                    background-color: #5D94E5;
                }
            '''
        )
        self.output_directory_pixmap = QIcon(str(STATIC_DIRECTORY_PATH
                                                 / 'img'
                                                 / 'folder_icon.svg'))
        self.output_directory_change_button.setIcon(self.output_directory_pixmap)

        self.input_files_select_button: QPushButton = QPushButton('ОБЪЕДИНИТЬ')
        self.input_files_select_button.clicked.connect(self.merge_files)
        self.input_files_select_button.setStyleSheet(
            '''
                QPushButton {
                    background-color: #FF9900;
                    color: white;
                    font-weight: bold;
                    font-family: Roboto;
                    border-radius: 15%;
                    padding: 10%;
                }

                QPushButton:hover {
                    background-color: #FFB03A;
                }
            '''
        )

        self.head_text_label: QLabel = QLabel('ОБЪЕДИНИТЕ СВОИ PDF-ФАЙЛЫ')
        self.head_text_label.setStyleSheet(
            '''
                padding: 0px;
                font-size: 32px;
                font-family: Roboto;
                color: white;
                font-weight: bold;
            '''
        )

        self.beneath_text_label: QLabel = QLabel('ВСЕГО В ОДИН КЛИК')
        self.beneath_text_label.setStyleSheet(
            '''
                padding: 0px;
                font-size: 24px;
                font-family: Roboto;
                color: white;
                font-weight: bold;
            '''
        )

        self.mascot_image = QLabel()
        self.mascot_pixmap = QPixmap(str(STATIC_DIRECTORY_PATH
                                         / 'img'
                                         / 'Ali-e_merge.svg'))

        self.mascot_image.setPixmap(self.mascot_pixmap)
        self.mascot_image.resize(self.mascot_pixmap.width(),
                                 self.mascot_pixmap.height())
        self.mascot_image.setStyleSheet(
            '''
                margin: auto;
            '''
        )

        grid = (
            GridLayoutBuilder()
            .add_widget(self.head_text_label, 0, 0, 1, 3)  # row, col, row_span, col_span
            .add_widget(self.beneath_text_label, 1, 0, 1, 1)
            .add_widget(self.input_files_select_button, 2, 0, 1, 1)
            .add_widget(self.output_directory_label, 5, 0, 1, 1)
            .add_widget(self.output_directory_change_button, 5, 1, 1, 1)
            .add_widget(self.mascot_image, 0, 4, 5, 5)
            .build()
        )

        self.setLayout(grid)

    def merge_files(self) -> None:
        try:
            self.select_files_dialog()
            self.merge_tool.merge_files(self.output_directory,
                                        *self.input_files)
            question = QMessageBox.question(None,
                                            'Операция выполнена!\n',
                                            'Объединение файлов прошло успешно. Перейти к директории?',
                                            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Open)
            self.__handle_message_after_successful_split(question)
        except FileExistsError as error:
            QMessageBox.warning(None,
                                'Предупреждение',
                                str(error))

    def select_files_dialog(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(
                    self,
                    'Выберите PDF-файлы',
                    '',
                    'PDF files (*.pdf)'
                )
        if not files:
            raise FileExistsError("Файлы не выбраны!")
        self.input_files: List[Optional[Path]] = files

    def change_directory_dialog(self):
        try:
            self.output_directory: Path = Path(self.__get_directory_by_dialog())
        except FileExistsError:
            QMessageBox.warning(None,
                                'Предупреждение',
                                ('Директория не выбрана!\n'
                                 f'Будет использована директория по умолчанию:\n{str(self.output_directory)}'))
        self.update_label_text(self.output_directory_label,
                               str(self.output_directory))

    def __get_directory_by_dialog(self) -> Path:
        directory: str = QFileDialog.getExistingDirectory(
                self,
                'Выберите директорию для сохранения файла'
            )
        if not directory:
            raise FileExistsError('Не удалось получить доступ к директории!')
        return directory

    def __handle_message_after_successful_split(self, value: QMessageBox.StandardButton) -> None:
        match value:
            case QMessageBox.StandardButton.Open:
                os.startfile(self.output_directory)
            case _:
                pass

    def update_label_text(self, label: QLabel, text: str) -> None:
        label.setText(text)
