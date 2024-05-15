# coding:utf-8
from qfluentwidgets import (SettingCardGroup,ScrollArea,
                            ExpandLayout,PrimaryPushSettingCard,
                            ComboBoxSettingCard, RangeSettingCard)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar
from PyQt6.QtCore import Qt, QThread
from PyQt6.QtWidgets import (QWidget, QLabel, QLabel)
import os
from components.file_list_setting_card import FileListSettingCard
from components.edit_setting_card import EditSettingCard
from components.tabInterface import TabInterface
from utils.style_sheet import StyleSheet
from utils.settings import cfg
from operations.generate_time_series import generate_time_series

class ThreadGenerateTimeSeries(QThread):
    def __init__(self):
        super().__init__()
        self.file_path = cfg.videoTitleFiles.value[0]
    
    def run(self):
        generate_time_series(self.file_path)

class ThreadPredict(QThread):
    def __init__(self):
        super().__init__()
    def run(self):
        return
    
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
            '视频标题数据集文件',
            parent=self.dataGroup
        )
        self.predictFolderCard = FileListSettingCard(
            cfg.timeSeriesPath,
            '视频播放量时间序列数据集文件(可模拟生成)',
            parent=self.dataGroup
        )
        self.videoTimeSeriesButton = PrimaryPushSettingCard(
            '确认',
            FIF.ACCEPT,
            '生成播放量数据集',
            '开始基于视频标题数据集生成播放量时间序列数据集',
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
        self.predictDaysSetting = RangeSettingCard(
            cfg.predictDays,
            FIF.SEARCH,
            '预测天数',
            '选择预测视频未来几天的播放量',
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
        self.dataGroup.addSettingCard(self.predictFolderCard)
        self.dataGroup.addSettingCard(self.videoTimeSeriesButton)
        self.predictGroup.addSettingCard(self.predictDaysSetting)
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
        self.videoTimeSeriesButton.clicked.connect(self.startGenerateTimeSeries)
    
    def predict(self):
        title = ['id','标题']
        x = [1,2,3,4,5,6,7,8,9,10]
        y = [213,1232,324,23432,432432,43234,32432,32432,3243,32432]
        self.drawPredict.addDrawRes(1, x, y, '测试')
    
    def __showWaitingTooltip(self, s:str):
        InfoBar.info(
            '稍等',
            s,
            duration=1500,
            parent=self
        )
    def __showSucessTooltip(self, s:str):
        InfoBar.success(
            '成功',
            s,
            duration=1500,
            parent=self
        )
    def startGenerateTimeSeries(self):
        self.__showWaitingTooltip('正在生成视频播放量时间序列数据集')
        self.threadGenerateTimeSeries = ThreadGenerateTimeSeries()
        self.threadGenerateTimeSeries.start()
        self.threadGenerateTimeSeries.finished.connect(lambda: self.__showSucessTooltip('已生成播放量时间序列数据集'))
        
        time_series_path = os.environ.get('DATA_PATH')+'\\time_series.csv'
        self.predictFolderCard.addFileItem(time_series_path)
        cfg.set(cfg.timeSeriesPath, [time_series_path])
        
    def startPredict(self):
        self.__showWaitingTooltip('正在预测视频未来播放量')
        self.threadPredict = ThreadPredict()
    
        self.threadPredict.finished.connect(lambda: self.__showSucessTooltip('已生成预测播放量'))