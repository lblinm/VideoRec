# coding:utf-8
from qfluentwidgets import (SettingCardGroup,OptionsConfigItem,
                            OptionsSettingCard, PushSettingCard,
                            PrimaryPushSettingCard, ScrollArea,
                            ExpandLayout,RangeSettingCard)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar
from PyQt6.QtCore import Qt,QThread,pyqtSignal
from PyQt6.QtWidgets import QWidget, QLabel

from components.file_list_setting_card import FileListSettingCard
from components.edit_setting_card import EditSettingCard
from components.tabInterface import TabInterface
from utils.style_sheet import StyleSheet
from utils.settings import cfg
import csv
import os
#================operations=================
# from operations.user_video_rating import user_video_rating  #模拟生成评分矩阵
from operations.generate_rating_scores import generate_rating
from operations.load_data import load_data  #加载评分矩阵
from operations.CF_user import CF_user
from operations.find_video_title import find_video_title
from operations.CF_SVD import SVD
from operations.CB import CB_recommend
class WorkThread1(QThread):
    finish_signal = pyqtSignal(list)
    def __init__(self, parent=None):
        super(WorkThread1, self).__init__(parent)
        self.recAlgorithm = cfg.recChoose.value
        self.recUid = int(cfg.recUid.value)
        self.topk = cfg.recTopk.value
        self.filepath = cfg.videoTitleFiles.value[0]
    def run(self):
        res = []
        rec_table = []
        if self.recAlgorithm == 'User based CF':
            ratings_matrix = load_data(matrix_kind=1)
            cf_user = CF_user(ratings_matrix, self.recUid, top_n=self.topk)
            cf_user.compute_person_similarity()
            res = cf_user.top_k_rs_result()
        elif self.recAlgorithm == 'SVD CF':
            ratings_matrix = load_data(matrix_kind=0)
            svd = SVD(ratings_matrix, self.recUid,self.topk)
            svd.compute_svd()
            res = svd.predict_rating()
        elif self.recAlgorithm == 'Contend based':
            ratings_matrix = load_data(matrix_kind=1)
            res = CB_recommend(self.filepath, ratings_matrix, self.recUid, self.topk)
        rec_table = find_video_title(self.filepath, res)
        self.finish_signal.emit(rec_table)  
        return
    
class WorkThread2(QThread):
    def __init__(self, video_num, parent=None):
        super(WorkThread2, self).__init__(parent)
        self.tag_matrix = cfg.videoTitleFiles.value[0]
        self.video_num = video_num
        self.user_num = cfg.userNum.value
        self.videos_watched_per_user = cfg.videoPerPerson.value
    def run(self):
        generate_rating(self.tag_matrix, self.video_num, self.user_num, self.videos_watched_per_user)

