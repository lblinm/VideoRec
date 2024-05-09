import shutil
import pandas as pd

df=pd.read_csv('source/video_titles.csv',engine='python') # 读取csv文件
df = df.drop_duplicates(subset=['title'], keep='first', inplace=False) # 删除重复列
df['vid'] = range(1, len(df) + 1) # 重置序号列为连续的序号列
df.to_csv('source/video_titles.csv', index=False) # 保存为新的csv文件
