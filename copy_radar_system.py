# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_rda.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
import sys
import pyradar
import cv2 as cv
import numpy as np

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1101, 381))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_rtm = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_rtm.setMinimumSize(QtCore.QSize(300, 300))
        self.label_rtm.setAlignment(QtCore.Qt.AlignCenter)
        self.label_rtm.setObjectName("label_rtm")
        self.horizontalLayout.addWidget(self.label_rtm)
        self.label_dtm = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_dtm.setMinimumSize(QtCore.QSize(300, 300))
        self.label_dtm.setAlignment(QtCore.Qt.AlignCenter)
        self.label_dtm.setObjectName("label_dtm")
        self.horizontalLayout.addWidget(self.label_dtm)
        self.label_atm = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_atm.setMinimumSize(QtCore.QSize(300, 300))
        self.label_atm.setAlignment(QtCore.Qt.AlignCenter)
        self.label_atm.setObjectName("label_atm")
        self.horizontalLayout.addWidget(self.label_atm)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.RTM = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.RTM.setMinimumSize(QtCore.QSize(300, 10))
        self.RTM.setAlignment(QtCore.Qt.AlignCenter)
        self.RTM.setObjectName("RTM")
        self.horizontalLayout_2.addWidget(self.RTM)
        self.DTM = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.DTM.setMinimumSize(QtCore.QSize(300, 10))
        self.DTM.setAlignment(QtCore.Qt.AlignCenter)
        self.DTM.setObjectName("DTM")
        self.horizontalLayout_2.addWidget(self.DTM)
        self.ATM = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.ATM.setMinimumSize(QtCore.QSize(300, 10))
        self.ATM.setAlignment(QtCore.Qt.AlignCenter)
        self.ATM.setObjectName("ATM")
        self.horizontalLayout_2.addWidget(self.ATM)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(460, 390, 181, 51))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_rtm.setText(_translate("Form", "label_rtm"))
        self.label_dtm.setText(_translate("Form", "label_dtm"))
        self.label_atm.setText(_translate("Form", "label_atm"))
        self.RTM.setText(_translate("Form", "TextLabel"))
        self.DTM.setText(_translate("Form", "TextLabel"))
        self.ATM.setText(_translate("Form", "TextLabel"))
        self.pushButton.setText(_translate("Form", "PushButton"))
        self.initUI()

    def initUI(self):
        # 信号与槽连接, PyQt5与Qt5相同, 信号可绑定普通成员函数
        self.pushButton.clicked.connect(self.processSlot)
        # 数据读取器初始化
        self.data_reader = pyradar.radar_data_reader()
        # 把rtm从np转为cv数据
        self.update_data(frame_seq = 0)      # 更新第1帧数据
        # 刷新显示
        self.refreshShow()

    def processSlot(self):
        self.start_refresh_data()

    def update_data(self,frame_seq=0):
        self.data_reader.update_image(frame_seq)
        # 从np数据转成cv数据
        self.rtm = self.np_to_cvimg("rtm")
        self.dtm = self.np_to_cvimg("dtm")
        self.atm = self.np_to_cvimg("atm")
        # 从cv数据转成qimg数据
        self.qrtm = self.cv_to_qimg(self.rtm)
        self.qdtm = self.cv_to_qimg(self.dtm)
        self.qatm = self.cv_to_qimg(self.atm)


    def start_refresh_data(self):
        for frame_seq in range(self.data_reader.max_n_frames):
            self.update_data(frame_seq)
            self.refreshShow()
            # TODO:  QApplication.processEvents() 刷新界面，这就是最深的坑，没有这句，不会刷新
            cv.waitKey(40)

    def refreshShow(self):

        self.label_rtm.setPixmap(QPixmap.fromImage(self.qrtm))
        self.label_dtm.setPixmap(QPixmap.fromImage(self.qdtm))
        self.label_atm.setPixmap(QPixmap.fromImage(self.qatm))

        QtWidgets.QApplication.processEvents()  # 刷新界面

    def np_to_cvimg(self, input_data_type):
        if input_data_type == "rtm":
            local_data = self.data_reader.rtm
        elif input_data_type == "dtm":
            local_data = self.data_reader.dtm
        elif input_data_type == "atm":
            local_data = self.data_reader.atm
        img = cv.merge([local_data, local_data, local_data])
        return img

    def cv_to_qimg(self, img):
        # 提取图像的尺寸和通道, 用于将opencv下的image转换成Qimage
        cv.normalize(img, img, 0, 255, cv.NORM_MINMAX)
        img = img.astype(np.uint8)
        img = cv.applyColorMap(img, cv.COLORMAP_JET)

        height, width, channel = img.shape
        bytesPerLine = 3 * width
        qImg = QImage(img.data, width, height, bytesPerLine,
                           QImage.Format_RGB888).rgbSwapped()
        return qImg



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setFixedSize(1100, 450)
    ui = Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