class RecommendInterface(ScrollArea):
    """ Setting interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # label
        self.recLabel = QLabel("视频推荐", self)

        # 文件
        self.pathGroup = SettingCardGroup(
            '文件', self.scrollWidget)
        self.videoTitleFolderCard = FileListSettingCard(
            cfg.videoTitleFiles,
            '视频数据集文件',
            parent=self.pathGroup
        )
        


        # 评分
        self.ratingGroup = SettingCardGroup(
            '评分', self.scrollWidget)
      
        self.userNumSetting = RangeSettingCard(
            cfg.userNum,
            FIF.PEOPLE,
            '用户数量设置',
            '给视频评分的用户数量',
            self.ratingGroup
        )
        self.videoPerPersonSetting = RangeSettingCard(
            cfg.videoPerPerson,
            FIF.IOT,
            "用户观看视频数",
            "每一个用户给多少个视频评分",
            self.ratingGroup
        )
        self.ratingButton = PrimaryPushSettingCard(
            '确认',
            FIF.ACCEPT,
            '确认',
            '确认生成评分矩阵',
            self.ratingGroup
        )
        # 推荐
        self.recGroup = SettingCardGroup(
            '推荐', self.scrollWidget)
        self.recChooseSetting = OptionsSettingCard(
            cfg.recChoose,
            FIF.CALORIES,
            "推荐算法选择",
            "以哪一种算法做短视频推荐",
            texts=["User based CF","Item based CF","SVD CF","Content based"],
            parent=self.recGroup
        )
        self.recUidSetting = EditSettingCard(
            cfg.recUid,
            FIF.ASTERISK,
            "推荐用户选择",
            "输入想给其推荐视频的用户id",
            parent=self.recGroup
        )
        
        self.resGroup = SettingCardGroup(
            '结果',self.scrollWidget
        )
        self.topkSetting = RangeSettingCard(
            cfg.recTopk,
            FIF.TILES,
            "Top-K",
            "选择推荐结果的前几个返回",
            self.resGroup
        )
        
        self.okButton = PrimaryPushSettingCard(
            '确认',
            FIF.ACCEPT,
            '开始为ta推荐',
            '为ta推荐',
            self.resGroup
        )
        self.tabRecRes = TabInterface(self.resGroup)

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('settingInterface')

        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        self.recLabel.setObjectName('recLabel')

        self.__initLayout()
        StyleSheet.RECOMMEND_INTERFACE.apply(self)

        # initialize layout
        
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.recLabel.move(36, 30)

        # add cards to group
        self.pathGroup.addSettingCard(self.videoTitleFolderCard)


        self.ratingGroup.addSettingCard(self.userNumSetting)
        self.ratingGroup.addSettingCard(self.videoPerPersonSetting)
        self.ratingGroup.addSettingCard(self.ratingButton)

        self.recGroup.addSettingCard(self.recChooseSetting)
        self.recGroup.addSettingCard(self.recUidSetting)
        
        self.resGroup.addSettingCard(self.topkSetting)
        self.resGroup.addSettingCard(self.okButton)
        self.resGroup.addSettingCard(self.tabRecRes)
        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.pathGroup)
        self.expandLayout.addWidget(self.ratingGroup)
        self.expandLayout.addWidget(self.recGroup)
        self.expandLayout.addWidget(self.resGroup)
        

    def __onVideoTitleFileFolderChange(self, lis:list):
        self.videoTitleFileFolder = lis

    def __showWaitingTooltip(self, s:str):
        """ show restart tooltip """
        InfoBar.info(
            s,
            '请稍等...',
            duration=1500,
            parent=self
        )

    def __showWarningTooltip(self, s:str):
        InfoBar.warning(
            '警告',
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

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        # 文件 
        self.videoTitleFolderCard.fileChanged.connect(self.__onVideoTitleFileFolderChange)

        # 评分
        self.ratingButton.clicked.connect(self.__buildRatingMatrix)

        # 推荐
        self.okButton.clicked.connect(self.__recommendStart)
        

    def __buildRatingMatrix(self):
        self.__showWaitingTooltip("正在生成评分矩阵，这可能需要几分钟，请耐心等候~")
        num_lines = -1
        # 获取视频总数
        with open(cfg.videoTitleFiles.value[0],'r',newline='',encoding='utf-8-sig') as file:
            csv_reader = csv.reader(file)
            for _ in csv_reader:
                num_lines += 1
        # user_video_rating(self.userNum, num_lines, self.videoPerPerson)
        self.th2 = WorkThread2(num_lines)
        # generate_rating(self.videoTitleFileFolder[0],num_lines, self.userNum, self.videoPerPerson)
        self.th2.start()
        self.th2.finished.connect(lambda: self.__showSucessTooltip("生成评分矩阵成功"))

    def __recommendStart(self):
        if cfg.videoTitleFiles.value == []:
            self.__showWarningTooltip('找不到视频标题数据集文件')
            return
        if cfg.recUid.value == '':
            self.__showWarningTooltip('还未设置推荐用户的id')
            return
        if not os.path.exists(os.environ.get("DATA_PATH")+"\\ratings.csv"):
            self.__showWarningTooltip('还未生成评分矩阵')
            return
        self.__showWaitingTooltip("正在生成推荐结果")
        self.th1 = WorkThread1() 
        self.th1.finish_signal.connect(self.__recommendFinish)
        self.th1.start()

    def __recommendFinish(self, rec_table:list):
        title = ['id','标题']
        tabTitle = f'对用户{cfg.recUid.value}的推荐(使用{cfg.recChoose.value}算法)'
        self.tabRecRes.addTableRes(title, rec_table, tabTitle)
        
        
        