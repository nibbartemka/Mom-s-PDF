from pathlib import Path
import os
from typing import Optional, List

from PyQt6.QtWidgets import (
    QLabel,
    QFileDialog,
    QWidget,
    QPushButton,
    QMainWindow,
    QLineEdit,
    QFormLayout,
    QMessageBox
)
from PyQt6.QtGui import QPixmap, QIcon

from SplitTool import SplitTool, PageInterval, PageIntervalConverter
from .LayoutBuilder import GridLayoutBuilder
from config import DEFAULT_OUTPUT_PATH, STATIC_DIRECTORY_PATH


class IntervalEnteringWindow(QMainWindow):
    def __init__(self, output_directory: Path,
                 input_file: Path,
                 split_tool: SplitTool,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.output_directory: Path = output_directory
        self.split_tool: SplitTool = split_tool
        self.input_file: Path = input_file

        self.setWindowTitle('Укажите интeрвалы')

        central_widget: QWidget = QWidget()

        self.interval_input: QLineEdit = QLineEdit()
        self.interval_input.setPlaceholderText('Пример: 1-2 3-5 6-6')

        self.split_button: QPushButton = QPushButton('Разделить')
        self.split_button.clicked.connect(self.split_files)

        form_layout: QFormLayout = QFormLayout()
        form_layout.addRow('Укажите интервалы через пробел:', self.interval_input)
        form_layout.addRow('', self.split_button)

        central_widget.setLayout(
            form_layout
        )

        self.setCentralWidget(central_widget)

    def split_files(self) -> None:
        try:
            page_intervals: List[PageInterval] = [
                PageIntervalConverter.convert_line_to_page_interval(item)
                for item in self.interval_input.text().split()
            ]
            self.split_tool.split_file(self.input_file, self.output_directory,
                                       *page_intervals)
            question = QMessageBox.question(self,
                                            'Операция выполнена!\n',
                                            'Разделение файла прошло успешно. Перейти к директории?',
                                            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Open)
            self.__handle_message_after_successful_split(question)
        except ValueError as error:
            QMessageBox.critical(self, "Ошибка!",
                                 str(error))

    def __handle_message_after_successful_split(self, value: QMessageBox.StandardButton) -> None:
        match value:
            case QMessageBox.StandardButton.Open:
                os.startfile(self.output_directory)
                self.close()
            case _:
                self.close()


class SplitTab(QWidget):
    def __init__(self, split_tool: SplitTool, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.split_tool: SplitTool = split_tool

        self.output_directory: Path = DEFAULT_OUTPUT_PATH
        self.input_file: Optional[Path] = None

        self.head_text_label: QLabel = QLabel('РАЗДЕЛИТЕ СВОЙ PDF-ФАЙЛ')
        self.head_text_label.setStyleSheet(
            '''
                text-align: left;
                font-size: 32px;
                font-family: Roboto;
                color: white;
                font-weight: bold;
            '''
        )

        self.beneath_text_label: QLabel = QLabel('ВСЕГО В ОДИН КЛИК')
        self.beneath_text_label.setStyleSheet(
            '''
                font-size: 24px;
                font-family: Roboto;
                color: white;
                font-weight: bold;
            '''
        )

        self.mascot_image = QLabel()
        self.mascot_pixmap = QPixmap(str(STATIC_DIRECTORY_PATH
                                         / 'img'
                                         / 'Ali-e_split.svg'))
        self.mascot_image.setPixmap(self.mascot_pixmap)
        self.mascot_image.setStyleSheet(
            '''
                margin: auto;
            '''
        )

        self.input_files_select_button: QPushButton = QPushButton('РАЗДЕЛИТЬ')
        self.input_files_select_button.clicked.connect(self.split_files)
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
                    background-color: #E74848;
                }
            '''
        )
        self.output_directory_pixmap: QIcon = QIcon(str(STATIC_DIRECTORY_PATH
                                                        / 'img'
                                                        / 'folder_icon.svg'))
        self.output_directory_change_button.setIcon(self.output_directory_pixmap)

        grid = (
            GridLayoutBuilder()
            .add_widget(self.head_text_label, 0, 0, 1, 3)  # row, col, row_span, col_span
            .add_widget(self.beneath_text_label, 1, 0, 1, 3)
            .add_widget(self.input_files_select_button, 2, 0, 1, 1)
            .add_widget(self.output_directory_label, 5, 0, 1, 1)
            .add_widget(self.output_directory_change_button, 5, 1, 1, 1)
            .add_widget(self.mascot_image, 0, 4, 5, 5)
            .build()
        )

        self.setLayout(grid)

    def split_files(self) -> None:
        try:
            self.select_files_dialog()
            self.interval_intering_window: QMainWindow = IntervalEnteringWindow(self.output_directory,
                                                                                self.input_file,
                                                                                self.split_tool)
            self.interval_intering_window.show()
        except FileExistsError:
            QMessageBox.warning(None,
                                'Предупреждение',
                                'Файл не выбран!')

    def select_files_dialog(self) -> None:
        file, _ = QFileDialog.getOpenFileName(
                    self,
                    'Выберите PDF-файл',
                    '',
                    'PDF files (*.pdf)'
                )
        if not file:
            raise FileExistsError('Не удалось получить доступ к файлу!')
        self.input_file: Optional[Path] = file

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
        self.interval_intering_window: QMainWindow = IntervalEnteringWindow(self.output_directory,
                                                                            self.input_file,
                                                                            self.split_tool)

    def __get_directory_by_dialog(self) -> Path:
        directory: str = QFileDialog.getExistingDirectory(
                self,
                'Выберите директорию для сохранения файла'
            )
        if not directory:
            raise FileExistsError('Не удалось получить доступ к директории!')
        return directory

    def update_label_text(self, label: QLabel, text: str) -> None:
        label.setText(text)
