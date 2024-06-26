from qfluentwidgets import (TabBar,qrouter, FluentIcon as FIF, TableWidget,TextEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QLabel,QStackedWidget,QHeaderView,
                              QVBoxLayout, QLabel, QHBoxLayout, QFrame,
                              QTableWidgetItem)
from utils.style_sheet import StyleSheet
import pyqtgraph as pg
import random

class TabInterface(QWidget):
    """ Tab interface """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.tabCount = 1

        self.tabBar = TabBar(self)
        self.stackedWidget = QStackedWidget(self)
        self.tabView = QWidget(self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout(self.tabView)

        # 绘图
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        # add items to pivot
        self.__initWidget()

    def __initWidget(self):
        self.initLayout()

        self.tabBar.setScrollable(True)

        StyleSheet.TAB_INTERFACE.apply(self)

        self.connectSignalToSlot()

        # qrouter.setDefaultRouteKey(
        #     self.stackedWidget, self.songInterface.objectName())

    def connectSignalToSlot(self):
        self.tabBar.tabAddRequested.connect(self.addTab)
        self.tabBar.tabCloseRequested.connect(self.removeTab)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)

    def initLayout(self):
        self.tabBar.setTabMaximumWidth(250)

        self.setFixedHeight(280)
        self.hBoxLayout.addWidget(self.tabView, 1)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addWidget(self.tabBar)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

    def addSubInterface(self, widget, objectName, text, icon):
        widget.setObjectName(objectName)
        # widget.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.stackedWidget.addWidget(widget)
        self.tabBar.addTab(
            routeKey=objectName,
            text=text,
            icon=icon,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )
        self.tabCount += 1


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
            '工作不算争取价值，是劳动换取酬劳，工作的时候偷闲才是为自己争取价值。——青雀',
            '筑城者为我们砌成堡垒，使我们远离风雪，但我们必须铭记，风雪从未消失。——布洛妮娅',
        ]
        self.addSubInterface(QLabel(random.choice(textPool)), text, text, FIF.EXPRESSIVE_INPUT_ENTRY)

    def removeTab(self, index):
        item = self.tabBar.tabItem(index)
        widget = self.findChild(QLabel, item.routeKey())

        self.stackedWidget.removeWidget(widget)
        self.tabBar.removeTab(index)

    
    def addDrawRes(self,kind: int, x:list, y:list, tabTitle:str, detail:str = '', noLabel=False, x1:list=None, y1:list=None): #, x1:list=None, y1:list=None
        '''
        添加图标签页
        parmas: kind=0或1, 0代表柱形图，1代表折线图
        x: x轴
        y: y轴
        tabTitle: 标签页头文本
        detail: (None)在旁边显示的详细信息，以markdown形式
        '''
        widget = QWidget()
        hBoxLayout = QHBoxLayout(widget)
        
        # 图表
        drawRes = pg.PlotWidget()
        name = f'drawRes{self.tabCount}'
        if kind == 0:
            # 添加柱形
            barItem = pg.BarGraphItem(x=x, height=y, width=0.5, brush=(0, 159, 170),pen=None)
            drawRes.addItem(barItem)
        elif kind == 1:
            drawRes.plot(x, y, pen=(0, 159, 170))  #symbolBrush=(0, 159, 170)
            if x1 is not None:
                drawRes.plot(x1, y1, pen=(242,149,0))
        # 添加数据标签
        if not noLabel:
            for i in range(len(x)):
                label = pg.TextItem(text=str(y[i]))
                label.setAnchor((0.5,1))
                label.setPos(x[i], y[i])
                drawRes.addItem(label)
        

        hBoxLayout.addWidget(drawRes, 0)

        # 文本
        if detail != '':
            textEdit = TextEdit()
            textEdit.setMarkdown(detail)
            textEdit.setFixedWidth(250)
            hBoxLayout.addWidget(textEdit, 0, Qt.AlignmentFlag.AlignRight)
        # 增加标签页
        self.addSubInterface(widget, name, f'{tabTitle}({self.tabCount})', FIF.PENCIL_INK)

    def addTableRes(self, title:list, data:list, tabTitle:str, detail:str = ''):
        widget = QWidget()
        hBoxLayout = QHBoxLayout(widget)
        tableView = TableWidget()

        # 表格
        tableView.setBorderRadius(8)
        tableView.setWordWrap(False)
        tableView.verticalHeader().show()

        tableView.adjustSize()
        tableView.setObjectName("tableView")

        tableView.setRowCount(len(data))
        row_count = len(data[0]) if len(data) > 0 else 0
        tableView.setColumnCount(row_count)

        tableView.setHorizontalHeaderLabels(title)
        for i in range(len(data)):
            for j in range(row_count):
                item = QTableWidgetItem(data[i][j])
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                tableView.setItem(i, j, item)

        tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)

        hBoxLayout.addWidget(tableView, 1)
        name = f'tableRes{self.tabCount}'
        
        # 文本
        if detail != '':
            textEdit = TextEdit()
            textEdit.setMarkdown(detail)
            textEdit.setFixedWidth(250)
            hBoxLayout.addWidget(textEdit, 0, Qt.AlignmentFlag.AlignRight)

        self.addSubInterface(widget, name, f'{tabTitle}({self.tabCount})', FIF.LAYOUT)

