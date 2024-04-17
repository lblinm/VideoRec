## 准备

1. git、anaconda 下载安装
2. conda 创建虚拟环境或使用 base 环境，python>=3.6(我的是 3.10)
3. 下载安装 pyqt6

## 爬取短视频标题文本

得到 csv 文件，内容为

| vid | title         |
| --- | ------------- |
| 0   | 视频标题 xxxx |

加入了反爬机制: 随机生成随眠时间(虽然只爬首页可能没有也一样能爬())

## 搭建项目开发框架

1. 下载`PyQt6-Fluent-Widgets`轻量版: `pip install PyQt6-Fluent-Widgets -i https://pypi.org/simple/`

   - 查看 ui 效果`git clone -b PyQt6 git@github.com:zhiyiYo/PyQt-Fluent-Widgets.git`，`cd examples/gallery`, `python demo.py`

2. `designer`中做出界面，使用刚才下载的组件库
   - 做出窗口自适应
     1. 使用菜单栏的顶级布局
     2. `widget`的`sizepolicy`属性改为`expending`

## 注意事项

- textedit`setMarkdown()`写入 markdown，换行使用`\n\n`，不能用`\n`,`</br>`

## bug 困扰

- [x] python 文件中使用相对路径错误:

  - `print(os.getcwd())`发现是项目根目录`E:\project\rec\work_together`
  - 相对路径是相对于运行该程序的目录的，我在项目根目录下运行了该文件
  - https://www.zhihu.com/question/466490632
  - 获取项目根目录：`project_dir=os.path.dirname(sys.argv[0])`

- [x] CF_user 推荐的结果 vid 值较小，范围几乎在(0,300)，但视频总数有 12k 多个
  - 评分过于粗糙

## 后续工作

- [x] github 协作，写 ignore
- [x] 协同过滤算法
- [x] 使用 dotenv 文件管理环境变量 -> os 模块管理
- [ ] MF 算法的应用和 cache 存储
- [ ] 基于内容的推荐算法
- [ ] 时间序列预测算法

## 写文档

- 在项目根目录执行`tree /F`即可生成文件树，注意不是`tree -F`
