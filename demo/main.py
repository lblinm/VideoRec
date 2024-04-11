import sys
import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import (
  SplitFluentWindow, FluentIcon, setTheme,Theme,NavigationAvatarWidget, NavigationItemPosition
)
from view.recommend import Recommend


class Demo(SplitFluentWindow):
  
  def __init__(self):
    super().__init__()
    self.setWindowTitle('短视频推荐分析模拟器')
    
    #创建子界面
    self.Recommend = Recommend(self)
    self.addSubInterface(self.Recommend, FluentIcon.VIDEO, '短视频推荐')

    #主题
    self.current_theme = Theme.LIGHT

    #其它导航项
    self.navigationInterface.addItem(
      routeKey='changeTheme',
      icon=FluentIcon.CONSTRACT,
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

if __name__ == "__main__":
  QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
  app = QApplication(sys.argv)
  w = Demo()
  w.show()
  app.exec()