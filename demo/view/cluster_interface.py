# coding:utf-8
from qfluentwidgets import (SettingCardGroup,
                            OptionsSettingCard, PushSettingCard,
                            PrimaryPushSettingCard, ScrollArea,
                            ExpandLayout,RangeSettingCard,
                            TableWidget)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QFileDialog, QTableWidgetItem,QHeaderView

from components.file_list_setting_card import FileListSettingCard
from components.edit_setting_card import EditSettingCard
from utils.style_sheet import StyleSheet
from utils.settings import cfg

class ClusterInterface(ScrollArea):
    """ Setting interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # label
        self.recLabel = QLabel("视频聚类", self)



        
        


        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('clusterInterface')

        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        self.recLabel.setObjectName('recLabel')

        self.__initLayout()
        StyleSheet.CLUSTER_INTERFACE.apply(self)

        # initialize layout
        

    def __initLayout(self):
        self.recLabel.move(36, 30)

        # add cards to group
       
        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        
        #self.expandLayout.addWidget(self.tableView)

 



