# 结构

1. `demo`: 项目文件夹
2. `source`: 存储开发相关文件，包括视频数据集、爬虫脚本等

# 运行

1. 确保具有环境：`python >= 3.7 (perfect 3.9/3.10)`
2. 安装依赖：`pip install -r demo/requirements.txt`
3. 运行`main.py`文件：`python demo/main.py`

> release 发行版: 下载解压后双击`VideoTool.exe`

# 功能

1. 模拟用户行为，生成评分矩阵
2. SVD、Content Based、Item based CF 等多种推荐算法
3. 视频聚类
4. 用户聚类
5. 模拟视频历史播放量
6. 预测视频未来播放量

# 详细目录结构

demo 的目录结构

```shell
demo
│  config.json                            # 设置文件
│  pyproject.json                         # 打包配置文件
│  README.md
│  requirements.txt                       # 项目依赖
│
├─assets                                  # 静态资源
│  ├─image
│  │      logo.png                        # logo图片
│  │
│  ├─qss                                  # qss文件
│  │  ├─dark                              # 深色主题qss
│  │  │      recommend_interface.qss      # 推荐页qss
│  │  │      tab_interface.qss            # 标签组件qss
│  │  │
│  │  └─light                             # 浅色主题qss
│  │          recommend_interface.qss     # 推荐页qss
│  │          tab_interface.qss           # 标签页qss
│  │
│  └─word                                 # 文本文件
│          CNstop_words_zh.txt            # 停用词文件
│          idf.txt.big                    # 词频文件
│
├─data                                    # 数据存储
│      ratings.csv                        # 评分矩阵
│      ratings.npz                        # 评分矩阵(稀疏矩阵)缓存文件
│      ratings.pkl                        # 评分矩阵(dataframe)缓存文件
│      reverted_table_cache.pkl           # 关键词-视频倒排表（视频画像）
│      SVD_R.npz                          # 视频隐向量
│      SVD_U.npz                          # 用户隐向量
│      time_series.csv                    # 历史播放量数据集
│      users_profile_cache.pkl            # 关键词-用户倒排表（用户画像）
│      user_preference_matrix.csv         # 用户偏好矩阵
│      user_similarity.cache              # 用户相似度矩阵
│      word_cache.pkl                     # 特征向量缓存文件
│
├─docs                                    # 开发过程中的文档
│
├─src                                     # 主要代码
   │  main.py                             # 项目入口文件
   │
   ├─components                           # 组件
   │  │  edit_setting_card.py             # 设置卡组件
   │  │  file_list_setting_card.py        # 文件导入组件
   │  │  tabInterface.py                  # 标签页组件
   │
   ├─operations                           # 算法逻辑
   │  │  category.py                      # 按视频标签分类
   │  │  CB.py                            # 基于内容的推荐
   │  │  CF_SVD.py                        # SVD推荐算法
   │  │  CF_user.py                       # 基于用户协同过滤
   │  │  find_video_title.py              # 根据id输出视频标题
   │  │  generate_preferrence_matrix.py   # 产生用户偏好矩阵
   │  │  generate_rating_scores.py        # 用户-视频评分矩阵生成
   │  │  generate_time_series.py          # 视频历史播放量生成
   │  │  load_data.py                     # 加载评分矩阵
   │  │  predict.py                       # 视频未来播放量预测
   │  │  userActionCluster.py             # 视频聚类
   │  │  userCluster.py                   # 用户聚类
   │  │  user_video_rating.py             # 评分随机生成
   │
   ├─utils                                # 辅助函数
   │  │  settings.py                      # 管理设置文件
   │  │  style_sheet.py                   # 为页面和组件应用qss
   │  │  video_type.py                    # 视频标签
   │
   └─view                                 # 子页面
       │  cluster_interface.py            # 聚类页
       │  predict_interface.py            # 预测页
       │  recommend_interface.py          # 推荐页
```
