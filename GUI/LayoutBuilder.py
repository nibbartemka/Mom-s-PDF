from typing import Protocol, TypeAlias

from PyQt6.QtWidgets import (
    QGridLayout,
    QBoxLayout,
    QHBoxLayout,
    QVBoxLayout,
    QWidget
)


Layout: TypeAlias = (QGridLayout
                     | QBoxLayout
                     | QVBoxLayout
                     | QHBoxLayout)


class LayoutBuilder(Protocol):
    def add_widget(self, widget: QWidget,
                   *args, **kwargs) -> 'LayoutBuilder':
        pass

    def build(self) -> Layout:
        pass


class GridLayoutBuilder(object):
    def __init__(self) -> None:
        self.grid = QGridLayout()

    def add_widget(self, widget: QWidget,
                   *args, **kwargs) -> LayoutBuilder:
        self.grid.addWidget(widget, *args, **kwargs)
        return self

    def build(self) -> Layout:
        return self.grid


class HBoxLayoutBuilder(object):
    def __init__(self) -> None:
        self.horizontal_box = QHBoxLayout()

    def add_widget(self, widget: QWidget,
                   *args, **kwargs) -> LayoutBuilder:
        self.horizontal_box.addWidget(widget, *args, **kwargs)
        return self

    def build(self) -> Layout:
        return self.horizontal_box


class VBoxLayoutBuilder(object):
    def __init__(self) -> None:
        self.vertical_box = QVBoxLayout()

    def add_widget(self, widget: QWidget,
                   *args, **kwargs) -> LayoutBuilder:
        self.vertical_box.addWidget(widget, *args, **kwargs)
        return self

    def build(self) -> Layout:
        return self.vertical_box
