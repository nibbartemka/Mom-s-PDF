from PyQt6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QWidget
)
from PyQt6.QtGui import QIcon

from MergeTool import PDFMergeTool
from SplitTool import PDFSplitTool
from .MergeTab import MergeTab
from .SplitTab import SplitTab
from .LayoutBuilder import GridLayoutBuilder, HBoxLayoutBuilder
from config import STATIC_DIRECTORY_PATH


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MOM'S PDF")
        self.setWindowIcon(QIcon(str(STATIC_DIRECTORY_PATH
                                     / 'img'
                                     / 'Ali-e_window_icon.svg')))
        self.setFixedSize(800, 400)

        tab_widget: QTabWidget = QTabWidget()

        merge_tab: QWidget = QWidget()
        merge_tab.setLayout(
            HBoxLayoutBuilder()
            .add_widget(MergeTab(PDFMergeTool()))
            .build()
        )
        merge_tab.setStyleSheet(
            '''
                background-color: #2372E9;
                border-bottom-left-radius: 15%;
                border-bottom-right-radius: 15%;
                border-top-right-radius: 15%;
            '''
        )

        split_tab: QWidget = QWidget()
        split_tab.setLayout(
            HBoxLayoutBuilder()
            .add_widget(SplitTab(PDFSplitTool()))
            .build()
        )
        split_tab.setStyleSheet(
            '''
                background-color: #EB3131;
                border-bottom-left-radius: 15%;
                border-bottom-right-radius: 15%;
                border-top-right-radius: 15%;
            '''
        )

        tab_widget.addTab(merge_tab, 'ОБЪЕДИНИТЬ PDF')
        tab_widget.addTab(split_tab, 'РАЗДЕЛИТЬ PDF')
        tab_widget.setStyleSheet(
            '''
                QTabWidget::pane {
                    border: none;
                }

                QTabBar::tab {
                    color: white;
                    font-family: Roboto;
                    font-weight: bold;
                    padding: 10%;
                    border-top-left-radius: 15%;
                    border-top-right-radius: 15%;
                }

                QTabBar::tab:!selected {
                    background-color: LightGrey;
                }

                QTabBar::tab:selected {
                    background-color: Snow;
                    color: Black;
                }

                QTabBar::tab:hover {
                    background-color: #E5E0E0;
                    color: DarkGrey;
                }
            '''
        )

        central_widget = QWidget()
        central_widget.setLayout(
            GridLayoutBuilder()
            .add_widget(tab_widget)
            .build()
        )

        self.setCentralWidget(central_widget)
