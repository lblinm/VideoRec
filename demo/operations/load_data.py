import pandas as pd
import numpy as np
import os
from scipy.sparse import coo_matrix, save_npz, load_npz
def load_data():
	'''
	加载数据为稀疏矩阵
	'''
	DATA_PATH = os.environ.get('DATA_PATH')
	ratings_path = DATA_PATH + '\\ratings.csv'
	cache_path = DATA_PATH + '\\ratings.cache'
	print("开始加载数据集...")
	if os.path.exists(cache_path):
		data_sparse = load_npz(data_sparse)
	else:
		dtype = {"uid": np.int32, "vid": np.int32, "rating": np.float64}
		ratings = pd.read_csv(ratings_path,dtype=dtype, usecols=range(3))

		data_array = ratings['rating']
		row_array = ratings['uid']
		col_array = ratings['vid']
		data_sparse = coo_matrix((data_array, (row_array, col_array)),dtype=np.float64)
		save_npz(cache_path, data_sparse)
	return data_sparse


	# if os.path.exists(cache_path):
	#     print("加载缓存中...")
	#     ratings_matrix = pd.read_pickle(cache_path)
	#     print("从缓存加载数据集完毕")
	# else:
	#     print("加载数据中...")
	#     dtype = {"uid": np.int32, "vid": np.int32, "rating": np.float64}
	#     ratings = pd.read_csv(ratings_path, dtype=dtype, usecols=range(3))
	#     ratings_matrix = ratings.pivot_table(index=["uid"], columns=["vid"],values="rating")
	#     # ratings_matrix.columns = ['uid', 'vid', 'rating']
	#     print(ratings_matrix)
	#     ratings_matrix.to_pickle(cache_path)
	#     print("数据集加载完毕")
	# return ratings_matrix
