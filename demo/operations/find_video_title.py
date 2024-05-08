import csv
import pandas as pd
def find_video_title(video_title_path, rec_res):
  res = []
  try:
    titles = pd.read_csv(video_title_path, usecols=['title'])
    for rec_vid in rec_res:
      res.append([str(rec_vid), titles.iat[rec_vid,0]])
    # with open(video_title_path, newline="", encoding="utf-8-sig") as file:
    #   reader = csv.reader(file)
    #   for index,row in enumerate(reader):
    #     if index in rec_res:
    #       res.append([str(index), row[1]])
    return res
  except:
    print("寻找视频标题目录失败")
    return str(rec_res)