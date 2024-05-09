import pandas as pd 

def category(titles_path):
  titles = pd.read_csv(titles_path, usecols=['vid','tag'])
  tag_count = titles.groupby('tag').size()
  y = tag_count.values.tolist()
  return y