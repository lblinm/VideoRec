import random
import csv

def user_video_rating(user_num, video_num, watch_per, data_path):
  ratings = []
  for uid in range(user_num):
    for vid in range(watch_per):
      ratings.append([uid, random.randint(0,video_num-1),random.randint(0,9)])

  csv_path = data_path+'/ratings.csv'
  with open(csv_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['uid','vid','rating'])
    for row in ratings:
      writer.writerow(row)