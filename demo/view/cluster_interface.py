# coding:utf-8
from qfluentwidgets import (SettingCardGroup,setFont, ScrollArea,
                            ExpandLayout,ComboBoxSettingCard,
                            PrimaryPushSettingCard)
from qfluentwidgets import FluentIcon as FIF
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QLabel, QLabel)
from components.file_list_setting_card import FileListSettingCard
from components.tabInterface import TabInterface
from utils.style_sheet import StyleSheet
from utils.settings import cfg
from utils.video_type import VIDEO_TYPE
from operations.category import category
from operations.load_data import load_data
from operations.userActionCluster import userActionCluster

class ClusterInterface(ScrollArea):
    """ Setting interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # label
        self.recLabel = QLabel("聚类分析", self)
        # 数据集
        self.dataGroup = SettingCardGroup('数据集',self.scrollWidget)
        self.videoTitleFolderCard = FileListSettingCard(
            cfg.videoTitleFiles,
            '视频数据集文件',
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

        self.__initLayout()
        StyleSheet.CLUSTER_INTERFACE.apply(self)

        self.__connectSignalToSlot()
        

    def __initLayout(self):
        self.recLabel.move(36, 30)

        # add cards to group
        # 数据集
        self.dataGroup.addSettingCard(self.videoTitleFolderCard)
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
        self.videoClusterButton.clicked.connect(self.videoCluster)

    def videoCluster(self):
        if cfg.videoClusterAlgorithm.value == "基于原有标签":
            h = category(cfg.videoTitleFiles.value[0])
            x = list(range(len(VIDEO_TYPE)))
            tabTitle = "基于原有标签的视频聚类结果"
            detail = "### 详细信息 \n"
            for i in range(len(x)):
                detail += f'{i}. {VIDEO_TYPE[i]}: {h[i]}\n'
        if cfg.videoClusterAlgorithm.value == "基于用户行为":
            ratings_matrix = load_data(matrix_kind=1)
            x, h = userActionCluster(ratings_matrix)
            tabTitle = "基于用户行为的视频聚类结果"
            detail = None
        self.drawVideoCluster.addDrawRes(0, x, h, tabTitle, detail)

