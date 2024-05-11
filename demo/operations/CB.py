import os
import pandas as pd
import numpy as np
import pickle
import jieba, jieba.analyse, jieba.posseg as pseg
import time

def CB_video(titles_path, inverted_table_cache, words_cache_path):
  print("正在对视频标题进行关键词提取+建立视频画像倒排表...")
  st_time = time.time()
  titles = pd.read_csv(titles_path, usecols=['vid', 'title'])
  titles.set_index('vid', inplace=True, drop=True)

  wordmodel = jieba.analyse
  # 加停用词库
  stop_words_path = os.environ.get("WORD_PATH") + "\\CNstop_words_zh.txt"
  wordmodel.set_stop_words(stop_words_path=stop_words_path)
  
  # 加词频文件
  idf_path = os.environ.get("WORD_PATH") + "\\idf.txt.big"
  wordmodel.set_idf_path(idf_path=idf_path)

  words = []
  inverted_table = {}
  for row in titles.itertuples():
    words_per = wordmodel.extract_tags(row[1], 4, withWeight=True, allowPOS=['ns','n','vn','v','nr','x'])
    for word_info in words_per:
      word_videos = inverted_table.get(word_info[0], [])
      word_videos.append((row[0], word_info[1]))
      inverted_table.setdefault(word_info[0], word_videos)
    words.append(words_per)
  
  # 检查是否正确打开文件，并以二进制写入模式打开文件
  with open(inverted_table_cache, 'wb') as f:
    pickle.dump(inverted_table, f)
  with open(words_cache_path, 'wb') as file:  
    pickle.dump(words, file)

  end_time = time.time()
  print(f"关键词提取+倒排表建立完毕, 耗时{end_time-st_time}s")

def CB_user(ratings, users_profile_cache):
  print("正在提取用户喜爱的关键词，建立用户画像...")
  # 加载关键词列表
  words_cache_path = os.environ.get("DATA_PATH") + "\\word_cache.pkl"
  with open(words_cache_path, 'rb') as file:
    words = pickle.load(file)

  # 各用户平均分
  user_avg_ratings = np.mean(ratings, axis=1)

  # 用户画像建立: 最喜爱的关键词列表
  users_profile = []
  for uid, user_avg_rating in enumerate(user_avg_ratings):
    user_profile = {}
    for vid, rating in ratings.iloc[uid].items():
      if rating > user_avg_rating:
        for tag, weight in words[vid]:
          if tag in user_profile.keys():
            user_profile[tag] += weight
          else:
            user_profile[tag] = weight
    user_profile = sorted(user_profile.items(), key=lambda x:x[1], reverse=True)[:30]
    users_profile.append(user_profile)

  with open(users_profile_cache, 'wb') as file:
    pickle.dump(users_profile, file)
  print("用户画像创建完毕")

def CB_recommend(titles_path,ratings, rec_uid, top_k):
  # 缓存文件路径
  words_cache_path = os.environ.get("DATA_PATH") + "\\word_cache.pkl"
  inverted_table_cache = os.environ.get("DATA_PATH") + "\\reverted_table_cache.pkl"
  users_profile_cache = os.environ.get("DATA_PATH") + "\\users_profile_cache.pkl"

  # 加载数据
  users_profile = None
  inverted_table = None
  if not os.path.exists(words_cache_path) or not os.path.exists(inverted_table_cache):
    CB_video(titles_path, words_cache_path, inverted_table_cache)
  else:
    with open(words_cache_path, 'rb') as f1:
      words = pickle.load(f1)
    with open(inverted_table_cache, 'rb') as f2:
      inverted_table = pickle.load(f2)

  if not os.path.exists(users_profile_cache):
    CB_user(ratings, users_profile_cache)
  else:
    with open(users_profile_cache, 'rb') as f3:
      users_profile = pickle.load(f3)

  # 根据用户喜欢的关键词推荐对应视频
  candidate = {}
  for tag, weight_user in users_profile[rec_uid]:
    for vid, weight_video in inverted_table[tag]:
      if vid in candidate.keys():
        candidate[vid] += weight_user * weight_video
      else:
        candidate[vid] = weight_user * weight_video
  # 用户评分过的视频
  # watched_videos = ratings.columns[ratings.iloc[rec_uid].notna()]
  # candidate = sorted(candidate.items(), key=lambda x:x[1], reverse=True)
  # candidate_filter = [(vid, weight) for vid, weight in candidate if vid not in watched_videos][:top_k]

  candidate = sorted(candidate.items(), key=lambda x: x[1], reverse=True)[:100]
  print("推荐结果：", candidate)
  rec_id = []
  for item in candidate:
    rec_id.append(item[0])
  return rec_id
  
