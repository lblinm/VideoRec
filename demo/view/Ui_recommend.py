# Form implementation generated from reading ui file 'e:\project\pyqt6_study\recommend.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_recommend(object):
    def setupUi(self, recommend):
        recommend.setObjectName("recommend")
        recommend.resize(408, 391)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(recommend.sizePolicy().hasHeightForWidth())
        recommend.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        recommend.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(recommend)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem1)
        self.label_video_file = CaptionLabel(parent=recommend)
        self.label_video_file.setObjectName("label_video_file")
        self.horizontalLayout_8.addWidget(self.label_video_file)
        self.lineEdit_video_file = LineEdit(parent=recommend)
        self.lineEdit_video_file.setObjectName("lineEdit_video_file")
        self.horizontalLayout_8.addWidget(self.lineEdit_video_file)
        self.pushButton_video_file = PushButton(parent=recommend)
        self.pushButton_video_file.setObjectName("pushButton_video_file")
        self.horizontalLayout_8.addWidget(self.pushButton_video_file)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.label_uid_num = CaptionLabel(parent=recommend)
        self.label_uid_num.setObjectName("label_uid_num")
        self.horizontalLayout.addWidget(self.label_uid_num)
        self.lineEdit_user_num = LineEdit(parent=recommend)
        self.lineEdit_user_num.setObjectName("lineEdit_user_num")
        self.horizontalLayout.addWidget(self.lineEdit_user_num)
        self.pushButton_user_num = PushButton(parent=recommend)
        self.pushButton_user_num.setObjectName("pushButton_user_num")
        self.horizontalLayout.addWidget(self.pushButton_user_num)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.label_video_num = CaptionLabel(parent=recommend)
        self.label_video_num.setObjectName("label_video_num")
        self.horizontalLayout_2.addWidget(self.label_video_num)
        self.lineEdit_video_num = LineEdit(parent=recommend)
        self.lineEdit_video_num.setObjectName("lineEdit_video_num")
        self.horizontalLayout_2.addWidget(self.lineEdit_video_num)
        self.pushButton_video_num = PushButton(parent=recommend)
        self.pushButton_video_num.setObjectName("pushButton_video_num")
        self.horizontalLayout_2.addWidget(self.pushButton_video_num)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.label_rec_user = CaptionLabel(parent=recommend)
        self.label_rec_user.setObjectName("label_rec_user")
        self.horizontalLayout_3.addWidget(self.label_rec_user)
        self.lineEdit_rec_uid = LineEdit(parent=recommend)
        self.lineEdit_rec_uid.setObjectName("lineEdit_rec_uid")
        self.horizontalLayout_3.addWidget(self.lineEdit_rec_uid)
        self.pushButton_rec_uid = PushButton(parent=recommend)
        self.pushButton_rec_uid.setObjectName("pushButton_rec_uid")
        self.horizontalLayout_3.addWidget(self.pushButton_rec_uid)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem8)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.frame = QtWidgets.QFrame(parent=recommend)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.label_rec_result = BodyLabel(parent=self.frame)
        self.label_rec_result.setGeometry(QtCore.QRect(10, 10, 351, 16))
        self.label_rec_result.setObjectName("label_rec_result")
        self.horizontalLayout_5.addWidget(self.frame)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem9)

        self.retranslateUi(recommend)
        QtCore.QMetaObject.connectSlotsByName(recommend)

    def retranslateUi(self, recommend):
        _translate = QtCore.QCoreApplication.translate
        recommend.setWindowTitle(_translate("recommend", "Form"))
        self.label_video_file.setText(_translate("recommend", "选择短视频文件路径"))
        self.pushButton_video_file.setText(_translate("recommend", "选择"))
        self.label_uid_num.setText(_translate("recommend", "模拟生成的用户数量"))
        self.pushButton_user_num.setText(_translate("recommend", "确认"))
        self.label_video_num.setText(_translate("recommend", "每用户观看视频数量"))
        self.pushButton_video_num.setText(_translate("recommend", "确认"))
        self.label_rec_user.setText(_translate("recommend", "推荐视频给用户(uid)"))
        self.pushButton_rec_uid.setText(_translate("recommend", "确认"))
        self.label_rec_result.setText(_translate("recommend", "基于用户的协同过滤算法推荐结果："))

from qfluentwidgets import BodyLabel, CaptionLabel, LineEdit, PushButton
