import os
import pandas as pd
import sys
from settings import DATA_PATH

CACHE_DIR = DATA_PATH
#相似度计算
class CF_user():
		def __init__(self, rating_matrix, rec_id,based="user", top_n=5):
			self.rating_matrix = rating_matrix
			self.based = based
			self.rec_id = rec_id
			self.top_n = top_n

		def compute_person_similarity(self):
			'''
			计算皮尔逊相关系数
			params:
			return: 相似度矩阵
			'''
			user_similarity_cache_path = os.path.join(CACHE_DIR, "user_similarity.cache")
			item_similarity_cache_path = os.path.join(CACHE_DIR, "item_similarity.cache")

			#基于皮尔逊相关系数计算相似度
			if self.based == "user":
				if os.path.exists(user_similarity_cache_path):
					print("正从缓存加载用户相似度矩阵")
					self.user_similarity = pd.read_pickle(user_similarity_cache_path)
				else:
					print("开始计算用户相似度矩阵")
					self.user_similarity = self.rating_matrix.T.corr() #转置后运算
					self.user_similarity.to_pickle(user_similarity_cache_path)
			elif self.based == "item":
				if os.path.exists(item_similarity_cache_path):
					print("正从缓存加载物品相似度矩阵")
					self.item_similarity = pd.read_pickle(item_similarity_cache_path)
				else:
					print("开始计算物品相似度矩阵")
					self.item_similarity = self.rating_matrix.corr()
					self.item_similarity.to_pickle(item_similarity_cache_path)
			else:
				raise Exception("Unhandle 'based' Value: %s"%self.based)
			print("相似度矩阵计算/加载完毕")

		#基于用户相似度的评分预测
		def predict_user(self):
			'''
			预测给定用户对所有物品的评分值
			params:
			return: 预测的评分值
				'''
			#print("开始预测用户<%d>对物品<%d>的评分..."%(uid, iid))

			# 1-找出uid用户的相似用户
			similar_users = self.user_similarity[self.rec_id].drop([self.rec_id]).dropna()
			# 相似用户筛选原则：正相关的用户
			similar_users = similar_users.where(similar_users>0).dropna()
			if similar_users.empty is True:
				raise Exception("用户<%d>没有相似的用户！"%self.rec_id)
			# 2-从uid用户的近邻相似用户中筛选出对iid物品有评分记录的近邻用户
			item_ids = self.rating_matrix.columns
			for iid in item_ids:
				ids = set(self.rating_matrix[iid].dropna().index)&set(similar_users.index)
				finally_similar_users = similar_users.loc[list(ids)] 
				# 3-结合uid用户与其近邻用户的相似度预测uid用户对iid物品的评分
				sum_up = 0 #评分预测公式的分子
				sum_down = 0 #评分预测公式的分母
				for sim_uid, similarity in finally_similar_users.items():
					# 近邻用户的评分数据
					sim_user_rated_movies = self.rating_matrix.loc[sim_uid].dropna()
					# 近邻用户对iid物品的评分
					sim_user_rating_for_item = sim_user_rated_movies[iid]
					# 计算分子
					sum_up += similarity * sim_user_rating_for_item
					# 计算分母
					sum_down += similarity
				#计算预测的评分值并返回，此处改动，当sum_down为0时predict_rating=0
				if sum_down != 0:
					predict_rating = sum_up / sum_down
					yield iid, round(predict_rating, 2)
		#基于物品相似度的评分预测
					
		# 根据预测评分为指定用户进行top—N推荐
		def top_k_rs_result(self):
			'''
			为指定用户进行top-n推荐
			return: 对某用户的推荐结果，形式是二元组(int,float)的列表
			'''
			if self.based == "user":
				pre_all = self.predict_user()
			res = sorted(pre_all, key=lambda x: x[1], reverse=True)[:self.top_n]
			print("对用户<%d>推荐的vid: "%(self.rec_id), res)
			res_id = []
			for item in res:
				res_id.append(item[0])
			return res_id

						