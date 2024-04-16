import os
import pandas as pd
import numpy as np
import os
from settings import DATA_PATH
def load_data():
    '''
    加载数据
    data_path: 数据集|cache路径
    return: 用户-评分矩阵
    '''
    ratings_path = os.path.join(DATA_PATH, "ratings.csv")
    # ratings_path = data_path + "/ratings.csv"
    cache_path = os.path.join(DATA_PATH, "ratings.cache")
    #cache_path = data_path + "/ratings_matrix.cache"
    #print("cache_path: ", cache_path)
    print("开始加载数据集...")
    if os.path.exists(cache_path):
        print("加载缓存中...")
        ratings_matrix = pd.read_pickle(cache_path)
        print("从缓存加载数据集完毕")
    else:
        print("加载数据中...")
        dtype = {"uid": np.int32, "vid": np.int32, "rating": np.int32}
        ratings = pd.read_csv(ratings_path, dtype=dtype, usecols=range(3))
        ratings_matrix = ratings.pivot_table(index=["uid"], columns=["vid"],values="rating")
        ratings_matrix.to_pickle(cache_path)
        print("数据集加载完毕")
    return ratings_matrix
