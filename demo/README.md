# 运行

1. 确保有：python>=3.6, PyQt6-Fluent-Widgets 库，否则：`pip install requirement.txt`
2. 在 demo 目录下，`python main.py`

# 项目文件结构

```
demo
│  main.py                       运行入口文件
│  README.md                     文档
│  requirement.txt               需要安装的库
│
├─data                           用来存放评分矩阵、相似度矩阵的数据
│
├─operations                     存放逻辑代码
│  │  CF_user.py                 基于用户的协同过滤推荐算法
│  │  load_data.py               加载评分矩阵
│  └─ user_video_rating.py       模拟用户评分行为
│
└─view                           ui文件，也写有数据操作逻辑
   │  recommend.py               推荐页面，写数据渲染、调用函数等
   │  recommend.ui               ui推荐页面
   └─Ui_recommend.py             ui文件生成的py文件

```

# issue/bug

- [x] python 文件中使用相对路径错误:

  - `print(os.getcwd())`发现是项目根目录`E:\project\rec\work_together`
  - 相对路径是相对于运行该程序的目录的，我在项目根目录下运行了该文件
  - `view`中文件 import`operations`文件夹下的 py 文件，以`from operation.xxx import xxx`引用

- [ ] CF_user 推荐的结果 vid 值较小，范围几乎在(0,300)，但视频总数有 12k 多个
  - 可能是逻辑处理出了问题，需要细查

# 进度

- [x] 模拟用户观看视频、评分行为，生成评分矩阵
- [x] 实现推荐视频给某用户 -> 目前只有基于用户的协同过滤算法
