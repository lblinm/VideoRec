import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from collections import Counter

def userCluster(ratings_matrix:pd.DataFrame):
  '''
  params: 评分矩阵
  return:
  1. 聚类的类别
  2. 每类别数量
  3. 以改类别数聚类的轮廓系数
  '''
  # 每视频平均分
  video_avg_ratings = np.mean(ratings_matrix, axis=0)

  # 找出每视频喜爱的人群
  mask = ratings_matrix > video_avg_ratings
  sequence = [mask[column_label].index[mask[column_label]].tolist() for column_label in mask]

  # 通过Word2Vec模型得出用户特征向量
  model = Word2Vec(sentences=sequence, vector_size=100, window=5, min_count=1, sg=1)
  user_feature_vector = [model.wv[uid].tolist() for uid in model.wv.index_to_key]

  # 选择最好的聚类K值
  silhouette_scores = []
  possible_clusters = range(2, 20)

  for n_cluster in possible_clusters:
    kmeans = KMeans(n_clusters=n_cluster, n_init=10)
    cluster_labels = kmeans.fit_predict(user_feature_vector)
    silhouette_avg = silhouette_score(user_feature_vector, cluster_labels)
    silhouette_scores.append(silhouette_avg)
  
  best_n_clusters = possible_clusters[silhouette_scores.index(max(silhouette_scores))]
  
  # 聚类
  kmeans = KMeans(n_clusters=best_n_clusters, n_init=10)
  
  cluster_labels = kmeans.fit_predict(user_feature_vector)
  cluster_counts = Counter(cluster_labels)
  sorted_cluster_counts = dict(sorted(cluster_counts.items()))

  return list(sorted_cluster_counts.keys()), list(sorted_cluster_counts.values()), silhouette_scores[best_n_clusters]