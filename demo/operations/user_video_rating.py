import random
import csv
import pandas as pd
import os
from settings import DATA_PATH

def user_video_rating(user_num, video_num, watch_per):
  ratings = pd.DataFrame()
  for uid in range(user_num):
    for per in range(watch_per):
      #ratings.append([uid, random.randint(0,video_num-1),random.randint(0,9)])
      new_row = {'uid':uid, 'vid':random.randint(0,video_num-1), 'rating':random.randint(0,9)}
      ratings.append(new_row, ignore_index=False)
      
  ratings_cache_path = os.path.join(DATA_PATH, 'ratings.cache')
  ratings.to_pickle(ratings_cache_path)
  # with open(csv_path, 'w', newline='') as file:
  #   writer = csv.writer(file)
  #   writer.writerow(['uid','vid','rating'])
  #   for row in ratings:
  #     writer.writerow(row)