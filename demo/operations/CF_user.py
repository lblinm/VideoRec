import os
import pandas as pd
import sys

CACHE_DIR = os.path.dirname(sys.argv[0]) + "/data"
#相似度计算
def compute_person_similarity(ratings_matrix, based="user"):
    '''
    计算皮尔逊相关系数
    params:
    ratings_matrix: 用户-评分矩阵
    based: user or item
    return: 相似度矩阵
    '''
    user_similarity_cache_path = os.path.join(CACHE_DIR, "user_similarity.cache")
    item_similarity_cache_path = os.path.join(CACHE_DIR, "item_similarity.cache")
    #基于皮尔逊相关系数计算相似度
    if based == "user":
        if os.path.exists(user_similarity_cache_path):
            print("正从缓存加载物品相似度矩阵")
            similarity = pd.read_pickle(user_similarity_cache_path)
        else:
            print("开始计算物品相似度矩阵")
            similarity = ratings_matrix.T.corr()
            similarity.to_pickle(user_similarity_cache_path)
    elif based == "item":
        if os.path.exists(item_similarity_cache_path):
            print("正从缓存加载物品相似度矩阵")
            similarity = pd.read_pickle(item_similarity_cache_path)
        else:
            print("开始计算物品相似度矩阵")
            similarity = ratings_matrix.corr()
            similarity.to_pickle(item_similarity_cache_path)
    else:
        raise Exception("Unhandle 'based' Value: %s"%based)
    print("相似度矩阵计算/加载完毕")
    return similarity

#实现评分预测方法：predict
def predict(uid, iid, ratings_matrix, user_similar):
    '''
    预测给定用户对物品的评分值
    params:
        uid: 用户ID
        iid: 物品ID
        ratings_matrix: 用户-物品评分矩阵
        user_similar: 用户两两相似的矩阵
    return: 预测的评分值
    '''
    #print("开始预测用户<%d>对物品<%d>的评分..."%(uid, iid))

    # 1-找出uid用户的相似用户
    similar_users = user_similar[uid].drop([uid]).dropna()
    # 相似用户筛选原则：正相关的用户
    similar_users = similar_users.where(similar_users>0).dropna()
    if similar_users.empty is True:
        raise Exception("用户<%d>没有相似的用户！"%uid)
    # 2-从uid用户的近邻相似用户中筛选出对iid物品有评分记录的近邻用户
    ids = set(ratings_matrix[iid].dropna().index)&set(similar_users.index)
    finally_similar_users = similar_users.loc[list(ids)] 
    # 3-结合uid用户与其近邻用户的相似度预测uid用户对iid物品的评分
    sum_up = 0 #评分预测公式的分子
    sum_down = 0 #评分预测公式的分母
    for sim_uid, similarity in finally_similar_users.items():
        # 近邻用户的评分数据
        sim_user_rated_movies = ratings_matrix.loc[sim_uid].dropna()
        # 近邻用户对iid物品的评分
        sim_user_rating_for_item = sim_user_rated_movies[iid]
        # 计算分子
        sum_up += similarity * sim_user_rating_for_item
        # 计算分母
        sum_down += similarity
    #计算预测的评分值并返回，此处改动，当sum_down为0时predict_rating=0
    predict_rating = sum_up / sum_down if sum_down != 0 else 0
    
    #print("预测用户<%d>对物品<%d>的评分：%0.2f"%(uid,iid,predict_rating))
    
    return round(predict_rating, 2)

def predict_all(uid, ratings_matrix, user_similar):
    '''
    预测全部评分
    params:
        uid: 用户id
        ratings_matrix: 用户-物品打分矩阵
        user_similar: 用户两两间的相似度
    return: 生成器，逐个返回预测评分
    '''
    print("正在预测该用户对所有物品的评分")
    item_ids = ratings_matrix.columns
    for iid in item_ids:
        try:
            rating = predict(uid, iid, ratings_matrix, user_similar)
        except Exception as e:
            print(e)
        else:
            if rating != 0:
              yield uid, iid, rating

# 根据预测评分为指定用户进行top—N推荐
def top_k_rs_result(rec_id, ratings_matrix,user_similar, top_n):
    '''
    为指定用户进行top-n推荐
    params:
    rec_id: 用户id
    ratings_matrix: 评分矩阵
    user_similar: 相似度矩阵
    top_n: 推荐数量
    return: 对某用户的推荐结果，形式是三元组(int,int,float)的列表
    '''
    pre_all = predict_all(rec_id, ratings_matrix, user_similar)
    res = sorted(pre_all, key=lambda x: x[2], reverse=True)[:top_n]
    print("对用户<%d>推荐的vid: "%(rec_id), res)
    return res

        