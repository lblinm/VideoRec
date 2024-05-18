# 准备打包工具

注意安装打包工具的虚拟环境、给项目运行准备的虚拟环境、项目这三个的目录要在同一个盘，否则会报错

1. 安装`embed-pyhon-manager`库

`pip install pyportable-installer`时，由于找不到作者写的另一个库，会将版本降到 3.+，由此引发一系列错误

要下载另一个库，需要把 github 上的 clone 到本地再安装

```shell
git clone git@github.com:likianta/embed-python-manager.git
cd embed-python-manager
pip install .
```

2. 安装`pyportable-installer`

```shell
pip install pyportable-installer==4.4.2
```

3. 修改`emebed-python-manager`库的下载源

> 不修改的话，打包时会报错：taobao 源的 SSL 证书错误

在 python 环境所在目录找到`embed-python-manager`库目录，打开`source_list\npm_taobao_org.yml`

1. 修改`home`值`https://npm.taobao.org/mirrors/python/`为清华源`home: https://pypi.tuna.tsinghua.edu.cn/simple/`
2. 项目需要的对应嵌入版 python 下载源修改为正确的源`python310: https://www.python.org/ftp/python/3.10.0/python-3.10.0b4-embed-amd64.zip`

# 准备项目运行的虚拟环境

Anaconda 中

```shell
conda create --prefix=E:/project/rec/try/penv python=3.10
conda env list
conda config --append envs_dirs E:/project/rec/try
conda activate penv
pip install pandas numpy pyqt6 jieba gensim scikit-learn statsmodels pyqtgraph wrapt
pip install PyQt6-Fluent-Widgets -i https://pypi.org/simple/    #需要关掉代理
pip install scipy==1.10.1  # 降版本，否则gemsim报错
```

成功

```shell
Installing collected packages: pytz, PyQt6-Qt6, jieba, wrapt, tzdata, threadpoolctl, six, PyQt6-sip, packaging, numpy, joblib, smart-open, scipy, python-dateutil, pyqtgraph, pyqt6, patsy, scikit-learn, pandas, gensim, statsmodels
Successfully installed PyQt6-Qt6-6.7.0 PyQt6-sip-13.6.0 gensim-4.3.2 jieba-0.42.1 joblib-1.4.2 numpy-1.26.4 packaging-24.0 pandas-2.2.2 patsy-0.5.6 pyqt6-6.7.0 pyqtgraph-0.13.7 python-dateutil-2.9.0.post0 pytz-2024.1 scikit-learn-1.4.2 scipy-1.13.0 six-1.16.0 smart-open-7.0.4 statsmodels-0.14.2 threadpoolctl-3.5.0 tzdata-2024.1 wrapt-1.16.0
Successfully uninstalled scipy-1.13.0
Successfully installed PyQt6-Fluent-Widgets-1.5.6 PyQt6-Frameless-Window-0.3.9 darkdetect-0.8.0 pywin32-306
```

确定用此虚拟环境运行项目无误

# 项目目录调整

注意项目所在盘要和虚拟环境的盘一样

```
project
│  config.json
│  pyproject.json
│  README.md
│  requirement.txt
│  requirements.txt
│
├─assets
│
├─data
│
├─docs
│
├─src
   │  main.py
   │
   ├─components
   │
   ├─operations
   │
   ├─utils
   │
   └─view
```

# 在项目目录下编写打包配置文件

项目根目录下新建`pyproject.json`

```json
{
  "app_name": "VideoRecTool",
  "app_version": "0.1.0",
  "description": "A simple tool for video recommendation and analysis.",
  "authors": "lblinm <lblinm@outlook.com>",
  "build": {
    "proj_dir": "src",
    "dist_dir": "dist/{app_name}-{app_version}",
    "launchers": {
      "{app_name}": {
        "file": "src/main.py",
        "icon": "",
        "function": "",
        "args": [],
        "kwargs": {}
      }
    },
    "readme": "",
    "attachments": {
      "assets": "assets",
      "data": "only_folder",
      "config.json": "asset"
    },
    "attachments_exclusions": [],
    "attachments_exist_scheme": "overwrite",
    "module_paths": [],
    "module_paths_scheme": "translate",
    "python_version": "3.9",
    "venv": {
      "enabled": true,
      "mode": "pip",
      "options": {
        "depsland": {
          "venv_name": "{app_name_snake}_venv",
          "venv_id": "",
          "requirements": [],
          "offline": false,
          "local": ""
        },
        "source_venv": {
          "path": "E:/project/rec/try/penv",
          "copy_venv": true
        },
        "pip": {
          "requirements": [
            "darkdetect==0.8.0",
            "gensim==4.3.2",
            "jieba==0.42.1",
            "joblib==1.4.2",
            "numpy==1.26.4",
            "packaging==24.0",
            "pandas==2.2.2",
            "patsy==0.5.6",
            "pyQt6==6.7.0",
            "PyQt6-Fluent-Widgets==1.5.6",
            "PyQt6-Frameless-Window==0.3.9",
            "PyQt6-Qt6==6.7.0",
            "PyQt6-sip==13.6.0",
            "pyqtgraph==0.13.7",
            "python-dateutil==2.9.0.post0",
            "pytz==2024.1",
            "pywin32==306",
            "scikit-learn==1.4.2",
            "scipy==1.10.1",
            "setuptools==69.5.1",
            "six==1.16.0",
            "smart-open==7.0.4",
            "statsmodels==0.14.2",
            "threadpoolctl==3.5.0"
          ],
          "pypi_url": "https://pypi.org/simple",
          "offline": false,
          "local": ""
        },
        "embed_python": {
          "path": ""
        }
      }
    },
    "compiler": {
      "enabled": false,
      "mode": "pyportable_crypto",
      "options": {
        "cythonize": {
          "c_compiler": "msvc",
          "python_path": "auto_detect"
        },
        "pyarmor": {
          "license": "trial",
          "obfuscate_level": 0
        },
        "pyc": {
          "optimize_level": 0
        },
        "pyportable_crypto": {
          "key": "{random}"
        },
        "zipapp": {
          "password": ""
        }
      }
    },
    "experimental_features": {
      "add_pywin32_support": false,
      "platform": "system_default",
      "add_tkinter_support": {
        "enable": true,
        "system_python_path": "_auto_detect"
      }
    },
    "enable_console": false
  },
  "note": "",
  "pyportable_installer_version": "4.4.2"
}
```

# 开始打包

`pyproject.json`同级目录下终端运行

```shell
python -m pyportable_installer build
```
