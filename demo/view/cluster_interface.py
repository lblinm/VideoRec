# coding:utf-8
from qfluentwidgets import (SettingCardGroup,setFont,
                            OptionsSettingCard, PushSettingCard,
                            PrimaryPushSettingCard, ScrollArea,
                            ExpandLayout,RangeSettingCard,
                            TableWidget, TabBar,CheckBox,BodyLabel,
                            SpinBox,ComboBox,qrouter,TabCloseButtonDisplayMode)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (QWidget, QLabel, QFileDialog, QTableWidgetItem,QHeaderView,
                             QStackedWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QSizePolicy)
from components.file_list_setting_card import FileListSettingCard
from components.edit_setting_card import EditSettingCard
from utils.style_sheet import StyleSheet
from utils.settings import cfg
import pyqtgraph as pg
import random
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
        
        # 视频聚类
        self.clusterGroup = SettingCardGroup('视频、用户聚类',self.scrollWidget)
        self.videoTitleFolderCard = FileListSettingCard(
            cfg.videoTitleFiles,
            '视频数据集文件',
            parent=self.clusterGroup
        )
        self.showClusterResult = tabInterface(self.clusterGroup)
        self.showClusterResult.detailSignal.connect(self.resetTableView)

        self.detailLabel = QLabel("详细信息", self)
        setFont(self.detailLabel, 20)
        self.detailLabel.adjustSize()
        self.tableView = TableWidget(self.clusterGroup)
        

        self.__initTableView()
        
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
        self.clusterGroup.addSettingCard(self.videoTitleFolderCard)
        self.clusterGroup.addSettingCard(self.showClusterResult)
        self.clusterGroup.addSettingCard(self.detailLabel)
        self.clusterGroup.addSettingCard(self.tableView)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.clusterGroup)
        #self.expandLayout.addWidget(self.tableView)

    def __initTableView(self):
        self.tableView.setBorderVisible(True)
        self.tableView.setBorderRadius(8)
        self.tableView.setWordWrap(False) #取消自动换行
        self.tableView.setRowCount(5)
        self.tableView.setColumnCount(3)
        self.tableView.setHorizontalHeaderLabels(['横轴','说明','数量'])
        # data = ['-1','这里什么也没有~']

        # for j in range(2):
        #     self.tableView.setItem(0, j, QTableWidgetItem(data[j]))
                
        self.tableView.verticalHeader().hide() # 隐藏垂直表头
        #self.tableView.resizeColumnsToContents() #列自适应
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        #self.tableView.setFixedSize()
        self.tableView.adjustSize()
        self.tableView.setObjectName("tableView")

    def resetTableView(self,detailInfo:list):
        row_count = len(detailInfo)
        self.tableView.setRowCount(row_count)
        for i in range(row_count):
            for j in range(3):
                item = QTableWidgetItem(detailInfo[i][j])
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tableView.setItem(i, j, item)

