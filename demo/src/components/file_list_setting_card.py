# coding:utf-8
from typing import List
from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QPainter, QIcon
from PyQt6.QtWidgets import (QPushButton, QFileDialog, QWidget, QLabel,
                             QHBoxLayout, QToolButton, QSizePolicy)
from PyQt6.QtSvg import QSvgRenderer

from qfluentwidgets import ToolButton, PushButton, ConfigItem, qconfig, FluentIcon as FIF,Dialog,ExpandSettingCard



class fileItem(QWidget):
    """ file item """

    removed = pyqtSignal(QWidget)

    def __init__(self, file, parent=None):
        super().__init__(parent=parent)
        self.file = file
        self.hBoxLayout = QHBoxLayout(self)
        self.fileLabel = QLabel(file, self)
        self.removeButton = ToolButton(FIF.CLOSE, self)

        self.removeButton.setFixedSize(39, 29)
        self.removeButton.setIconSize(QSize(12, 12))

        self.setFixedHeight(53)
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        self.hBoxLayout.setContentsMargins(48, 0, 60, 0)
        self.hBoxLayout.addWidget(self.fileLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.addSpacing(16)
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.removeButton, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.removeButton.clicked.connect(
            lambda: self.removed.emit(self))


class FileListSettingCard(ExpandSettingCard):
    """ file list setting card """

    fileChanged = pyqtSignal(list)

    def __init__(self, configItem, title, content=None, directory="./", parent=None):
        """
        Parameters
        ----------
        configItem: RangeConfigItem
            configuration item operated by the card

        title: str
            the title of card

        content: str
            the content of card

        directory: str
            working directory of file dialog

        parent: QWidget
            parent widget
        """
        super().__init__(FIF.FOLDER, title, content, parent)
        self.configItem = configItem
        self._dialogDirectory = directory
        self.addfileButton = PushButton('添加文件', self, FIF.FOLDER_ADD)

        self.files = qconfig.get(configItem).copy()   # type:List[str]
        self.__initWidget()

    def __initWidget(self):
        self.addWidget(self.addfileButton)

        # initialize layout
        self.viewLayout.setSpacing(0)
        self.viewLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        for file in self.files:
            self.addFileItem(file)

        self.addfileButton.clicked.connect(self.__showfileDialog)

    def __showfileDialog(self):
        """ show file dialog """
        file,_ = QFileDialog.getOpenFileName(
            self, '选择文件', self._dialogDirectory,"CSV Files (*.csv)")

        if not file or file in self.files:
            return

        self.addFileItem(file)
        self.files.append(file)
        qconfig.set(self.configItem, self.files)
        self.fileChanged.emit(self.files)

    def addFileItem(self, file):
        """ add file item """
        item = fileItem(file, self.view)
        item.removed.connect(self.__showConfirmDialog)
        self.viewLayout.addWidget(item)
        item.show()
        self._adjustViewSize()

    def __showConfirmDialog(self, item):
        """ show confirm dialog """
        name = Path(item.file).name
        title = self.tr('是否确认删除该文件?')
        content = "如果将" + f'"{name}"' + "文件从列表中移除，则该文件不会再出现在列表中，但不会被删除"
        w = Dialog(title, content, self.window())
        w.yesSignal.connect(lambda: self.__removeFile(item))
        w.exec()

    def __removeFile(self, item):
        """ remove file """
        if item.file not in self.files:
            return

        self.files.remove(item.file)
        self.viewLayout.removeWidget(item)
        item.deleteLater()
        self._adjustViewSize()

        self.fileChanged.emit(self.files)
        qconfig.set(self.configItem, self.files)
