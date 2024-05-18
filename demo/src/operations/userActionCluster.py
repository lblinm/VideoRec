import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from collections import Counter

def userActionCluster(ratings_matrix:pd.DataFrame):
  '''
  params: 评分矩阵
  return:
  1. 聚类的类别
  2. 每类别数量
  3. 以改类别数聚类的轮廓系数
  '''
  # 找到每用户打分平均分以上的视频
  user_avg_ratings = np.mean(ratings_matrix, axis=1)
  sequences = []
  for index, row in ratings_matrix.iterrows():
    sequences.append(row[ row > user_avg_ratings[index] ].index.tolist())
  
  # 训练Word2Vec模型
  model = Word2Vec(sentences=sequences, vector_size=100, window=5, min_count=1, sg=1)

  # 获取视频特征向量
  video_feature_vector = []
  for vid in model.wv.index_to_key:
    video_feature_vector.append(model.wv[vid].tolist())

  # 选择最好的聚类K值
  # silhouette_scores = []
  # possible_clusters = range(10, 20)
  
  # for n_cluster in possible_clusters:
  #   kmeans = KMeans(n_clusters=n_cluster, n_init=10)
  #   cluster_labels = kmeans.fit_predict(video_feature_vector)
  #   silhouette_avg = silhouette_score(video_feature_vector, cluster_labels)
  #   silhouette_scores.append(silhouette_avg)

  # best_n_clusters = possible_clusters[silhouette_scores.index(max(silhouette_scores))]
  # print('best:', best_n_clusters)
  best_n_clusters = 20
  # 使用kmeans聚类
  kmeans = KMeans(n_clusters=best_n_clusters, n_init=10)

  cluster_labels = kmeans.fit_predict(video_feature_vector)
  silhouette = silhouette_score(video_feature_vector, cluster_labels)

  # 计算每个类别的数量
  cluster_counts = Counter(cluster_labels)
  sorted_cluster_counts = dict(sorted(cluster_counts.items()))
  return list(sorted_cluster_counts.keys()), list(sorted_cluster_counts.values()), silhouette #silhouette_scores[best_n_clusters]
  