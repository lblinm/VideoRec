import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from sklearn.cluster import KMeans
from collections import Counter

def userActionCluster(ratings_matrix:pd.DataFrame):
  '''
  生成视频特征向量并聚类
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

  # 使用kmeans聚类
  kmeans = KMeans(n_clusters=40)
  cluster_labels = kmeans.fit_predict(video_feature_vector)

  # 计算每个类别的数量
  cluster_counts = Counter(cluster_labels)
  sorted_cluster_counts = dict(sorted(cluster_counts.items()))
  return list(sorted_cluster_counts.keys()), list(sorted_cluster_counts.values())
  