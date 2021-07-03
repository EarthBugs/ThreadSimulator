from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QWidget


class UILoader:
    def __init__(self, file_dir) -> None:
        self.__ui_file = QFile(file_dir)
        self.__ui_file.open(QFile.ReadOnly)
        self.__ui_file.close()

        self.__ui = QUiLoader().load(self.__ui_file)

    def get_ui(self) -> QWidget:
        return self.__ui
