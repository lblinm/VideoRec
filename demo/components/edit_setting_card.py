# coding:utf-8
from typing import Union

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QIcon, QPainter
from PyQt6.QtWidgets import (QFrame, QHBoxLayout, QLabel, QToolButton,
                             QVBoxLayout, QPushButton)
from qfluentwidgets import  LineEdit, SettingCard, qconfig,FluentIconBase


class EditSettingCard(SettingCard):

  valueChanged = pyqtSignal(str)

  def __init__(self, configItem, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
    """
    Parameters
    ----------
    configItem: EditSettingCard
        configuration item operated by the card

    icon: str | QIcon | FluentIconBase
        the icon to be drawn

    title: str
        the title of card

    content: str
        the content of card

    parent: QWidget
        parent widget
    """
    super().__init__(icon, title, content, parent)
    self.configItem = configItem
    self.lineEdit = LineEdit(self)
    
    self.hBoxLayout.addStretch(1)
    self.hBoxLayout.addSpacing(6)
    self.hBoxLayout.addWidget(self.lineEdit, 0, Qt.AlignmentFlag.AlignRight)
    self.hBoxLayout.addSpacing(16)

    configItem.valueChanged.connect(self.setValue)
    self.lineEdit.textChanged.connect(self.__onValueChanged)

  def __onValueChanged(self, value: str):
    """ slider value changed slot """
    self.setValue(value)
    self.valueChanged.emit(value)

  def setValue(self, value):
    qconfig.set(self.configItem, value)
    self.lineEdit.setText(str(value))