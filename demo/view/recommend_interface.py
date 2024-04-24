# coding:utf-8
from qfluentwidgets import (SettingCardGroup,OptionsConfigItem,
                            OptionsSettingCard, PushSettingCard,
                            PrimaryPushSettingCard, ScrollArea,
                            ExpandLayout,RangeSettingCard,
                            TableWidget)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar
from PyQt6.QtCore import Qt,QThread,pyqtSignal
from PyQt6.QtWidgets import QWidget, QLabel, QFileDialog, QTableWidgetItem,QHeaderView

from components.file_list_setting_card import FileListSettingCard
from components.edit_setting_card import EditSettingCard
from utils.style_sheet import StyleSheet
from utils.settings import cfg
import csv
#================operations=================
from operations.user_video_rating import user_video_rating  #模拟生成评分矩阵
from operations.load_data import load_data  #加载评分矩阵
from operations.CF_user import CF_user
from operations.find_video_title import find_video_title
from operations.CF_SVD import SVD

class WorkThread(QThread):
    finish_signal = pyqtSignal(list)
    def __init__(self, recAlgorithm, recUid, topk, filepath,parent=None):
        super(WorkThread, self).__init__(parent)
        self.recAlgorithm = recAlgorithm
        self.recUid = recUid
        self.topk = topk
        self.filepath = filepath
    def run(self):

        ratings_matrix = load_data()
        res = []
        rec_table = []
        if self.recAlgorithm == 'User based CF':
            cf_user = CF_user(ratings_matrix, self.recUid, top_n=self.topk)
            cf_user.compute_person_similarity()
            res = cf_user.top_k_rs_result()
        if self.recAlgorithm == 'SVD CF':
            svd = SVD(ratings_matrix, self.recUid,self.topk)
            svd.compute_svd()
            res = svd.predict_rating()
        rec_table = find_video_title(self.filepath, res)
        self.finish_signal.emit(rec_table)  
        return
    
class RecommendInterface(ScrollArea):
    """ Setting interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # 算法参数
        ## 文件
        self.videoTitleFileFolder = cfg.videoTitleFiles.value #视频数据集文件夹
        ## 评分
        self.userNum = cfg.userNum.value
        self.videoPerPerson = cfg.videoPerPerson.value
        ## 推荐
        self.recAlgorithm = cfg.recChoose.value
        self.recTopK = cfg.recTopk.value


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
        

        self.downloadFolderCard = PushSettingCard(
            '下载',
            FIF.DOWNLOAD,
            '下载评分数据集',
            cfg.get(cfg.downloadFolder),
            self.pathGroup
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
        self.tableView = TableWidget(self.resGroup)
        
        self.__initTableView()

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
        self.pathGroup.addSettingCard(self.downloadFolderCard)

        self.ratingGroup.addSettingCard(self.userNumSetting)
        self.ratingGroup.addSettingCard(self.videoPerPersonSetting)
        self.ratingGroup.addSettingCard(self.ratingButton)

        self.recGroup.addSettingCard(self.recChooseSetting)
        self.recGroup.addSettingCard(self.recUidSetting)
        
        self.resGroup.addSettingCard(self.topkSetting)
        self.resGroup.addSettingCard(self.okButton)
        self.resGroup.addSettingCard(self.tableView)
        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.pathGroup)
        self.expandLayout.addWidget(self.ratingGroup)
        self.expandLayout.addWidget(self.recGroup)
        self.expandLayout.addWidget(self.resGroup)
        
        #self.expandLayout.addWidget(self.tableView)

    def __initTableView(self):
        self.tableView.setBorderVisible(True)
        self.tableView.setBorderRadius(8)
        self.tableView.setWordWrap(False) #取消自动换行
        self.tableView.setRowCount(10)
        self.tableView.setColumnCount(2)
        self.tableView.setHorizontalHeaderLabels(['id','标题'])
        data = ['-1','这里什么也没有~']

        for j in range(2):
            self.tableView.setItem(0, j, QTableWidgetItem(data[j]))
                
        self.tableView.verticalHeader().hide() # 隐藏垂直表头
        #self.tableView.resizeColumnsToContents() #列自适应
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        #self.tableView.setFixedSize()
        self.tableView.adjustSize()
        self.tableView.setObjectName("tableView")

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
    def __onDownloadFolderCardClicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), "./")
        if not folder or cfg.get(cfg.downloadFolder) == folder:
            return

        cfg.set(cfg.downloadFolder, folder)
        self.downloadFolderCard.setContent(folder)

    def __onRecUidChange(self, text:str):
        self.recUid = int(text)

    def __onTopKChange(self, k:int):
        self.recTopK = k

    def __onUserNumChange(self, i:int):
        self.userNum = i

    def __onVideoPerPersonChange(self, i:int):
        self.videoPerPerson = i
    
    def __onRecChooseChange(self, cfgItem:OptionsConfigItem):
        self.recAlgorithm = cfgItem.value

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        # 文件 
        self.videoTitleFolderCard.fileChanged.connect(self.__onVideoTitleFileFolderChange)
        self.downloadFolderCard.clicked.connect(
            self.__onDownloadFolderCardClicked)
        # 评分
        self.userNumSetting.valueChanged.connect(self.__onUserNumChange)
        self.videoPerPersonSetting.valueChanged.connect(self.__onVideoPerPersonChange)
        self.ratingButton.clicked.connect(self.__buildRatingMatrix)
        # 推荐
        self.recChooseSetting.optionChanged.connect(self.__onRecChooseChange)
        self.recUidSetting.valueChanged.connect(self.__onRecUidChange)
        # 结果
        self.topkSetting.valueChanged.connect(self.__onTopKChange)
        self.okButton.clicked.connect(self.__recommendStart)
        

    def __buildRatingMatrix(self):
        self.__showWaitingTooltip("正在生成")
        num_lines = 0
        # 获取视频总数
        with open(self.videoTitleFileFolder[0],'r',newline='',encoding='utf-8-sig') as file:
            csv_reader = csv.reader(file)
            for _ in csv_reader:
                num_lines += 1
        user_video_rating(self.userNum, num_lines, self.videoPerPerson)
        self.__showSucessTooltip('生成评分矩阵成功')

    def __recommendStart(self):
        if self.videoTitleFileFolder == []:
            self.__showWarningTooltip('找不到视频标题数据集文件')
            return
        if not hasattr(self,'recUid'):
            self.__showWarningTooltip('还未设置推荐用户的id')
            return
        self.__showWaitingTooltip("正在生成推荐结果")
        self.th = WorkThread(self.recAlgorithm,self.recUid, self.recTopK, self.videoTitleFileFolder[0])
        self.th.finish_signal.connect(self.__recommendFinish)
        self.th.start()

    def __recommendFinish(self, rec_table:list):
        row_count = len(rec_table) if rec_table else 0
        self.tableView.setRowCount(row_count)
        for i in range(row_count):
            for j in range(2):
                self.tableView.setItem(i, j, QTableWidgetItem(rec_table[i][j]))
        self.__showSucessTooltip('生成推荐结果成功')
        
        
        