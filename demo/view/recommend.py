import os
import csv
import sys

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter,QColor
from PyQt6.QtWidgets import QWidget,QFileDialog

from qfluentwidgets import FluentIcon as FI
from .Ui_recommend import Ui_recommend

from operations.user_video_rating import user_video_rating  #模拟生成评分矩阵
from operations.load_data import load_data  #加载评分矩阵
from operations.CF_user import CF_user
from operations.find_video_title import find_video_title
from operations.CF_MF import BiasSVD
from settings import WORKING_PATH, DATA_PATH

class Recommend(QWidget, Ui_recommend):
  def __init__(self, parent=None):
    super().__init__(parent=parent)
    self.setupUi(self)

    #设置流畅图标
    self.pushButton_video_file.setIcon(FI.FOLDER)
    self.pushButton_rec_uid.setIcon(FI.ACCEPT)
    self.pushButton_user_num.setIcon(FI.ACCEPT)
    self.pushButton_video_num.setIcon(FI.ACCEPT)
    #设置部件属性
    #self.textEdit_rec_res.setEnabled(False) #设置文本框不可编辑
    #信号槽连接
    self.pushButton_video_file.clicked.connect(self.open_video_file) #获取视频标题csv文件
    self.pushButton_user_num.clicked.connect(self.simulate_user) #模拟生成用户
    self.pushButton_video_num.clicked.connect(self.simulate_rating) #模拟生成评分矩阵
    self.pushButton_rec_uid.clicked.connect(self.rec_to_uid) #推荐视频给某位用户
  
  #选择视频标题文件，获取视频个数
  def open_video_file(self):
    home_dir = str()
    fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir)
    self.video_title_path = fname[0]
    num_lines = 0

    with open(self.video_title_path, 'r', newline='', encoding='utf-8') as file:
      csv_reader = csv.reader(file)
      for _ in csv_reader:
        num_lines += 1

    self.num_video = num_lines
    print('video.csv行数: ', num_lines)
  
  #获取生成用户的数量
  def simulate_user(self):
    text = self.lineEdit_user_num.text()
    try:
      self.num_user = int(text)
      #print(self.user_num)
      print("生成用户数：", self.num_user)
    except:
      print("不合法输入！")


  def simulate_rating(self):
    text = self.lineEdit_video_num.text()
    try:
      num_watch = int(text)
      if hasattr(self, 'num_user'):
        print("即将生成用户评分矩阵")
        user_video_rating(self.num_user, self.num_video, num_watch)
        print("生成完毕")
      else:
        print("未输入生成用户数！")
    except:
      print("不合法输入！")
  
  def rec_to_uid(self):
    text = self.lineEdit_rec_uid.text()
    try:
      rec_uid = int(text)
    except:
      print("不合法输入！")
      return
    #基于(用户)的评分矩阵
    ratings_matrix = load_data() #加载评分矩阵
    cf_user = CF_user(ratings_matrix,rec_uid)
    cf_user.compute_person_similarity() #计算相似度矩阵
    res = cf_user.top_k_rs_result()
    #从标题文件中找出标题
    if not hasattr(self, "video_title_path"):
      self.video_title_path = os.path.join(WORKING_PATH, "../source/videos.csv")
      #self.video_title_path = WORKING_PATH + "/../source/videos.csv"
    rec_str = find_video_title(self.video_title_path, res)
    self.textEdit_rec_res.setMarkdown(rec_str)
    # try:
    #   with open(self.video_title_path, newline="", encoding="utf-8-sig") as file:
    #     reader = csv.reader(file)
    #     for index,row in enumerate(reader):
    #       if index in res:
    #         rec_str += f"vid-{index}:{row[1]} \n\n"

    #   self.textEdit_rec_res.setMarkdown(rec_str)
    # except:
    #   print("寻找视频标题目录失败")
    #   self.textEdit_rec_res.setMarkdown("### 推荐结果:\n\n"+str(res))

