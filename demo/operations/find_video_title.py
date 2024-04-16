import csv

def find_video_title(video_title_path, rec_res):
  rec_str = "### 推荐结果:\n\n"
  try:
    with open(video_title_path, newline="", encoding="utf-8-sig") as file:
      reader = csv.reader(file)
      for index,row in enumerate(reader):
        if index in rec_res:
          rec_str += f"vid-{index}:{row[1]} \n\n"
    return rec_str
  except:
    print("寻找视频标题目录失败")
    return str(rec_res)