class tabInterface(QWidget):
    """ Tab interface """
    detailSignal = pyqtSignal(list)
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.tabCount = 1

        self.tabBar = TabBar(self)
        self.stackedWidget = QStackedWidget(self)
        self.tabView = QWidget(self)
        self.controlPanel = QFrame(self)

        self.existCateCheckBox = CheckBox("按已有类别",self)
        self.userActionCateCheckBox = CheckBox("按相似用户群体",self)  
        self.simiLikeCateCheckBox = CheckBox("按相似观看兴趣",self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout(self.tabView)
        self.panelLayout = QVBoxLayout(self.controlPanel)

        self.videoClusterLabel = QLabel("视频聚类",self)
        self.userClusterLabel = QLabel("用户聚类",self)

        # 绘图
        pg.setConfigOptions(leftButtonPan = False)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        # add items to pivot
        self.__initWidget()

    def __initWidget(self):
        self.initLayout()

        self.tabBar.setScrollable(True)

        self.controlPanel.setObjectName('controlPanel')
        self.videoClusterLabel.setObjectName('clusterLabel')
        self.userClusterLabel.setObjectName('clusterLabel')
        StyleSheet.TAB_INTERFACE.apply(self)

        self.connectSignalToSlot()

        # qrouter.setDefaultRouteKey(
        #     self.stackedWidget, self.songInterface.objectName())

    def connectSignalToSlot(self):
        self.existCateCheckBox.stateChanged.connect(self.addExistCateTab)
        self.userActionCateCheckBox.stateChanged.connect(self.addUserActionCateTab)

        self.tabBar.tabAddRequested.connect(self.addTab)
        self.tabBar.tabCloseRequested.connect(self.removeTab)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)

    def initLayout(self):
        self.tabBar.setTabMaximumWidth(150)

        self.setFixedHeight(280)
        self.controlPanel.setFixedWidth(220)
        self.hBoxLayout.addWidget(self.tabView, 1)
        self.hBoxLayout.addWidget(self.controlPanel, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addWidget(self.tabBar)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.panelLayout.setSpacing(8)
        self.panelLayout.setContentsMargins(14, 16, 14, 14)
        self.panelLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.panelLayout.addWidget(self.videoClusterLabel)
        self.panelLayout.addWidget(self.existCateCheckBox)
        self.panelLayout.addWidget(self.userActionCateCheckBox)
        self.panelLayout.addSpacing(4)
        self.panelLayout.addWidget(self.userClusterLabel)
        self.panelLayout.addWidget(self.simiLikeCateCheckBox)
        # self.panelLayout.addSpacing(4)

        # self.panelLayout.addSpacing(4)

    def addSubInterface(self, widget, objectName, text, icon):
        widget.setObjectName(objectName)
        widget.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.stackedWidget.addWidget(widget)
        self.tabBar.addTab(
            routeKey=objectName,
            text=text,
            icon=icon,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onDisplayModeChanged(self, index):
        mode = self.closeDisplayModeComboBox.itemData(index)
        self.tabBar.setCloseButtonDisplayMode(mode)

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        if not widget:
            return

        self.tabBar.setCurrentTab(widget.objectName())
        qrouter.push(self.stackedWidget, widget.objectName())

    def addTab(self):
        text = f'啊哈哈鸡汤来喽({self.tabCount})'
        textPool = [
            '仅仅活着是不够的，还需要有阳光、自由、和一点花的芬芳。——安徒生',
            '在最黑暗的那段人生，是我自己把自己拉出深渊。没有那个人，我就做那个人。——中岛美嘉',
            '且视他人之疑目如盏盏鬼火，大胆地去走你的夜路。——史铁生',
            '上人生的旅途罢，前途很远，也很暗。然而不要怕，不怕的人的面前才有路。——鲁迅',
            '所谓自由，不是随心所欲，而是自我主宰。——康德',
            '一个人知道自己为什么而活，就可以忍受任何一种生活。——尼采',
            '在隆冬，我终于知道，在我身上有一个不可战胜的夏天。——阿尔贝·加缪',
            '种一棵树最好的时间是十年前，其次是现在。——丹比萨·莫约',
        ]
        self.addSubInterface(QLabel(random.choice(textPool)), text, text, FIF.UP)
        self.tabCount += 1

    def removeTab(self, index):
        item = self.tabBar.tabItem(index)
        widget = self.findChild(QLabel, item.routeKey())

        self.stackedWidget.removeWidget(widget)
        self.tabBar.removeTab(index)

    def addExistCateTab(self):
        if self.existCateCheckBox.isChecked():
            self.drawExistCate = pg.PlotWidget(self)
            h = category(cfg.videoTitleFiles.value[0])
            barItem = pg.BarGraphItem(x=range(len(VIDEO_TYPE)),height=h, width = 0.5, brush=(0, 159, 170),pen=None)
            self.drawExistCate.addItem(barItem)
            self.addSubInterface(self.drawExistCate, 'existCate', '按已有类别', FIF.PENCIL_INK)
            detailInfo = []
            for i in range(len(h)):
                detailInfo.append([str(i),VIDEO_TYPE[i],str(h[i])])
            self.detailSignal.emit(detailInfo)
        else:
            self.tabBar.removeTabByKey('existCate')
    
    def addUserActionCateTab(self):
        if self.userActionCateCheckBox.isChecked():
            self.drawUserActionCluster = pg.PlotWidget(self)
            ratings_matrix = load_data(matrix_kind=1)
            x, h = userActionCluster(ratings_matrix)
            barItem = pg.BarGraphItem(x=x, height=h,width = 0.5, brush=(0, 159, 170),pen=None)
            self.drawUserActionCluster.addItem(barItem)
            self.addSubInterface(self.drawUserActionCluster, 'userActionCate', '按相似用户群体', FIF.PENCIL_INK)
            detailInfo = []
            for i in range(len(x)):
                detailInfo.append([str(x[i]),f'第{i}类',str(h[i])])
            self.detailSignal.emit(detailInfo)
        else:
            self.tabBar.removeTabByKey('userActionCate')