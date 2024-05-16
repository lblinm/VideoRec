import sys
import os
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from qfluentwidgets import (
  FluentWindow, FluentIcon as FIF, setTheme,Theme,
    NavigationItemPosition,SplashScreen
)
#from view.recommend import Recommend
from view.recommend_interface import RecommendInterface
from view.cluster_interface import ClusterInterface
from view.predict_interface import PredictInterface

import utils.settings as settings

# 路径管理
WORKING_PATH = os.path.abspath(os.path.dirname(__file__))
os.environ['WORKING_PATH'] = WORKING_PATH
os.environ['IMAGE_PATH'] = WORKING_PATH + '\\resource\\image'
os.environ['QSS_PATH'] = WORKING_PATH + '\\resource\\qss'
os.environ['WORD_PATH'] = WORKING_PATH + '\\resource\\word'
os.environ['DATA_PATH'] = WORKING_PATH + '\\data'


class Demo(FluentWindow):
  
  def __init__(self):
    super().__init__()
    self.initWindow()
    
    #创建子界面
    self.recommendInterface = RecommendInterface(self)
    self.clusterInterface = ClusterInterface(self)
    self.predictInterface = PredictInterface(self)
    

    #主题
    self.current_theme = Theme.LIGHT

    #导航栏
    self.initNavigation()
    
    self.splashScreen.finish()

  def initWindow(self):
    self.resize(800, 600)
    self.setWindowTitle('短视频推荐分析模拟器')
    self.setWindowIcon(QIcon(os.environ.get('IMAGE_PATH')+'\\logo.png'))

    #创建初始页
    self.splashScreen = SplashScreen(self.windowIcon(), self)
    self.splashScreen.setIconSize(QSize(500, 500))
    self.splashScreen.raise_()

    desktop = QApplication.screens()[0].availableGeometry()
    w, h = desktop.width(), desktop.height()
    self.move(w//2 - self.width()//2, h//2 - self.height()//2)
    self.show()

    #处理事件队列中的所有待处理事件，以确保及时更新和响应用户界面
    QApplication.processEvents()
  
  def initNavigation(self):
    self.addSubInterface(self.recommendInterface, FIF.VIDEO, '视频推荐')
    
    pos = NavigationItemPosition.SCROLL
    self.addSubInterface(self.clusterInterface, FIF.IOT, '视频聚类',pos)
    self.addSubInterface(self.predictInterface, FIF.MARKET, '热度预测',pos)

    self.navigationInterface.addItem(
      routeKey='changeTheme',
      icon=FIF.CONSTRACT,
      text='主题切换',
      position=NavigationItemPosition.BOTTOM,
      onClick=self.changeTheme
    )

  def changeTheme(self):
    if(self.current_theme == Theme.LIGHT):
      self.current_theme = Theme.DARK
    else:
      self.current_theme = Theme.LIGHT
    setTheme(self.current_theme)
  
  # def createSubInterface(self):
  #   loop = QEventLoop(self)
  #   QTimer.singleShot(1500, loop.quit)
  #   loop.exec()


app = QApplication(sys.argv)
w = Demo()
w.show()
app.exec()