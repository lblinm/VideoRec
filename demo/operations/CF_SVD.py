import pandas as pd
import numpy as np
import os
import math as mt 
import time
from scipy.sparse.linalg import *
from scipy.sparse.linalg import svds
from scipy.sparse import csc_matrix, coo_matrix, save_npz, load_npz

class SVD():
  def __init__(self, ratings_matrix,rec_uid, top_k, F=50):
    self.rec_uid = rec_uid
    self.top_k = top_k
    self.F =F
    self.data_sparse = ratings_matrix
    self.userNum = self.data_sparse.shape[0]
    self.itemNum = self.data_sparse.shape[1]
    self.st_time = time.time()

  def compute_svd(self):
    DATA_PATH = os.environ.get('DATA_PATH')
    SVD_U_path = DATA_PATH + '\\SVD_U.npz'
    SVD_R_path = DATA_PATH + '\\SVD_R.npz'
    if os.path.exists(SVD_U_path):
      print("正在加载隐向量")
      self.U = load_npz(SVD_U_path)
      self.R = load_npz(SVD_R_path)
      print("加载隐向量完毕")
      return
    
    print("正在计算隐向量")
    U, s, V = svds(self.data_sparse, self.F)
    print('U-shape', U.shape)
    print('s-shape', s.shape)
    print('V-shape', V.shape)

    # 将S转换成对角阵的格式
    dim = (len(s),len(s))
    S = np.zeros(dim, dtype=np.float32)
    for i in range(0,len(s)):  
      S[i,i] = np.sqrt(s[i])
    
    # 都转成稀疏矩阵
    self.U = csc_matrix(U, dtype = np.float32)
    self.R = csc_matrix(S, dtype = np.float32) * csc_matrix(V, dtype = np.float32)

    # 存入本地文件
    save_npz(SVD_U_path, self.U)
    save_npz(SVD_R_path, self.R)
    print("计算隐向量完毕")
    
    
  def predict_rating(self):
    '''
    return: 1. 推荐结果（视频id）；2. 推荐结果指标
    '''
    prod = self.U[self.rec_uid,:] * self.R
    prod_dense = prod.todense().A.flatten()
    sorted_indices = np.argsort(-prod_dense)
    res_list = list(zip(sorted_indices[:self.top_k], prod_dense[sorted_indices][:self.top_k]))

    # print("推荐结果:",res_list)
    
    rec_id = []
    for item in res_list:
      rec_id.append(item[0])
    end_time = time.time()
    
    # 指标
    # 耗时
    t = round(end_time - self.st_time, 6)
    indicators = {'time':t}
    return rec_id, indicators
