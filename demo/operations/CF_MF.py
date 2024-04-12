import random
import math


class BiasSVD():
  def __init__(self, rating_data, F=5, alpha=0.1, lmbda=0.1, max_iter=100):
    self.rating_data = rating_data  # 评分矩阵
    self.F = F          # 这个表示隐向量的维度
    self.alpha = alpha  # 学习率
    self.lmbda = lmbda  # 正则项系数
    self.max_iter = max_iter        # 最大迭代次数

    user_num = self.rating_data.shape[0]
    item_num = self.rating_data.shape[1]
    #初始化隐向量
    self.P = [[random.random() / math.sqrt(F) for _ in range(F)] for _ in range(user_num)]
    self.Q = [[random.random() / math.sqrt(F) for _ in range(F)] for _ in range(item_num)]
    #初始化偏置值
    self.bu = [0 for _ in range(user_num)]
    self.bi = [0 for _ in range(item_num)]

    #求评分平均值,作为全局偏置系数
    self.mu = self.rating_matrix.mean()

  def train(self):
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



