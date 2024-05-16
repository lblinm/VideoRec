# coding:utf-8
from qfluentwidgets import (SettingCardGroup, ScrollArea,
                            ExpandLayout,ComboBoxSettingCard,
                            PrimaryPushSettingCard, InfoBar,
                            IndeterminateProgressBar)
from qfluentwidgets import FluentIcon as FIF
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (QWidget, QLabel, QLabel)
from components.file_list_setting_card import FileListSettingCard
from components.tabInterface import TabInterface
from utils.style_sheet import StyleSheet
from utils.settings import cfg
from utils.video_type import VIDEO_TYPE
from operations.category import category
from operations.load_data import load_data
from operations.userActionCluster import userActionCluster
from operations.userCluster import userCluster

class ThreadCluster(QThread):
    finished_signal = pyqtSignal(int, list, list, str, str)
    def __init__(self, videoOrUser:bool):
        super().__init__()
        self.videoOrUser = videoOrUser
    def run(self):
        x, y,tabTitle, detail = None, None, None, ''
        if self.videoOrUser:
            if cfg.videoClusterAlgorithm.value == "基于原有标签":
                y = category(cfg.videoTitleFiles.value[0])
                x = list(range(len(VIDEO_TYPE)))
                tabTitle = "基于原有标签的视频聚类结果"
                detail = "### 详细信息\n"
                for i in range(len(x)):
                    detail += f"{i}. {VIDEO_TYPE[i]}: {y[i]}\n"

            elif cfg.videoClusterAlgorithm.value == "基于用户行为":
                ratings_matrix = load_data(matrix_kind=1)
                x, y, silhouette = userActionCluster(ratings_matrix)
                tabTitle = "基于用户行为的视频聚类结果"
                detail = f"### 详细信息\n轮廓系数: {round(silhouette, 3)}"
        else:
            if cfg.userClusterAlgorithm.value == "基于相似兴趣":
                ratings_matrix = load_data(matrix_kind=1) 
                x, y, silhouette = userCluster(ratings_matrix)
                tabTitle = "基于相似用户的用户聚类结果"
                detail = f"### 详细信息\n轮廓系数: {round(silhouette, 3)}"
        self.finished_signal.emit(0, x, y, tabTitle, detail)
        
class ClusterInterface(ScrollArea):
    """ Setting interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # label
        self.bar = IndeterminateProgressBar(self, start=False)
        self.recLabel = QLabel("聚类分析", self)
        # 数据集
        self.dataGroup = SettingCardGroup('数据集',self.scrollWidget)
        self.videoTitleFolderCard = FileListSettingCard(
            cfg.videoTitleFiles,
            '视频数据集文件',
            parent=self.dataGroup
        )
        self.ratingFolderCard = FileListSettingCard(
            cfg.ratingPath,
            "用户-视频评分矩阵数据集文件(可模拟生成)",
            parent=self.dataGroup
        )

        # 视频聚类
        self.videoClusterGroup = SettingCardGroup('视频聚类',self.scrollWidget)
        self.videoClusterAlgorithm = ComboBoxSettingCard(
            cfg.videoClusterAlgorithm,
            FIF.CALORIES,
            "聚类方式",
            "选择视频聚类的方式",
            texts=["基于原有标签", "基于用户行为"],
            parent=self.videoClusterGroup
        )
        self.videoClusterButton = PrimaryPushSettingCard(
            "确认",
            FIF.ACCEPT,
            "确认聚类",
            "以该方式展示聚类结果",
            parent=self.videoClusterGroup
        )
        self.drawVideoCluster = TabInterface(self.videoClusterGroup)
        
        # 用户聚类
        self.userClusterGroup = SettingCardGroup('用户聚类', self.scrollWidget)
        self.userClusterAlgorithm = ComboBoxSettingCard(
            cfg.userClusterAlgorithm,
            FIF.CALORIES,
            "聚类方式",
            "选择用户聚类的方式",
            texts=["基于相似兴趣"],
            parent=self.userClusterGroup
        )
        self.userClusterButton = PrimaryPushSettingCard(
            "确认",
            FIF.ACCEPT,
            "确认聚类",
            "以该方式展示聚类结果",
            parent=self.userClusterGroup
        )
        self.drawUserCluster = TabInterface(self.userClusterGroup)
        
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

        self.bar.resize(self.width(), self.bar.height())
        self.__initLayout()
        StyleSheet.CLUSTER_INTERFACE.apply(self)

        self.__connectSignalToSlot()
        

    def __initLayout(self):
        self.recLabel.move(36, 30)

        # add cards to group
        # 数据集
        self.dataGroup.addSettingCard(self.videoTitleFolderCard)
        self.dataGroup.addSettingCard(self.ratingFolderCard)
        # 视频聚类
        self.videoClusterGroup.addSettingCard(self.videoClusterAlgorithm)
        self.videoClusterGroup.addSettingCard(self.videoClusterButton)
        self.videoClusterGroup.addSettingCard(self.drawVideoCluster)
        # 用户聚类
        self.userClusterGroup.addSettingCard(self.userClusterAlgorithm)
        self.userClusterGroup.addSettingCard(self.userClusterButton)
        self.userClusterGroup.addSettingCard(self.drawUserCluster)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        
        self.expandLayout.addWidget(self.dataGroup)
        self.expandLayout.addWidget(self.videoClusterGroup)
        self.expandLayout.addWidget(self.userClusterGroup)

    def __connectSignalToSlot(self):
        self.videoClusterButton.clicked.connect(self.startVideoCluster)
        self.userClusterButton.clicked.connect(self.startUserCluster)

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

    def startVideoCluster(self):
        self.bar.start()
        self.__showWaitingTooltip("正在生成视频聚类结果")
        self.threadVideoCluster = ThreadCluster(True)
        self.threadVideoCluster.finished_signal.connect(self.drawVideoCluster.addDrawRes)
        self.threadVideoCluster.finished.connect(lambda: self.__showSucessTooltip("视频聚类成功"))
        self.threadVideoCluster.finished.connect(self.bar.stop)
        self.threadVideoCluster.start()
    
    def startUserCluster(self):
        self.bar.start()
        self.__showWaitingTooltip("正在生成用户聚类结果")
        self.threadUserCluster = ThreadCluster(False)
        self.threadUserCluster.finished_signal.connect(self.drawUserCluster.addDrawRes)
        self.threadUserCluster.finished.connect(lambda: self.__showSucessTooltip("用户聚类成功"))
        self.threadUserCluster.finished.connect(self.bar.stop)
        self.threadUserCluster.start()
    