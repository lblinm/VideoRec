import random
import math
import os
import pickle
from settings import DATA_PATH

class BiasSVD():
  def __init__(self, rating_matrix,rec_uid, F=5, alpha=0.1, lmbda=0.1, max_iter=100, top_n=5):
    self.rating_matrix = rating_matrix  # 评分矩阵
    self.rec_uid = rec_uid
    self.F = F          # 这个表示隐向量的维度
    self.alpha = alpha  # 学习率
    self.lmbda = lmbda  # 正则项系数
    self.max_iter = max_iter        # 最大迭代次数
    self.top_n = top_n

    user_num = self.rating_matrix.shape[0]
    item_num = self.rating_matrix.shape[1]
    #初始化隐向量
    self.P = [[random.random() / math.sqrt(F) for _ in range(F)] for _ in range(user_num)]
    self.Q = [[random.random() / math.sqrt(F) for _ in range(F)] for _ in range(item_num)]
    #初始化偏置值
    self.bu = [0 for _ in range(user_num)]
    self.bi = [0 for _ in range(item_num)]

    #求评分平均值,作为全局偏置系数
    self.mu = self.rating_matrix.mean()

  def train(self):
    P_cache_path = os.path.join(DATA_PATH, "MF_P.pkl")
    Q_cache_path = os.path.join(DATA_PATH, "MF_Q.pkl")
    bu_cache_path = os.path.join(DATA_PATH, "MF_bu.pkl")
    bi_cache_path = os.path.join(DATA_PATH, "MF_bi.pkl")
    if os.path.exists(P_cache_path):
      self.P = pickle.load(P_cache_path)
      self.Q = pickle.load(Q_cache_path)
      self.bu = pickle.load(bu_cache_path)
      self.bi = pickle.load(bi_cache_path)
    if os.path.exists(P_cache_path):
      print("正在从缓存加载用户隐向量")
      self.P = pd.read_pickle(P_cache_path)
      if os.path.exists(Q_cache_path):
        print("正在从缓存加载物品隐向量")
        self.P = pd.read_pickle(Q_cache_path)
        if os.path.exists(P_cache_path):
          print("正在从缓存加载用户偏置系数")
          self.P = pd.read_pickle(bu_cache_path)
          if os.path.exists(P_cache_path):
            print("正在从缓存加载用户偏置系数")
            self.P = pd.read_pickle(bi_cache_path)
            return
    print("正在训练生成用户、物品隐向量...")
    for step in range(self.max_iter):
      for user, row in self.rating_matrix.iterrows():
        for item, rui in row.iteritems():
          rhat_ui = self.predict(user, item)
          e_ui = rui - rhat_ui

          self.bu[user] += self.alpha*(e_ui-self.lmbda*self.bu[user])
          self.bi[item] += self.alpha*(e_ui-self.lmbda*self.bi[item])

          for k in range(self.F):
            self.P[user][k] += self.alpha*(e_ui*self.Q[item][k]-self.lmbda*self.P[user])
            self.Q[item][k] += self.alpha*(e_ui*self.P[user][k]-self.lmbda*self.Q[item])
      self.alpha *= 0.1
      
  #user对item的评分：P[user][]@Q[item][].T+bu[user]+bi[item]+mu
  def predict(self, user, item):
    return sum(self.P[user][f] * self.Q[item][f] for f in range(self.F)) + self.bu[user] + self.bi[item] + self.mu

  def predict_all(self):
    rec_res = []
    item_ids = self.rating_matrix.columns
    for item in item_ids:
      predict_rating = self.predict(self.rec_uid, item)
      if predict_rating != 0:
        rec_res.append((item, predict_rating))
    res = sorted(rec_res, key=lambda x: x[1], reverse=True)[:self.top_n]
    print("对用户<%d>推荐的vid: "%(self.rec_uid), res)
    res_id = []
    for item in res:
      res_id.append(item[0])
    return res_id
