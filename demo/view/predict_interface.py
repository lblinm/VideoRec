# coding:utf-8
from qfluentwidgets import (SettingCardGroup,setFont, ScrollArea,
                            ExpandLayout,TableWidget, TabBar,CheckBox,
                            qrouter,PrimaryPushSettingCard,
                            ComboBoxSettingCard)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (QWidget, QLabel, QTableWidgetItem,QHeaderView,
                             QStackedWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame)
from components.file_list_setting_card import FileListSettingCard
from components.edit_setting_card import EditSettingCard
from components.tabInterface import TabInterface
from utils.style_sheet import StyleSheet
from utils.settings import cfg
import pyqtgraph as pg
import random
class PredictInterface(ScrollArea):
    """ Setting interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # label
        self.recLabel = QLabel("热度预测", self)
        
        # 数据集
        self.dataGroup = SettingCardGroup('数据集',self.scrollWidget)
        self.videoTitleFolderCard = FileListSettingCard(
            cfg.videoTitleFiles,
            '视频数据集文件',
            parent=self.dataGroup
        )

        # 预测
        self.predictGroup = SettingCardGroup('预测', self.scrollWidget)
        self.predictAlgorithmSetting = ComboBoxSettingCard(
            cfg.predictAlgorithm,
            FIF.CALORIES,
            '算法',
            '选择时间序列预测的算法',
            texts=['ARIMA','Holt-Winters'],
            parent=self.predictGroup
        )
        self.vidSetting = EditSettingCard(
            cfg.vidPre,
            FIF.MOVIE,
            "视频ID",
            "输入想要预测的视频的ID",
            parent=self.predictGroup
        )
        self.predictButtonCard = PrimaryPushSettingCard(
            '确认',
            FIF.ACCEPT,
            '确认预测',
            '开始为该视频预测未来播放量变化',
            self.predictGroup
        )
        self.drawPredict = TabInterface(self)
        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('PredictInterface')

        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        self.recLabel.setObjectName('recLabel')

        self.__initLayout()
        StyleSheet.PREDICT_INTERFACE.apply(self)

        # initialize layout
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.recLabel.move(36, 30)

        # add cards to group
        self.dataGroup.addSettingCard(self.videoTitleFolderCard)
        self.predictGroup.addSettingCard(self.predictAlgorithmSetting)
        self.predictGroup.addSettingCard(self.vidSetting)
        self.predictGroup.addSettingCard(self.predictButtonCard)
        self.predictGroup.addSettingCard(self.drawPredict)
        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        
        self.expandLayout.addWidget(self.dataGroup)
        self.expandLayout.addWidget(self.predictGroup)
        #self.expandLayout.addWidget(self.tableView)

    def __connectSignalToSlot(self):
        self.predictButtonCard.clicked.connect(self.predict)
    
    def predict(self):
        title = ['id','标题']
        data = [['1','2614873627958v 34n3v8924732947'],
                ['2','32433huhdkjfdsoiafjdsiofjdsioajf'],
                ['1','2614873627958v 34n3v8924732947'],
                ['2','32433huhdkjfdsoiafjdsiofjdsioajf'],
                ['1','2614873627958v 34n3v8924732947'],
                ['2','32433huhdkjfdsoiafjdsiofjdsioajf'],
                ['1','2614873627958v 34n3v8924732947'],
                ['2','32433huhdkjfdsoiafjdsiofjdsioajf'],
                ]
        tabTitle = "测试"
        self.drawPredict.addTableRes(title, data, tabTitle)
 