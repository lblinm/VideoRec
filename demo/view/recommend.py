import os
import csv
import sys

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter,QColor
from PyQt6.QtWidgets import QWidget,QFileDialog

from qfluentwidgets import FluentIcon as FI
from .Ui_recommend import Ui_recommend

from operations.user_video_rating import user_video_rating  #模拟生成评分矩阵
#from ..operation.xx 导入错误 - 不允许顶层包相对导入？
from operations.load_data import load_data  #加载评分矩阵
from operations.CF_user import *

WORKING_PATH = os.path.dirname(sys.argv[0])
DATA_PATH = WORKING_PATH+"/data"

class Recommend(QWidget, Ui_recommend):
  def __init__(self, parent=None):
    super().__init__(parent=parent)
    self.setupUi(self)

    #设置流畅图标
    self.pushButton_video_file.setIcon(FI.FOLDER)
    self.pushButton_rec_uid.setIcon(FI.ACCEPT)
    self.pushButton_user_num.setIcon(FI.ACCEPT)
    self.pushButton_video_num.setIcon(FI.ACCEPT)
    #信号槽连接
    self.pushButton_video_file.clicked.connect(self.open_video_file) #获取视频标题csv文件
    self.pushButton_user_num.clicked.connect(self.simulate_user) #模拟生成用户
    self.pushButton_video_num.clicked.connect(self.simulate_rating) #模拟生成评分矩阵
    self.pushButton_rec_uid.clicked.connect(self.rec_to_uid) #推荐视频给某位用户
  
  #选择视频标题文件，获取视频个数
  def open_video_file(self):
    home_dir = str()
    fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir)
    file_path = fname[0]
    num_lines = 0

    with open(file_path, 'r', newline='', encoding='utf-8') as file:
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
        user_video_rating(self.num_user, self.num_video, num_watch, DATA_PATH)
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
    ratings_matrix = load_data(DATA_PATH) #加载评分矩阵
    similarity = compute_person_similarity(ratings_matrix) #计算/加载相似度矩阵
    #predict(rec_uid, 100, ratings_matrix, similarity) #预测uid对vid的评分
    rec_res = top_k_rs_result(rec_uid, ratings_matrix, similarity, 5)
    
    rec_tabel = []
    for item in rec_res:
      rec_tabel.append(item[1])
    text = self.label_rec_result.text()
    cut_index = text.find('：')
    text = text[:cut_index+1]
    rec_text = text + str(rec_tabel)
    self.label_rec_result.setText(rec_text)


