# 运行

1. 项目用到的库：pyqt6、qfluentwidget、numpy、pandas，要求 python >= 3.6

   - 没有，可以单个下载，也可在`demo`文件夹下打开终端，运行`pip install requirement.txt`

2. 在`demo`文件夹下打开终端，运行`python main.py`

# 项目文件结构

```
demo
│  config.json                       设置文件，保存有上次退出时设置的参数
│  main.py                           程序主入口
│  README.md                         本文档
│  requirement.txt                   项目依赖的库
│
├─components                         组件文件夹，重新组件封装的组件(来资qfluentWidget)
│  │  edit_setting_card.py           设置卡片
│  └─ file_list_setting_card.py      文件列表设置卡片
│
├─data                               数据文件夹，存放算法过程中产生的数据，如评分矩阵、相似度矩阵
│
├─docs                               开发过程中的文档
│  │  lblinm.md
│  └─ 用户评分数据模拟01.md
│
├─operations                         算法文件夹，存放关于生成评分、视频推荐、聚类等操作的算法逻辑
│  │  CF_MF.py                       矩阵分解推荐算法
│  │  CF_user.py                     基于用户的协同过滤算法
│  │  find_video_title.py            接收推荐结果，返回视频标题
│  │  load_data.py                   加载数据
│  └─ user_video_rating.py           生成评分数据
│
├─resource                           资源文件夹，存放有图片、qss等静态资源
│  ├─image
│  │      logo.png
│  │
│  └─qss
│      ├─dark
│      │      recommend_interface.qss
│      │
│      └─light
│              recommend_interface.qss
│
├─utils                              存放一些界面操作逻辑能用到的函数
│  │  settings.py                    产生设置类，连接config.json交互和界面类
│  └─ style_sheet.py                 将qss应用到界面类中
│
└─view                               界面文件夹，存放子页面文件
   │  cluster_interface.py           聚类页
   │  predict_interface.py           预测页
   └─ recommend_interface.py         推荐页

```

# issue/bug

- [x] python 文件中使用相对路径错误:

  - `print(os.getcwd())`发现是项目根目录`E:\project\rec\work_together`
  - 相对路径是相对于运行该程序的目录的，我在项目根目录下运行了该文件
  - `view`中文件 import`operations`文件夹下的 py 文件，以`from operation.xxx import xxx`引用

- [x] CF_user 推荐的结果 vid 值较小，范围几乎在(0,300)，但视频总数有 12k 多个
  - 评分生成过于粗糙，预测评分后结果拉不开差距
- [ ] 删除 app\download 的功能

# 进度

- [x] 模拟用户观看视频、评分行为，生成评分矩阵
- [x] 实现推荐视频给某用户
- [ ] 矩阵分解算法应用
- [ ] 基于内容的推荐
- [ ] 基于内容的聚类
- [ ] 时间序列预测算法
