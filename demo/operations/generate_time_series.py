import os
import numpy as np
import pandas as pd
import csv
import time
from utils.settings import cfg

def generate_time_series(file_path):
  return
  start_time = time.time()
  videos = pd.read_csv(file_path, usecols=['vid','play'])
  # 模拟的天数
  days = 10
  simulate = []
  for i, row in videos.iterrows():
    # 最大播放量
    max_play = int(row['play'])
    # 增长速率
    k = np.random.uniform(0.01, 0.2)
    # 增长最快的时间点
    t_0 = np.random.randint(3,10)
    # 初始噪声的方差
    sigma_start = max_play * 0.005
    # 最终噪声的方差
    sigma_end = max_play * 0.0005
    # 时间范围
    t = np.arange(1, days + 1)
    # 计算每天的播放量增量
    delta_P = k * max_play * np.exp(-k * (t - t_0)) / (1 + np.exp(-k * (t - t_0)))**2
    # 计算随时间递减的方差
    # 这里使用递减的方式计算每天的方差
    sigma_t = sigma_start - (sigma_start - sigma_end) * (t - 1) / (days - 1)
    # 添加随时间递减的随机噪声
    delta_P_noisy = np.rint(delta_P + np.random.normal(0, sigma_t, size=delta_P.shape))
    # 确保增量不为负数
    delta_P_noisy[delta_P_noisy < 0] = 0
    
    simulate.append(delta_P_noisy)

  save_path = os.environ.get('DATA_PATH') + '\\time_series.csv'
  with open(save_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(simulate)
  
  end_time = time.time()
  print(f"生成时间序列数据集完成，耗时{round(end_time-start_time,2)}s")
  return save_path