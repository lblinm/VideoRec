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

    # 推荐
    # 数据集
    # 视频标题
    videoTitleFiles = ConfigItem(
        "Folders", "VideoTitle", [] 
    )
    # 评分矩阵
    ratingPath = ConfigItem(
        "Folders", "ratingPath", []
    )
    # 评分矩阵的用户数量
    userNum = RangeConfigItem("rating", "userNum", 10000, RangeValidator(1000,20000))

    # 评分矩阵每用户观看视频
    videoPerPerson = RangeConfigItem("rating","videoPerPerson", 500, RangeValidator(500,2000))

    # 推荐算法选择
    recChoose = OptionsConfigItem(
        "rec", "algorithm", "Userbased CF", OptionsValidator(["User based CF", "SVD CF", "Contend based"])
    )
    
    # 推荐用户id选择
    recUid = ConfigItem(
        "rec", "recUid", 1,  ConfigValidator()
    )
    # topk排序
    recTopk = RangeConfigItem(
        "rec", "topk", 10, RangeValidator(10,100)
    )


    # 聚类
    videoClusterAlgorithm = OptionsConfigItem(
        "cluster", "videoClusterAlgorithm", "基于用户行为", OptionsValidator(["基于原有标签","基于用户行为"])
    )
    userClusterAlgorithm = OptionsConfigItem(
        "cluster", "userClusterAlgorithm", "基于相似兴趣", OptionsValidator(["基于相似兴趣"])
    )


    # 预测
    timeSeriesPath = ConfigItem(
        "Folders", "timeSeriesPath", []
    )
    predictDays = RangeConfigItem(
        "predict", "days", 10, RangeValidator(10,30)
    )
    vidPre = ConfigItem(
        "predict", "vid", 1, ConfigValidator()
    )
    predictAlgorithm = OptionsConfigItem(
        "predict", "algorithm", "ARIMA", OptionsValidator(["ARIMA","Holt-Winters"])
    )

cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load('config.json', cfg)