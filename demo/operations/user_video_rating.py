import random
import csv
import os


def user_video_rating(user_num, video_num, watch_per):
  DATA_PATH = os.environ.get('DATA_PATH')
  ratings = []
  for uid in range(user_num):
    for per in range(watch_per):
      #ratings.append([uid, random.randint(0,video_num-1),random.randint(0,9)])
      new_row = [uid,random.randint(0,video_num-1), random.uniform(0,1)]
      ratings.append(new_row)
      
  csv_path = DATA_PATH + '\\ratings.csv'
  with open(csv_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['uid','vid','rating'])
    for row in ratings:
      writer.writerow(row)