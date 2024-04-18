# coding:utf-8
import sys
from enum import Enum

from PyQt6.QtCore import QLocale
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            OptionsValidator, RangeConfigItem, RangeValidator, ConfigValidator,
                            FolderListValidator, Theme, FolderValidator, ConfigSerializer)



def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


class Config(QConfig):
    """ Config of application """

    # folders
    videoTitleFiles = ConfigItem(
        "Folders", "VideoTitle", [] 
    )
    downloadFolder = ConfigItem(
        "Folders", "Download", "app/download", FolderValidator())

    # 评分矩阵的用户数量
    userNum = RangeConfigItem("rating", "userNum", 1000, RangeValidator(0,10000))

    # 评分矩阵每用户观看视频
    videoPerPerson = RangeConfigItem("rating","videoPerPerson", 100, RangeValidator(0,500))

    # 推荐算法选择
    recChoose = OptionsConfigItem(
        "rec", "algorithm", "Userbased CF", OptionsValidator(["User based CF","Item based CF","BiassSVD","Contend based"]))
    
    # 推荐用户id选择
    recUid = ConfigItem(
        "rec", "recUid", 1,  ConfigValidator()
    )
    # topk排序
    recTopk = RangeConfigItem(
        "rec", "topk", 10, RangeValidator(10,100)
    )

cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load('config.json', cfg)